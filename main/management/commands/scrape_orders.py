import logging

from django.core.management import BaseCommand

from godsunchained.settings import BASE_DIR
from main.constants import ORDER_STATUS_ACTIVE, ORDER_STATUS_FILLED
from main.scrape_immutable import scrape_orders

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Scrape mode'

    def add_arguments(self, parser):
        parser.add_argument(
            '--complete', default=False, action='store_true',
            help='Force to do complete scrape')

    def handle(self, *args, **options):
        logger.info('Started scraping orders')
        scrape_orders(complete=options['complete'])
        logger.info('Finished scraping orders')
