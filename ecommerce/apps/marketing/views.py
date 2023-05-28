from datetime import timezone
from django.shortcuts import render
from .models import Newsletter
from .forms import *
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from mailchimp_marketing.api_client import ApiClient
from django.contrib import messages
from mailchimp_marketing import Client
import json
import requests
from django.conf import settings
from .forms import EmailForm

from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError


# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID




# Subscription Logic
def subscribe(email):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))



# # Views here.
# def subscription(request):
#     email_form = EmailForm(request.POST or None)

#     if email_form.is_valid():
#         # new_contact = Newsletter.objects.create(
#         #     **email_form.cleaned_data
#         # )

#         # # new_contact.timestamp = timezone.now()
#         # new_contact.save()
#         subscribe(email_form)

#         messages.success(request, "Merci d'avoir souscris à notre boite aux lettres ! ") # message
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#         # return redirect("/")        

#     template_name = 'base/base.html'
#     context = {
#         'email_form': email_form
#     }
#     return render(request, template_name=template_name, context=context)




# Views here.
def subscription(request):
    if request.method == "POST":
        email = request.POST['email']
        subscribe(email)                    # function to access mailchimp
        messages.success(request, "Vous serez notifié de toutes nouveautés ! ") # message
        new_email = Newsletter.objects.create(
            email=email
        )
        new_email.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            

    return render(request, "marketing/index.html")
