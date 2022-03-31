import logging

from django.core.management import BaseCommand
from django.db.models import F, Max, Q

from godsunchained.settings import BASE_DIR
from main.constants import ORDER_STATUS_ACTIVE, ORDER_STATUS_FILLED
from main.models import Proto
from main.scrape_immutable import scrape_orders
from main.stats import build_day_stats

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Build stats'

    def add_arguments(self, parser):
        parser.add_argument(
            '--complete', default=False, action='store_true',
            help='Force to do complete scrape')

    def handle(self, *args, **options):
        logger.info(f'Started building stats')

        if options['complete']:
            Proto.objects.update(stats_at=None)

        # process all new protos
        logger.info('Processing new protos...')
        protos = Proto.objects.filter(stats_at=None).all()
        for proto in protos:
            build_day_stats(proto)

        # process all updated orders
        logger.info('Processing updated protos...')
        protos = Proto.objects.annotate(
            last_order=Max('assets__orders__updated_at')).filter(
            Q(stats_at__isnull=False) &
            Q(last_order__gt=F('stats_at')))
        for proto in protos:
            build_day_stats(proto)

        logger.info(f'Finished building stats')
