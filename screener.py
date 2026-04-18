import logging
from yahooquery import Screener
import requests

log = logging.getLogger(__name__)


def get_most_active(count=100):
    try:
        s = Screener()
        data = s.get_screeners('most_actives', count=count)
        quotes = data['most_actives']['quotes']
        return [q['symbol'] for q in quotes]
    except Exception as e:
        log.warning(f"Primary screener failed ({e}); using fallback.")
        return _fallback_most_active(count)


def _fallback_most_active(count):
    url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
    params = {"scrIds": "most_actives", "count": count}
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    result = resp.json()
    try:
        return [q['symbol'] for q in result['finance']['result'][0]['quotes']]
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"Fallback screener returned unexpected structure: {e}") from e
