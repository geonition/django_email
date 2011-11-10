/*
email_rest application javascript functions
*/
gnt.email_rest = {};

/*
helper function to check regular expressions
*/
gnt.email_rest.checkRegexp =
function(o, regexp) {
    if ( !( regexp.test( o ) ) ) {
        return false;
    } else {
        return true;
    }
};

gnt.email_rest.validate_email =
function(email_address) {
    if (email_address != null && email_address.length > 6){
	isEmailValid = gnt.email_rest.checkRegexp( email_address, /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
	if (!isEmailValid){
	    return false;
	} else {
	    return true;
	}
    } else {
	return false;
    }
};

gnt.email_rest.get_email =
function(callback_function) {
      
	$.ajax({
	  url: '{% url api_manage_email %}',
	  type: "GET",
	  data: {},
	  success: function(data){
			if(callback_function !== undefined) {
			    callback_function(data);
			}
	    },
	  error: function(e) {
                      if(callback_function !== undefined) {
                          callback_function(e);    
                      }
        },  
	  dataType: "json"
	});
};


gnt.email_rest.save_email =
function (email, callback_function) {

    if (!gnt.email_rest.validate_email(email.email)){
	if(callback_function !== undefined) {
	    var e = {"status" : 400, "responseText" : "Email address is invalid"}; 
	    callback_function(e);
	}
    }
    
    $.ajax({
	url: '{% url api_manage_email %}',
	type: "POST",
	data: {'value': email},
	contentType: 'application/json',
	success: function(data){
	    if(callback_function !== undefined) {
		callback_function(data);
		}
	    },
	error: function(e) {
	    if(callback_function !== undefined) {
		callback_function(e);
	    }
	},
	dataType: "json"
    });
};

/*
typeString
Default: 'GET'

The type of request to make ("POST" or "GET"), default is "GET". 
Note: Other HTTP request methods, such as PUT and DELETE, can also be used here, but they are not supported by all browsers.
*/
gnt.email_rest.delete_email =
function(callback_function) {
	$.ajax({
	  url: '{% url api_manage_email %}',
	  type: "DELETE",
	  data: {},
	  success: function(data){
				if(callback_function !== undefined) {
				    callback_function(data);	
				}	
	   },
       error: function(e) {
                      if(callback_function !== undefined) {
                          callback_function(e);    
                      }
       },  
	  dataType: "text"
	});
}
