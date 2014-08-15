#FIXIT: To build: 
#Upload Skypegroup user list
#Upload Ning profile list
#Upload Googlegroup profile list
#Upload Skypegroup chat: cut and paste
#Upload Skypegroup chat: downloaded from Skype
#Download Skypegroup chat from Skype
#Send Skype contact request to everyone on a list
#Create Skypechat
#Invite everyone on a list into a Skypechat
#Create master user list from skype, ning and googlegroups

from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.utils.encoding import smart_unicode

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()

    
def index(request):
    return HttpResponse("Hello, world. You're at the volta index.")

def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            print("Received message" + form.cleaned_data['message'])
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'volta/contact.html', {
        'form': form,
    })


def handle_ningusers_file(ningfile):
    return


def upload_ningusers_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_ningusers_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render_to_response('volta/upload.html', {'form': form})

