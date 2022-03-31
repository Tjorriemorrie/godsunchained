import logging
import pickle
from datetime import datetime
from time import sleep

import requests
from django.db import OperationalError
from django.utils.timezone import make_aware
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout, SSLError
from retry import retry

from godsunchained.settings import BASE_DIR
from main.constants import BUY_TOKEN_TYPE_ERC20, BUY_TOKEN_TYPE_ETH, CURRENCY_GOG, CURRENCY_IMX, \
    SELL_TOKEN_ADDRESS, SELL_TOKEN_TYPE_ERC721, TOKEN_CURRENCIES
from main.models import Asset, Order, Proto

logger = logging.getLogger(__name__)


class ScrapeError(Exception):
    """Base exception error."""


class RateLimitScrapeError(Exception):
    """Rate limited exception error."""


class OrdersScrapeError(Exception):
    """Orders exception error."""


class TokenTypeOrdersScrapeError(Exception):
    """Token type orders exception error."""


class DataOrdersScrapeError(Exception):
    """Data orders exception error."""


class CardTypeOrdersScrapeError(Exception):
    """Card type orders exception error."""


class CostingOrdersScrapeError(Exception):
    """Card type orders exception error."""


class PricingOrdersScrapeError(Exception):
    """Card type orders exception error."""


class CursorOrdersScrapeError(Exception):
    """Cursor orders exception error."""


sleep_time = 0
last_url = None


@retry((RateLimitScrapeError, ConnectionError, ReadTimeout, HTTPError), tries=9, delay=5, jitter=1, max_delay=60)
def get(url: str, params: dict = None) -> dict:
    global sleep_time
    global last_url
    if last_url == url:
        sleep_time = round(sleep_time + 0.5, 3)
        logger.info(f'Increased sleep time to {sleep_time}')
    elif sleep_time:
        sleep_time = round(sleep_time - 0.005, 3)
    last_url = url
    sleep(sleep_time)

    try:
        res = requests.get(url, params=params)
    except SSLError as exc:
        logger.warning(f'Connection error over ssl...?')
        raise RateLimitScrapeError()
    res.raise_for_status()
    return res.json()


def upsert_proto(metadata: dict) -> Proto:
    if metadata['type'] != 'card':
        raise CardTypeOrdersScrapeError(metadata)
    defaults = {
        'name': metadata['name'],
        'effect': metadata.get('effect'),
        'god': metadata['god'],
        'set': metadata['set'],
        'rarity': metadata['rarity'],
        'mana': metadata['mana'],
        'type': metadata['type'],
        'img': metadata['image'],
        'tribe': metadata.get('tribe'),
        'attack': metadata.get('attack'),
        'health': metadata.get('health'),
    }
    proto, created = Proto.objects.update_or_create(
        id=metadata['proto'],
        defaults=defaults,
    )
    if created:
        logger.info(f'Created {proto}')
    return proto


# @retry((HTT,), delay=3, jitter=3, max_delay=30)
def fetch_asset(item: dict) -> dict:
    sell_token_address = item['sell']['data']['token_address']
    token_id = item['sell']['data']['token_id']
    data = get(f'https://api.x.immutable.com/v1/assets/{sell_token_address}/{token_id}')
    return data


def upsert_asset(item: dict) -> Asset:
    asset_info = fetch_asset(item)
    proto = upsert_proto(asset_info['metadata'])
    defaults = {
        'proto': proto,
        'token_address': asset_info['token_address'],
        'token_id': asset_info['token_id'],
        'user': asset_info['user'],
        'status': asset_info['status'],
        'quality': asset_info['metadata']['quality'],
        'created_at': make_aware(datetime.fromisoformat(asset_info['created_at'][:19])),
        'updated_at': make_aware(datetime.fromisoformat(asset_info['updated_at'][:19])),
    }
    asset, created = Asset.objects.update_or_create(
        id=asset_info['id'],
        defaults=defaults,
    )
    if created:
        logger.info(f'Created {asset}')
    return asset


def fetch_orders(params: dict) -> dict:
    logger.info('Fetching orders...')
    data = get(f'https://api.x.immutable.com/v1/orders', params)
    if not data['result']:
        raise DataOrdersScrapeError(f'No data! {data}')
    return data


