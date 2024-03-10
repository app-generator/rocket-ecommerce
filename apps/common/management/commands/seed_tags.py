import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.common.models import Tag


class Command(BaseCommand):
    help = 'Seed the tags table with data from a JSON file'

    def handle(self, *args, **options):
        file_path = os.path.join(settings.MEDIA_ROOT, 'seeder', 'tags.json')
        with open(file_path) as f:
            data = json.load(f)

        existing_tags = Tag.objects.values_list('name', flat=True)

        for item in data:
            tag_name = item['tag']
            tag, created = Tag.objects.get_or_create(name=tag_name)

            if not created:
                self.stdout.write(f'Tag "{tag_name}" already exists.')

            if tag_name in existing_tags:
                existing_tags = existing_tags.exclude(name=tag_name)

        Tag.objects.filter(name__in=existing_tags).delete()

        self.stdout.write(self.style.SUCCESS('Tag seeding completed successfully.'))