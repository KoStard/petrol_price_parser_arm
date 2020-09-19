import requests
from bs4 import BeautifulSoup
import re
import json
from github import Github
from datetime import datetime
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


def generate_message(volume,
                     volume_uom,
                     price_currency,
                     price,
                     fuel_type,
                     provider):
    return {
        "volume": volume,
        "volume_uom": volume_uom,
        "price_currency": price_currency,
        "price": price,
        "type": fuel_type,
        "provider": provider,
        "date": datetime.now().date().isoformat()
    }


def handle_maxoil():
    response = requests.get("http://www.maxoil.am/", headers=headers).text
    selector = "body > div.wrapper > main > div.wrap > div.js-conveyor-example > ul > li > span > p"
    soup = BeautifulSoup(response, 'html.parser')
    items = soup.select(selector)
    volume_matcher = re.compile(r"(?P<volume>\d+)(?P<uom>\w+)")
    new_messages = []
    for item in items:
        item_text = item.get_text()
        name, price_label = [e.strip() for e in item_text.split("-")]
        volume_label, price, currency = price_label.split(" ")
        volume_match = volume_matcher.match(volume_label)
        volume_match_dict = volume_match.groupdict()
        volume = volume_match_dict['volume']
        uom = volume_match_dict['uom']
        message = generate_message(
            volume,
            uom,
            currency,
            price,
            name,
            "maxoil"
        )
        new_messages.append(message)
    return new_messages


handlers = [
    handle_maxoil
]


def execute_handlers():
    messages = []
    for handler in handlers:
        messages += handler()
    return messages


def handle_event(arg1=None, arg2=None):
    token = os.environ['TOKEN']
    messages = execute_handlers()
    serialized_messages = json.dumps(messages)
    g = Github(token)
    repo = g.get_repo("KoStard/petrol_price_history_arm")
    key = datetime.now().date().isoformat()
    # github.GithubException.GithubException -> if already present
    repo.create_file("history/{}.json".format(key), "Adding content for {}".format(key), serialized_messages)
    return serialized_messages