ticker_prices = {
    CURRENCY_IMX: 2.64,  # 29 mar
    CURRENCY_GOG: 0.48,  # 30 mar
}


def add_ticker_price(costing: dict) -> dict:
    global ticker_prices
    if costing['currency'] in ticker_prices:
        ticker_price = ticker_prices[costing['currency']]
    else:
        params = {
            'key': '2b41baa6d12b78e58f8555b1b61820c9b87e79fd',
            'ids': costing['currency'],
            'interval': '1d',
            'convert': 'USD',
            'status': 'active',
        }
        ticker = get('https://api.nomics.com/v1/currencies/ticker', params)
        try:
            ticker_price =  float(ticker[0]['price'])
        except Exception as exc:
            raise PricingOrdersScrapeError(f'No price for {costing["currency"]}')
        ticker_prices[costing['currency']] = ticker_price
    costing['usd'] = costing['cost'] / ticker_price
    return costing


def get_costing(item: dict) -> dict:
    if item['buy']['type'] == BUY_TOKEN_TYPE_ETH:
        currency = BUY_TOKEN_TYPE_ETH
    elif item['buy']['type'] == BUY_TOKEN_TYPE_ERC20:
        currency = TOKEN_CURRENCIES[item['buy']['data']['token_address']]
    else:
        raise CostingOrdersScrapeError(f'Unknown sell token type: {item["buy"]["type"]}')
    costing = {
        'cost': int(item['buy']['data']['quantity']) / (10 ** int(item['buy']['data']['decimals'])),
        'currency': currency,
    }
    costing = add_ticker_price(costing)
    return costing


@retry((OperationalError,), delay=5, jitter=1, max_delay=60, tries=10)
def upsert_order(item: dict) -> bool:
    asset = upsert_asset(item)
    costing = get_costing(item)
    defaults = {
        'asset': asset,

        'status': item['status'],
        'user': item['user'],
        'quantity': item['amount_sold'],
        'cost': costing['cost'],
        'currency': costing['currency'],
        'usd': costing['usd'],

        'sell_id': item['sell']['data']['id'],
        'sell_type': item['sell']['type'],
        'sell_token_address': item['sell']['data']['token_address'],
        'sell_token_id': item['sell']['data']['token_id'],

        'buy_type': item['buy']['type'],
        'buy_token_address': item['buy']['data']['token_address'] or None,

        'expires_at': make_aware(datetime.fromisoformat(item['expiration_timestamp'][:19])),
        'created_at': make_aware(datetime.fromisoformat(item['timestamp'][:19])),
        'updated_at': make_aware(datetime.fromisoformat(item['updated_timestamp'][:19])),
    }
    order, created = Order.objects.update_or_create(
        id=item['order_id'],
        defaults=defaults,
    )
    logger.info(f'Saved {order}')
    return created


def clear_cursor(f):
    logger.info(f'No new items in data! Clearing cursor...')
    with open(f, 'wb') as fh:
        pickle.dump(dict(), fh)


def scrape_orders(status, complete=False):
    file_name = complete and 'complete' or 'recent'
    file_path = BASE_DIR / f'{file_name}_{status}.pkl'
    try:
        with open(file_path, 'rb') as fh:
            params = pickle.load(fh)
        if not params:
            raise CursorOrdersScrapeError('Empty cursor')
    except (FileNotFoundError, EOFError, CursorOrdersScrapeError):
        params = {
            'sell_token_address': SELL_TOKEN_ADDRESS,
            'sell_token_type': SELL_TOKEN_TYPE_ERC721,
            'status': status,
        }
    page = 0
    while True:
        page += 1
        try:
            data = fetch_orders(params)
        except DataOrdersScrapeError:
            return clear_cursor(file_path)

        created_count = 0
        for item in data['result']:
            created = upsert_order(item)
            created_count += int(created)
        if not complete and not created_count:
            return clear_cursor(file_path)

        if 'cursor' not in data:
            logger.info('No cursor returned.')
            return clear_cursor(file_path)
        params['cursor'] = data['cursor']
        with open(file_path, 'wb') as fh:
            pickle.dump(params, fh)
