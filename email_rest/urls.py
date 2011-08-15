# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

urlpatterns = patterns('email.views',
            url(r'^confirm-email/(\w+)/$',
                'confirm_email',
                name="api_emailconfirmation"),
            url(r'^email/$',
                'email',
                name="api_manage_email"),
        )
