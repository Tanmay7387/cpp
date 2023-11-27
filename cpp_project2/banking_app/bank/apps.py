from django.apps import AppConfig


class BankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bank'

class YourAppNameConfig(AppConfig):
    name = 'bank'

    def ready(self):
        import your_app_name.signals    
