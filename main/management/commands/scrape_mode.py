import logging

from django.core.management import BaseCommand

from main.scrape_immutable import scrape_mode

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Scrape mode'

    def handle(self, *args, **options):
        logger.info('Started scraping mode cmd')
        scrape_mode()
        logger.info('Ended scraping mode cmd')
