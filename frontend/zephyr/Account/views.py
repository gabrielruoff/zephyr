from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.template import loader


def index(request):
    template = loader.get_template('templates/Account.html')
    context = {

    }
    return HttpResponse(template.render(context, request))

def account(request, username):
    return HttpResponse("Username is %s." % username)