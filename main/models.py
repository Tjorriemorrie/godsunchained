from django.db import models

from main.constants import ORDER_STATUS_ACTIVE, ORDER_STATUS_FILLED
from main.managers import OrderManager, ProtoManager


class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# class Mode(Timestamped):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=250)
#     live = models.BooleanField()
#     active = models.BooleanField()
#     required_level = models.IntegerField()
#     properties = models.JSONField()
#
#     def __str__(self) -> str:
#         return f'<Mode {self.pk} {self.name}>'
#
#
# class Person(Timestamped):
#     name = models.CharField(max_length=100)
#     xp_level = models.IntegerField(null=True)
#     total_xp = models.IntegerField(null=True)
#     xp_to_next = models.IntegerField(null=True)
#     won_matches = models.IntegerField(null=True)
#     lost_matches = models.IntegerField(null=True)
#
#
# class Card(Timestamped):
#     name = models.CharField(max_length=250)
#     effect = models.CharField(max_length=250)
#     god = models.CharField(max_length=50)
#     rarity = models.CharField(max_length=50)
#     tribe = models.CharField(max_length=50)
#     tribe_valid = models.BooleanField()
#     mana = models.IntegerField()
#     attack = models.IntegerField()
#     attack_valid = models.BooleanField()
#     health = models.IntegerField()
#     health_valid = models.BooleanField()
#     type = models.CharField(max_length=50)
#     set = models.CharField(max_length=50)
#     collectable = models.BooleanField()
#     live = models.BooleanField()
#     art = models.CharField(max_length=50)
#     lib = models.CharField(max_length=50)
#
#     def __str__(self) -> str:
#         return f'<Card {self.name} {self.mana} {self.god} {self.type}>'
#
#
# class Player(Timestamped):
#     person = models.ForeignKey(Person, on_delete=models.PROTECT, related_name='players')
#     cards = models.ManyToManyField(Card, related_name='players')
#     status = models.CharField(max_length=50)
#     health = models.IntegerField()
#     god = models.CharField(max_length=50)
#     god_power = models.ForeignKey(Card, on_delete=models.PROTECT)
#     globaal = models.BooleanField()
#
#
# class Match(Timestamped):
#     id = models.CharField(max_length=250, primary_key=True)
#     mode = models.ForeignKey(Mode, on_delete=models.PROTECT, related_name='matches')
#     winner = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='matches_winner')
#     loser = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='matches_loser')
#     played_at = models.DateTimeField()
#     ts_start = models.PositiveBigIntegerField()
#     ts_end = models.PositiveBigIntegerField()
#     total_turns = models.IntegerField()
#     total_rounds = models.IntegerField()


############################################################################################
# immutable api
############################################################################################

# https://api.godsunchained.com/v0/proto/85
class Proto(models.Model):
    name = models.CharField(max_length=100)
    effect = models.CharField(max_length=500, null=True)
    god = models.CharField(max_length=20)
    set = models.CharField(max_length=20)
    rarity = models.CharField(max_length=20)
    mana = models.IntegerField()
    type = models.CharField(max_length=20)
    img = models.CharField(max_length=20)
    tribe = models.CharField(max_length=20, null=True)
    attack = models.IntegerField(null=True)
    health = models.IntegerField(null=True)

    # stats
    qty_on_sale = models.IntegerField(null=True)
    current_price = models.FloatField(null=True)
    runner_price = models.FloatField(null=True)
    last_price = models.FloatField(null=True)
    stats_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f'<Proto {self.pk} {self.name} {self.god} {self.rarity}>'

    def active_orders(self):
        return Order.objects.filter(
            asset__proto_id=self.pk, status=ORDER_STATUS_ACTIVE
        ).order_by('usd').all()

    def filled_orders(self):
        return Order.objects.filter(
            asset__proto_id=self.pk, status=ORDER_STATUS_FILLED
        ).order_by('-updated_at').all()


class Asset(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    proto = models.ForeignKey(Proto, on_delete=models.CASCADE, related_name='assets')
    token_address = models.CharField(max_length=200)
    token_id = models.BigIntegerField()
    user = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    quality = models.CharField(max_length=20)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        unique_together = ('token_address', 'token_id')

    def __str__(self) -> str:
        return f'<Asset {self.token_address} / {self.token_id}>'


# all data by sell token address https://api.x.immutable.com/v1/orders?sell_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c
# individual order is by order_id https://api.x.immutable.com/v1/orders/96605562
# detail url is https://market.immutable.com/assets/{sell_token_address}/{sell_token_id}
class Order(models.Model):
    objects = OrderManager()

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='orders')

    status = models.CharField(max_length=50)
    user = models.CharField(max_length=100)
    quantity = models.IntegerField(null=True)
    cost = models.FloatField(null=True)
    currency = models.CharField(max_length=20)
    usd = models.FloatField()

    # sell
    sell_id = models.CharField(max_length=200)
    sell_type = models.CharField(max_length=20)
    sell_token_address = models.CharField(max_length=200)
    sell_token_id = models.BigIntegerField()

    # buy
    buy_type = models.CharField(max_length=20)
    buy_token_address = models.CharField(max_length=200, null=True)

    expires_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    scraped_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ['-pk']

    def __str__(self) -> str:
        return f'<Order {self.pk} {self.status}>'


class Day(Timestamped):
    day = models.DateField(db_index=True)

    class Meta:
        ordering = ['day']

    def __str__(self) -> str:
        return f'{self.day:"%Y-%m-%d"}'


class History(Timestamped):
    proto = models.ForeignKey(Proto, on_delete=models.CASCADE, related_name='histories')
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='histories')

    last_price = models.FloatField()
    prc7 = models.FloatField()
    prc14 = models.FloatField()
    prc30 = models.FloatField()
    prc60 = models.FloatField()
    vol7 = models.IntegerField()
    vol14 = models.IntegerField()
    vol30 = models.IntegerField()
    vol60 = models.IntegerField()

    class Meta:
        ordering = ['day']
        unique_together = ('proto', 'day')
