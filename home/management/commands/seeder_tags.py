from django.core.management import BaseCommand
from apps.common.models import Tag


class Command(BaseCommand):
    help = 'Generate tags'

    def handle(self, *args, **kwargs):
        tags = ['shoes', 'clothes', 'jeans', 'shirts']
        for tag in tags:
            Tag.objects.create(name=tag)
        
        self.stdout.write(self.style.SUCCESS('Tags created successfully.'))