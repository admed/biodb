from django.db import models
from django.contrib.auth.models import User  
from django.utils.translation import ugettext as _  
from userena.models import UserenaBaseProfile, UserenaSignup  

# Create your models here.

class MyProfile(UserenaBaseProfile):  
    user = models.OneToOneField(User,unique=True,  
                  verbose_name=_('user'),related_name='my_profile')  
    favourite_snack = models.CharField(_('favouritesnack'),max_length=5) 
    # Automagically create the user UserenaSignup object when referenced
    User.userena_signup = property(lambda u: UserenaSignup.objects.get_or_create(user=u)[0])