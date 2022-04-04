from operator import itemgetter

import pandas as pd
import plotly.express as px
from django.db.models import Count, F, OuterRef, Subquery
from django.db.models.functions import TruncDay
from django.views.generic import TemplateView

from main.constants import ORDER_STATUS_ACTIVE, ORDER_STATUS_FILLED
from main.models import History, Order, Proto
from django.core.cache import cache


class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['filled_count'] = Order.objects.filter(status=ORDER_STATUS_FILLED).count()
        kwargs['active_count'] = Order.objects.filter(status=ORDER_STATUS_ACTIVE).count()

        if not (graphs := cache.get('graphs')):
            filled_day_data = Order.objects.filter(status=ORDER_STATUS_FILLED).annotate(
                day=TruncDay('updated_at')).order_by('day').values('day').annotate(
                cnt=Count('day')).values('day', 'cnt')
            filled_day_df = pd.DataFrame([
                {'Day': d['day'], 'Count': d['cnt']}
                for d in filled_day_data])
            filled_day_fig = px.bar(filled_day_df, x='Day', y='Count', title='Orders filled per day')
            filled_by_day_graph = filled_day_fig.to_html(full_html=False)

            active_day_data = Order.objects.filter(status=ORDER_STATUS_ACTIVE).annotate(
                day=TruncDay('updated_at')).order_by('day').values('day').annotate(
                cnt=Count('day')).values('day', 'cnt')
            active_day_df = pd.DataFrame([
                {'Day': d['day'], 'Count': d['cnt']}
                for d in active_day_data])
            active_day_fig = px.bar(active_day_df, x='Day', y='Count', title='Orders active per day')
            active_by_day_graph = active_day_fig.to_html(full_html=False)

            graphs = {
                'filled_by_day_graph': filled_by_day_graph,
                'active_by_day_graph': active_by_day_graph,
            }
            cache.set('graphs', graphs)
        kwargs |= graphs

        return kwargs


class CardsView(TemplateView):
    template_name = 'main/cards.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['protos'] = Proto.objects.all()

        return kwargs


class CardView(TemplateView):
    template_name = 'main/card.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['proto'] = Proto.objects.get(pk=kwargs.pop('pk'))
        return kwargs


class BargainView(TemplateView):
    template_name = 'main/bargain.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        protos = Proto.objects.filter(qty_on_sale__gte=1).all()
        data = []
        for proto in protos:
            if his := proto.histories.last():
                if his.vol7 < 1 or his.vol14 < 2 or his.vol30 < 4 or his.vol60 < 8:
                    continue
                vs_last = his.last_price - proto.current_price
                vs_7day = his.prc7 - proto.current_price
                proto.bargain = min([vs_last, vs_7day])
                data.append(proto)
        data.sort(key=lambda x: x.bargain, reverse=True)
        # kwargs['protos'] = [d for d in data if d.ratio_bargain < 0.8]
        kwargs['protos'] = data[:20]
        return kwargs


class FiresaleView(TemplateView):
    template_name = 'main/firesale.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        protos = Proto.objects.all()
        data = []
        for proto in protos:
            his = proto.histories.last()
            if his and his.last_price < his.prc7 \
                    and his.prc7 < his.prc14 \
                    and his.prc14 < his.prc30 \
                    and his.prc30 < his.prc60:
                proto.ratio_firesale = proto.current_price / his.prc60
                data.append(proto)
        data.sort(key=lambda x: x.ratio_firesale)
        kwargs['protos'] = data[:20]
        return kwargs
