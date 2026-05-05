from django.apps import AppConfig


class FilmeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filme'

    def ready(self):
        import os
        from django.db.utils import ProgrammingError, OperationalError
        from .models import Usuario


        email = os.getenv('EMAIL_ADMIN')
        senha = os.getenv('SENHA_ADMIN')

        try:
            if not email or not senha:
                return


            usuarios = Usuario.objects.filter(email=email)
            if not usuarios:
                Usuario.objects.create_superuser(
                    username='admin',
                    email=email,
                    password=senha,
                    is_active=True,
                    is_staff=True,
                    is_superuser=True
                )
        except (ProgrammingError, OperationalError):
            return
