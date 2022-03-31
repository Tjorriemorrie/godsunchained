import logging

import numpy as np
from django.utils.timezone import now
from scipy import stats

from main.constants import ORDER_STATUS_ACTIVE, ORDER_STATUS_FILLED
from main.models import Day, History, Order, Proto
import pandas as pd

logger = logging.getLogger(__name__)


def build_day_stats(proto: Proto):
    # clear existing daystats
    logger.debug(f'Cleared all daystats for {proto}')
    History.objects.filter(proto=proto).delete()

    # get last day stat as starting point
    orders = list(Order.objects.filter(
        status=ORDER_STATUS_FILLED, asset__proto=proto, asset__quality='Meteorite'
    ).order_by('updated_at').values())

    if orders:
        # load
        df = pd.DataFrame.from_records(orders, index='updated_at')
        df.index = pd.to_datetime(df.index).floor('D')

        # drop outliers
        q1 = df['cost'].quantile(0.25)
        q3 = df['cost'].quantile(0.75)
        iqr = q3 - q1
        upper_bound = q3 + 1.5 * iqr
        df_out = df[df['cost'] <= upper_bound]

        # aggregate
        df_res = df_out.resample('D')
        df_agg = df_res.agg({'quantity': 'sum', 'cost': 'mean'})
        ix = pd.date_range(start=df_agg.index.min(), end=pd.Timestamp.today(tz='UTC'), freq='D')
        df_agg = df_agg.reindex(ix)
        df_agg['quantity'].fillna(0, inplace=True)
        df_agg['vol7'] = df_agg['quantity'].rolling('7d', min_periods=1).sum()
        df_agg['vol14'] = df_agg['quantity'].rolling('14d', min_periods=1).sum()
        df_agg['vol30'] = df_agg['quantity'].rolling('30d', min_periods=1).sum()
        df_agg['vol60'] = df_agg['quantity'].rolling('60d', min_periods=1).sum()
        df_agg['cost'].fillna(method='ffill', inplace=True)
        df_agg['prc7'] = df_agg['cost'].rolling('7d', min_periods=1).mean()
        df_agg['prc14'] = df_agg['cost'].rolling('14d', min_periods=1).mean()
        df_agg['prc30'] = df_agg['cost'].rolling('30d', min_periods=1).mean()
        df_agg['prc60'] = df_agg['cost'].rolling('60d', min_periods=1).mean()
        for day_val, row in df_agg.iterrows():
            day, _ = Day.objects.get_or_create(day=day_val)
            history = History.objects.create(
                day=day,
                proto=proto,
                last_price=row['cost'],
                prc7=row['prc7'],
                prc14=row['prc14'],
                prc30=row['prc30'],
                prc60=row['prc60'],
                vol7=row['vol7'],
                vol14=row['vol14'],
                vol30=row['vol30'],
                vol60=row['vol60'],
            )

    orders = Order.objects.filter(
        asset__proto=proto, status=ORDER_STATUS_ACTIVE
    ).order_by('cost').all()
    proto.qty_on_sale = len(orders)
    if orders:
        proto.current_price = orders[0].cost
    if len(orders) > 1:
        proto.runner_price = orders[1].cost
        proto.ratio_price = proto.current_price / proto.runner_price
    proto.stats_at = now()
    proto.save()
    logger.info(f'Created histories for {proto}')
