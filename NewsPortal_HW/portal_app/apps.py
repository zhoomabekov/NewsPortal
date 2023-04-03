from django.apps import AppConfig


class PortalAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portal_app'

    def ready(self):
        import portal_app.signals