from django.apps import AppConfig


class MypersonalexpensetrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myPersonalExpenseTracker'

    def ready(self):
        import myPersonalExpenseTracker.signals
