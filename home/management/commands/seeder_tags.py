from django.core.management import BaseCommand
from apps.common.models import Tag
from django.conf import settings
import os
import json

class Command(BaseCommand):
    help = 'Generate tags'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, 'seeder', 'tags.json')
        with open(file_path, 'r') as file:
            data = json.load(file)

            for tag in data:
                Tag.objects.get_or_create(name=tag['tag'])
        
        self.stdout.write(self.style.SUCCESS('Tags created successfully.'))