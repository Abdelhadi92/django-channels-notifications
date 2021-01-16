from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)

    def handle(self, *args, **options):
        file_name = options['name']

        DIRNAME = os.path.dirname(__file__)
        template_path = os.path.join(DIRNAME, 'templates/channelTemplate.txt')
        template_file = open(template_path, 'r')

        new_file = open("{}.py".format(file_name), "w+")
        new_file.write(template_file.read().format(name=file_name))

        self.stdout.write(self.style.SUCCESS('Channel created successfully.'))
