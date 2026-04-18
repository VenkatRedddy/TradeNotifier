import requests
from requests_oauthlib import OAuth1
from config import (TWITTER_API_KEY, TWITTER_API_SECRET,
                    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET,
                    RSI_OVERSOLD, RSI_OVERBOUGHT)

auth = OAuth1(TWITTER_API_KEY, TWITTER_API_SECRET,
              TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)


def upload_image(image_path):
    url = "https://upload.twitter.com/1.1/media/upload.json"
    with open(image_path, 'rb') as f:
        resp = requests.post(url, auth=auth, files={"media": f})
    resp.raise_for_status()
    return resp.json()['media_id_string']


def post_tweet(text, media_id):
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": text, "media": {"media_ids": [media_id]}}
    resp = requests.post(url, auth=auth, json=payload)
    resp.raise_for_status()
    return resp.json()


def notify(ticker, signal, strength, price, rsi, ema9, ema21, image_path):
    emoji_map = {
        'STRONG_BUY':  '🔥🟢',
        'BUY':         '🟢',
        'STRONG_SELL': '🔥🔴',
        'SELL':        '🔴',
    }
    emoji = emoji_map.get(strength, '⚪')
    rsi_tag = ""
    if rsi < RSI_OVERSOLD:
        rsi_tag = "📉 RSI Oversold!"
    elif rsi > RSI_OVERBOUGHT:
        rsi_tag = "📈 RSI Overbought!"
    text = (
        f"{emoji} ${ticker} WEEKLY {signal} SIGNAL\n\n"
        f"💰 Price: ${price:.2f}\n"
        f"📊 EMA9: ${ema9:.2f} | EMA21: ${ema21:.2f}\n"
        f"📈 RSI(14): {rsi:.1f} {rsi_tag}\n\n"
        f"⏰ Weekly timeframe\n"
        f"#trading #stocks #{ticker} #SwingTrade"
    )
    media_id = upload_image(image_path)
    return post_tweet(text, media_id)
