import os
import sys
from dotenv import load_dotenv
load_dotenv()

TWITTER_API_KEY        = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET     = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN   = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET  = os.getenv("TWITTER_ACCESS_SECRET")

_REQUIRED_TWITTER = {
    "TWITTER_API_KEY": TWITTER_API_KEY,
    "TWITTER_API_SECRET": TWITTER_API_SECRET,
    "TWITTER_ACCESS_TOKEN": TWITTER_ACCESS_TOKEN,
    "TWITTER_ACCESS_SECRET": TWITTER_ACCESS_SECRET,
}
_missing = [k for k, v in _REQUIRED_TWITTER.items() if not v]
if _missing:
    print(
        f"WARNING: Missing Twitter credentials: {', '.join(_missing)}. "
        "Notifications will fail. Set them in your .env file.",
        file=sys.stderr,
    )

EMA_FAST           = 9
EMA_SLOW           = 21
RSI_PERIOD         = 14
RSI_OVERSOLD       = 30
RSI_OVERBOUGHT     = 75

INTERVAL           = "1wk"
PERIOD             = "2y"
CHART_LOOKBACK     = 52

MOST_ACTIVE_COUNT  = 100
