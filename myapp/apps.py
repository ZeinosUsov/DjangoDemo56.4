from django.apps import AppConfig
from django.db.models.signals import post_migrate

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        from django.contrib.auth.models import User
        def create_braveguar(sender, **kwargs):
            if not User.objects.filter(username='BraveGuar').exists():
                User.objects.create_user(
                    username='BraveGuar',
                    password='gosdum',
                    email='admin@gosdumamusic.ru'
                )
                print("✅ Администратор BraveGuar создан (пароль: gosdum)")
        post_migrate.connect(create_braveguar, sender=self)