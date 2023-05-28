from django.shortcuts import redirect, render
from .forms import *
from .models import *
from django.contrib import messages

def contact_view(request):
    contact = ContactForm(request.POST or None)

    template_name = 'layout/contact.html'
    context = {
        'contact': contact 
    }
    
    if contact.is_valid():
        new_contact = Contact.objects.create(
            **contact.cleaned_data
        )
        new_contact.save()
        messages.info(request, "Merci de nous avoir contacté, notre équipe sera à votre disposition dans un bref delai !")
        return redirect("contact:main")

    return render(request, template_name, context)
    