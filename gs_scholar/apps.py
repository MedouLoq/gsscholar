from django.apps import AppConfig


class GsScholarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gs_scholar'
    def ready(self):
        import gs_scholar.signals  