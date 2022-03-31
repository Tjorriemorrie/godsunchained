import logging

from django.core.management import BaseCommand

from main.scrape_immutable import scrape_match

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Scrape match'

    def handle(self, *args, **options):
        logger.info('Started scraping match cmd')
        scrape_match()
        logger.info('Ended scraping match cmd')
