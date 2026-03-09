from django.apps import AppConfig


class AnimeVerseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anime_verse'

    def ready(self):
        import anime_verse.signals