from django.apps import AppConfig


class HostelsConfig(AppConfig):
    name = 'Hostel'

    def ready(self):
        import Hostel.signals
