import json

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создает объекты модели в БД из данных JSON файла.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file_path',
            type=str,
            help='Путь к файлу.',
        )
        parser.add_argument(
            '--model_name',
            type=str,
            help='Название модели.',
        )
        parser.add_argument(
            '--app_name',
            type=str,
            help='Приложение модели.',
        )

    def handle(self, *args, **options):
        with open(options['file_path'], 'r') as file:
            elements = json.load(file)
            model = apps.get_model(
                options['app_name'],
                options['model_name'],
            )
        elements = [
            model(**element) for element in elements
        ]
        model.objects.bulk_create(elements)
        self.stdout.write(
            self.style.SUCCESS('Загрузка данных успешно завершена.')
        )
