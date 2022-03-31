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


class RatioView(TemplateView):
    template_name = 'main/ratio.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        protos = Proto.objects.filter(
            qty_on_sale__gt=1, ratio_price__lt=0.9
        ).order_by('ratio_price').all()
        kwargs['protos'] = [
            p for p in protos
            if p.histories.last()
               and (p.current_price < p.histories.last().last_price
                    or p.current_price < p.histories.last().prc7)
               and (p.runner_price < p.histories.last().prc7
                    or p.runner_price < p.histories.last().prc14)
               and p.histories.last().vol7 > 0]
        return kwargs


class BargainView(TemplateView):
    template_name = 'main/bargain.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        protos = Proto.objects.filter(qty_on_sale__gte=1).all()
        data = []
        for proto in protos:
            if proto.histories.last() and proto.histories.last().vol7 > 2 and proto.histories.last().vol60 > 10:
                proto.ratio_bargain = proto.current_price / proto.histories.last().prc14
                data.append(proto)
        data.sort(key=lambda x: x.ratio_bargain)
        kwargs['protos'] = [d for d in data if d.ratio_bargain < 0.8]
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
