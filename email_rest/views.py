from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils import translation
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.core.exceptions import ValidationError
from django.core.validators import email_re
from geonition_utils.HttpResponseExtenders import HttpResponseUnauthorized
from models import EmailConfirmation
from models import EmailAddress
from datetime import datetime, timedelta
import logging
import sys

if sys.version_info >= (2, 6):
    import json
else:
    import simplejson as json

# set the ugettext _ shortcut
_ = translation.ugettext

logger = logging.getLogger('api.email.view')

# View used for confirming a user email using the confirmation key
def confirm_email(request, confirmation_key):
    confirmation_key = confirmation_key.lower()
    
    email_address = EmailConfirmation.objects.confirm_email(confirmation_key)
    
    logger.debug(u"Email confirmation attempt for %s with key %s" % (email_address, confirmation_key) )
    
    template = None
    try: # try to get customized template
        template = get_template("emailconfirmation/confirm_email.html")
    except TemplateDoesNotExist: # get default template
        template = get_template("emailconfirmation/default_confirm_template.html")
        
    #the template will handle the invalid confirmation key
    # if the confirmation key was invalid the email_address object is None
    return HttpResponse(template.render(RequestContext(request, {"email_address": email_address})))
    
    
        
#Views used for managing the email
def email(request):
    """
    This function handles the email managing part of the softgis REST api
    
    On GET request this function returns the email of the logged in user
    
    On POST request this function sends a confirmation email
    to the logged in user. The user will have to follow the link in the
    email in order to activate that email address
    
    On DELETE request this function removes existing email from 
    the database for the logged in user.
    
    Returns:
        200 if successful and user exists
        400 if bad request
        404 if user not found

    """
    #check if authenticated
    if not request.user.is_authenticated():
        return HttpResponseForbidden(u"You haven't signed in.")
    
    user = request.user
        
    if(request.method == "GET"):
        
        logger.debug("Email GET request for user %s returned %s" % (user.username, user.email))
        
        #return user email in json format
        json_data = json.dumps({"email":user.email})
        return HttpResponse(json_data, mimetype="application/json")
                
    elif(request.method == "POST"):
        
        try:
            email = json.loads(request.POST.keys()[0]).get("email", "")
        
        except ValueError:
            message = 'JSON decode error'
            logger.warning(message)
        
            return HttpResponseBadRequest(message)
        
        except IndexError:
        
            return HttpResponseBadRequest("POST data was empty so no email address could be retrieven from it")
    
        try:
            is_registration = json.loads(request.POST.keys()[0]).get("registration", False)
        
        except ValueError:
            is_registration = False
            
        logger.debug("Email POST request with param %s" %email)
       
        #check if email was provided
        if (email == "" or email == None):
            logger.warning("Email sent POST was empty or none")
            return HttpResponseBadRequest(
                    u"Expected argument email was not provided")


        
        #Test if the email address is the same as existing one. If so don't send the confirmation email
        if (user.email != email):
          
            #validate email
            if not email_re.match(email):
                 logger.warning("The email address %s is not valid" %email)
                 return HttpResponseBadRequest(
                    u"Email is not valid")
                
            
            #Send confirmation email
            email_address = EmailAddress.objects.add_email(user, email)

            if email_address == None:
                logger.warning("The email address %s is invalid or not unique" %email)
                
                #check if user is just created and delete it as the email registration failed
                three_mins_ago = datetime.now() + timedelta(minutes=-3)
                if user.date_joined > three_mins_ago and is_registration:
                    #delete the user
                    request.user.delete()
                
                return HttpResponseBadRequest(u"Email is either invalid or not unique")    
            else:
                logger.debug("Email %s has been added successfully for user %s and the confimation email has been sent" % (email, user.username))
                return HttpResponse(content = _(u"A confirmation email was sent to your new email address. Follow the intructions in the email to complete the registration."),
                                status = 200)

        logger.debug("The user %s already had assigned email %s so the POST was ignored" % (user.username,email )) 

        return HttpResponse(_(u"You already have this email address assigned to you"),
                            status=200)    
       
    elif (request.method  == "DELETE"):

                
        #reset email and save
        request.user.email = ""

        EmailAddress.objects.filter(user = request.user).delete()
    
        #save changes
        request.user.save()
        
        return HttpResponse(u"Email was succesfully deleted",
                            status=200)
        

                
             
        
    
        
    
    
