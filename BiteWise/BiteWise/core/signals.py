from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@receiver(post_save, sender=SocialAccount)
def create_or_update_google_user_profile(sender, instance, created, **kwargs):
    user = instance.user
    social_data = instance.extra_data 

    if created:
        user.name = social_data.get('name', user.name)  
        user.email = social_data.get('email', user.email)
        user.phone = social_data.get('phone', user.phone)
        user.google_id = instance.uid  
        user.profile_picture = instance.get_avatar_url() 
        user.save()
    else:
        if user.name != social_data.get('name', user.name):
            user.name = social_data.get('name', user.name)
            user.save()

        if user.email != social_data.get('email', user.email):
            user.email = social_data.get('email', user.email)
            user.save()

        if user.phone != social_data.get('phone', user.phone):
            user.phone = social_data.get('phone', user.phone)
            user.save()

        user.google_id = instance.uid 
        user.profile_picture = instance.get_avatar_url()  
        user.save()
