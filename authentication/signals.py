from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

@receiver(post_migrate)
def create_default_groups_and_superuser(sender, **kwargs):
    if sender.name == 'authentication':
        groups = ['FINANCIERA', 'ACTIVO']
        for name in groups:
            Group.objects.get_or_create(name=name)

    User = get_user_model()

    if not User.objects.filter(username='developer').exists():
            user = User.objects.create_superuser(
                username='developer',
                email='developer@example.com',
                password='default'
            )
            print('✅ Superusuario "developer" creado.')