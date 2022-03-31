# import pickle
# from collections import Counter
# from datetime import datetime
# from typing import List
#
# import requests
# from django.db import OperationalError
# from django.db.models import Max
# from retry import retry
# import logging
#
# from godsunchained.settings import ORDER_CURSOR
# from main.constants import BUY_TOKEN_ADDRESS, BUY_TOKEN_TYPE, ORDER_STATUS_FILLED, \
#     SELL_TOKEN_ADDRESS, \
#     SELL_TOKEN_TYPE, TS_RELEASE_DATE
# from main.models import Asset, Card, Match, Mode, Order, Person, Player, Proto
#
# logger = logging.getLogger(__name__)
#
#
# class ScrapeError(Exception):
#     """Base exception error."""
#
#
# class OrdersScrapeError(Exception):
#     """Orders exception error."""
#
#
# class TokenTypeOrdersScrapeError(Exception):
#     """Token type orders exception error."""
#
#
# class CardTypeOrdersScrapeError(Exception):
#     """Card type orders exception error."""
#
#
# class CursorOrdersScrapeError(Exception):
#     """Cursor orders exception error."""
#
#
# # @retry((HTT,), delay=3, jitter=3, max_delay=30)
# def fetch_mode() -> dict:
#     logger.info('Fetching modes...')
#     res = requests.get('https://api.godsunchained.com/v0/mode')
#     res.raise_for_status()
#     return res.json()
#
#
# @retry((OperationalError,), delay=5, jitter=1, max_delay=60, tries=10)
# def save_modes(data):
#     for item in data:
#         mode = Mode.objects.update_or_create(
#             id=item['id'],
#             defaults={
#                 'name': item['name'],
#                 'description': item['description'],
#                 'live': item['live'],
#                 'active': item['active'],
#                 'required_level': item['required_level'],
#                 'properties': item['properties'],
#             }
#         )
#         logger.info(f'Saved {mode}')
#
#
# def scrape_mode():
#     data = fetch_mode()
#     save_modes(data)
#
#
# def get_next_match_ts():
#     last_start = Match.objects.all().aggregate(Max('ts_start'))['ts_start__max']
#     if last_start:
#         return last_start
#     # otherwise default is the launch date of the game
#     return TS_RELEASE_DATE
#
#
# # @retry((HTT,), delay=3, jitter=3, max_delay=30)
# def fetch_match(ts_start: int) -> dict:
#     ts_end = ts_start + (60 * 30)
#     logger.info(f'Fetching matches from {ts_start} ({datetime.fromtimestamp(ts_start)})...')
#     res = requests.get('https://api.godsunchained.com/v0/match', params={'start_at': ts_start})  #, 'end_at': ts_end})
#     res.raise_for_status()
#     data = res.json()
#     return data
#
#
# @retry((OperationalError,), delay=5, jitter=1, max_delay=60, tries=10)
# def get_card(card_id: int) -> Card:
#     try:
#         card = Card.objects.get(pk=card_id)
#     except Card.DoesNotExist:
#         res = requests.get(f'https://api.godsunchained.com/v0/proto/{card_id}')
#         res.raise_for_status()
#         data = res.json()
#         card = Card.objects.create(
#             pk=data['id'],
#             name=data['name'],
#             effect=data['effect'],
#             god=data['god'],
#             rarity=data['rarity'],
#             tribe=data['tribe']['String'],
#             tribe_valid=data['tribe']['Valid'],
#             mana=data['mana'],
#             attack=data['attack']['Int64'],
#             attack_valid=data['attack']['Valid'],
#             health=data['health']['Int64'],
#             health_valid=data['health']['Valid'],
#             type=data['type'],
#             set=data['set'],
#             collectable=data['collectable'],
#             live=(False if data['live'] == 'false' else True),
#             art=data['art_id'],
#             lib=data['lib_id'],
#         )
#         logger.info(f'Created {card}')
#     return card
#
#
# @retry((OperationalError,), delay=5, jitter=1, max_delay=60, tries=10)
# def save_player(data, person_id: int) -> Player:
#     for i in range(2):
#         if data['player_info'][i]['user_id'] == person_id:
#             item = data['player_info'][i]
#     person = Person.objects.get_or_create(item['user_id'])
#     cards = [get_card(cid) for cid in item['cards']]
#     god_power = get_card(item['god_power'])
#     player = Player.objects.create(
#         person=person,
#         status=item['status'],
#         health=item['health'],
#         god=item['god'],
#         god_power=god_power,
#         cards=cards
#     )
#     logger.info(f'Created {player}')
#     return player
#
#
# @retry((OperationalError,), delay=5, jitter=1, max_delay=60, tries=10)
# def save_matches(data):
#     for item in data:
#         winner = save_player(item, item['player_won'])
#         loser = save_player(item, item['player_lost'])
#         mode = Mode.objects.get(pk=item['game_mode'])
#         match = Match.objects.update_or_create(
#             id=item['game_id'],
#             mode=mode,
#             winner=winner,
#             loser=loser,
#             played_at=datetime.fromtimestamp(item['start_time']),
#             ts_start=item['start_time'],
#             ts_end=item['end_time'],
#             total_turns=item['total_turns'],
#             total_rounds=item['total_rounds'],
#         )
#         logger.info(f'Saved {match}')
#
#
# def scrape_match():
#     ts = get_next_match_ts()
#     data = fetch_match(ts)
#     save_matches(data)
#
#
# # @retry((HTT,), delay=3, jitter=3, max_delay=30)
# def fetch_orders(params: dict) -> dict:
#     logger.info('Fetching orders...')
#     res = requests.get(f'https://api.x.immutable.com/v1/orders', params=params)
#     res.raise_for_status()
#     data = res.json()
#     for item in data['result']:
#         if item['sell']['type'] != SELL_TOKEN_TYPE or item['buy']['type'] != BUY_TOKEN_TYPE:
#             raise TokenTypeOrdersScrapeError(item)
#     return data
#
#
# def upsert_proto(metadata: dict) -> Proto:
#     if metadata['type'] != 'card':
#         raise CardTypeOrdersScrapeError(metadata)
#     defaults = {
#         'name': metadata['name'],
#         'effect': metadata['effect'],
#         'god': metadata['god'],
#         'set': metadata['set'],
#         'mana': metadata['mana'],
#         'type': metadata['type'],
#         'img': metadata['image'],
#         'tribe': metadata['tribe'],
#         'attack': metadata['attack'],
#         'health': metadata['health'],
#         'rarity': metadata['rarity'],
#     }
#     proto, created = Proto.objects.update_or_create(
#         id=metadata['proto'],
#         defaults=defaults,
#     )
#     if created:
#         logger.info(f'Created {proto}')
#     return proto
#
#
# # @retry((HTT,), delay=3, jitter=3, max_delay=30)
# def fetch_asset(item: dict) -> dict:
#     sell_token_address = item['sell']['data']['token_address']
#     token_id = item['sell']['data']['token_id']
#     res = requests.get(f'https://api.x.immutable.com/v1/assets/{sell_token_address}/{token_id}')
#     res.raise_for_status()
#     return res.json()
#
#
# def upsert_asset(item: dict) -> Asset:
#     asset_info = fetch_asset(item)
#     proto = upsert_proto(asset_info['metadata'])
#     defaults = {
#         'proto': proto,
#         'token_address': item['token_address'],
#         'token_id': item['token_id'],
#         'user': item['user'],
#         'status': item['status'],
#         'quality': item['metadata']['quality'],
#         'created_at': item['created_at'].rstrip('Z'),
#         'updated_at': item['updated_at'].rstrip('Z'),
#     }
#     asset, created = Asset.objects.update_or_create(
#         id=item['id'],
#         defaults=defaults,
#     )
#     if created:
#         logger.info(f'Created {asset}')
#     return asset
#
#
# @retry((OperationalError,), delay=5, jitter=1, max_delay=60, tries=10)
# def upsert_order(item: dict) -> bool:
#     asset = upsert_asset(item)
#     defaults = {
#         'asset': asset,
#
#         'status': item['status'],
#         'user': item['user'],
#         'quantity': item['amount_sold'],
#         'cost': int(item['buy']['data']['quantity']) / int(item['buy']['data']['decimals']),
#
#         'sell_id': item['sell']['data']['id'],
#         'sell_type': item['sell']['type'],
#         'sell_token_address': item['sell']['data']['token_address'],
#         'sell_token_id': item['sell']['data']['token_id'],
#
#         'buy_type': item['buy']['type'],
#         'buy_token_address': item['buy']['data']['token_address'] or None,
#
#         'expires_at': item['expiration_timestamp'].rstrip('Z'),
#         'created_at': item['timestamp'].rstrip('Z'),
#         'updated_at': item['updated_timestamp'].rstrip('Z'),
#     }
#     order, created = Order.objects.update_or_create(
#         id=item['order_id'],
#         defaults=defaults,
#     )
#     logger.info(f'Saved {order}')
#     return created
#
#
# def scrape_orders(status):
#     try:
#         with open(ORDER_CURSOR, 'rb') as fh:
#             params = pickle.load(fh)
#         if not params:
#             raise CursorOrdersScrapeError('Empty cursor')
#     except (FileNotFoundError, EOFError, CursorOrdersScrapeError):
#         params = {
#             'sell_token_address': SELL_TOKEN_ADDRESS,
#             'buy_token_address': BUY_TOKEN_ADDRESS,
#             'status': status,
#         }
#     while True:
#         data = fetch_orders(params)
#         created_count = 0
#         for item in data['result']:
#             created = upsert_order(item)
#             created_count += int(created)
#         if not created_count:
#             logger.info(f'No new items in data! Clearing cursor...')
#             with open(ORDER_CURSOR, 'wb') as fh:
#                 pickle.dump(dict(), fh)
#             return
#         if 'cursor' not in data:
#             raise ValueError('Expected cursor')
#         params = {'cursor': data['cursor']}
#         with open(ORDER_CURSOR, 'wb') as fh:
#             pickle.dump(params, fh)
