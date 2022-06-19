from django.apps import AppConfig


class PollishConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pollish'

    # import signals for application
    def ready(self):
        import pollish.signals
