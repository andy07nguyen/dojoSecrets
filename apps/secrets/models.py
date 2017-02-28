from __future__ import unicode_literals

from django.db import models

class SecretManager(models.Manager):
    def validate(self, postData, userid):
        secret = postData['secret']
        messages = []
        if len(secret)<4:
            # too short to go into the database!
            messages.append("Secret must be longer than three characters!")
            return(False, messages)
        else:
            # if the secret looks good, create the secret with the creator as the logged user
            loggeduser = User.objects.get(id=userid)
            try:
                # attempt to create a secret
                self.create(creator = loggeduser, description = secret)
                # make a success message
                messages.append("Your secret was saved")
                # return true because it worked, send back messages
                return(True, messages)
            except:
                # we're catching the error in case something goes wrong with our creation of a secret, we'll send back a message that something went wrong
                messages.append("We could not save your secret at this time")
                return(False, messages)
    def createLike(self, userid, secretid):
        # to create a like, we need the currently logged in user
        currentuser = User.objects.get(id=userid)
        # we also need the secret being liked
        try:
            secretToLike = self.get(id=secretid)
        except:
            return(False, "This secret does not exist in our database")
        #we add the current user to the likers of the secret. (See the many-to-many field in the Secret class)
        secretToLike.likers.add(currentuser)
        return(True, "You liked this!")






class User(models.Model):
    username = models.CharField(max_length = 45)

class Secret(models.Model):
    creator = models.ForeignKey(User)
    description = models.CharField(max_length=300)
    likers = models.ManyToManyField(User, related_name = "User_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SecretManager()
