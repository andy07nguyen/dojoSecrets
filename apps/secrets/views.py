from django.shortcuts import render, redirect
from .models import User, Secret
from django.contrib import messages
from django.db.models import Count


# Create your views here.
def index(request):
    request.session['id'] = 2
    currentuser = User.objects.get(id=request.session['id'])
    context = {
        "secrets" : Secret.objects.annotate(num_likes=Count('likers')),
        "user" : currentuser
    }
    allsecrets = Secret.objects.annotate(num_likes=Count('likers'))
    print "**********************"
    for secret in allsecrets:
        print secret.likers.all()
    print "**********************"
    return render(request, 'secrets/index.html', context)

def process(request):

    print "Made it to the process route!", request.POST
    if request.method == "GET":
        return redirect('/')
    if 'id' not in request.session:
        return redirect('/')
    else:
        result = Secret.objects.validate(request.POST, request.session['id'])
        if result[0] == True:
            #result[1] is an array of messages
            for message in result[1]:
                messages.info(request, message)
        else:
            for message in result[1]:
                messages.error(request, message)
        return redirect('/')
    # storing the secret in the database
    # validate the secret, make sure there's something in the field
    # send the secret to the models to be validated
    # send the logged user in case the user is needed to create a secret

def createlike(request, id):
    print "made it to create like", id
    result = Secret.objects.createLike(request.session['id'], id)
    if result[0]:
        return redirect('/')
    else:
        messages.error(request, result[1])
        return redirect('/')
