from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@receiver(post_save, sender=SocialAccount)
def create_or_update_google_user_profile(sender, instance, created, **kwargs):
    user = instance.user
    social_data = instance.extra_data  # Dados do Google que vêm com a autenticação

    if created:
        # Se for a criação do perfil
        user.name = social_data.get('name', user.name)  # O nome do Google é atribuído ao campo 'name'
        user.email = social_data.get('email', user.email)
        user.phone = social_data.get('phone', user.phone)
        user.google_id = instance.uid  # Preenche o campo google_id
        user.profile_picture = instance.get_avatar_url()  # Foto de perfil do Google
        user.save()
    else:
        # Atualiza os dados se necessário
        if user.name != social_data.get('name', user.name):
            user.name = social_data.get('name', user.name)
            user.save()

        if user.email != social_data.get('email', user.email):
            user.email = social_data.get('email', user.email)
            user.save()

        if user.phone != social_data.get('phone', user.phone):
            user.phone = social_data.get('phone', user.phone)
            user.save()

        # Atualiza os outros campos
        user.google_id = instance.uid  # Atualiza o google_id
        user.profile_picture = instance.get_avatar_url()  # Atualiza a foto de perfil
        user.save()
