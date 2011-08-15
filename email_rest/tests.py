# -*- coding: utf-8 -*-
"""
This file includes all the tests to test the api functionallity.

"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.core import mail
from models import EmailConfirmation
from models import EmailAddress

import sys

if sys.version_info >= (2, 6):
    import json
else:
    import simplejson as json
    
class EmailTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = None
        
        user1 = User.objects.create_user('test_user','', 'test_pass')
        self.client.login(username='test_user', password='test_pass')



    
    def test_email_update(self):
        """
        Test registering new email
        """
        
        #case 1 - no email sent
        post_content = {"email" : ""}
        
        response = self.client.post(reverse('api_manage_email'),
                                    json.dumps(post_content),
                                    content_type='application/json')
        
        self.assertEquals(response.status_code,
                400,
                "trying to set empty email address")

    def test_email_update_with_data(self):
        post_content = {"email" : "test@aalto.fi"}
        response = self.client.post(reverse('api_manage_email'),
                                    json.dumps(post_content),
                                    content_type='application/json')

        #Test if confirmation email is sent
        self.assertEquals(len(mail.outbox), 1, "Confirmation email not sent")

        #confirm the email

        emailAddress = EmailAddress.objects.get(email = "test@aalto.fi")
        emailConfirmation = EmailConfirmation.objects.get(email_address = emailAddress)

        response = self.client.get(reverse('api_emailconfirmation', args=[emailConfirmation.confirmation_key]))
        self.assertEquals(response.status_code,
                200,
                "the email address confirmation url is not working")
        response = self.client.get(reverse('api_manage_email'))
        responsejson = json.loads(response.content)
        self.assertEquals(responsejson.get('email'), "test@aalto.fi", "The email obtain using get is not ok")

        #delete the email and test again the GET
        response = self.client.delete(reverse('api_manage_email'))
        self.assertEquals(response.status_code,
                200,
                "the email address delete not working")
        response = json.loads(self.client.get(reverse('api_manage_email')).content)
        self.assertEquals(response.get('email'), "", "The email obtain using GET after delete is not an empty string")
    
    def test_email_fail_for_registration(self):
        
        user2 = User.objects.create_user('cristian1001','', 'cristi')
        EmailAddress.objects.add_email(user2, 'test2@test.com')
        user3 = User.objects.create_user('cristian1002','', 'cristi')
        EmailAddress.objects.add_email(user3, 'test3@test.com')
        
        post_content = {"email" : "test2@test.com", "registration" : True}
        response = self.client.post(reverse('api_manage_email'),
                            json.dumps(post_content),
                            content_type='application/json')
        self.assertEquals(response.status_code,
                400,
                "There email address has to be unique. Duplicates has been aceepted!")
        
        user_list = User.objects.filter(email="test2@test.com")
        
        self.assertEquals(len(user_list),
                0,
                "The user that tried to register with a duplicate email was not deleted!")
