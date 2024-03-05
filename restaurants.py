import dataclasses
import datetime
from typing import Dict, List

import requests
import streamlit as st

KANTTIINIT_URL_MASK = "https://kitchen.kanttiinit.fi/menus?lang=fi&restaurants={}&days={}"
RESTAURANT_IDS = [2, 3]


@dataclasses.dataclass
class RestaurantResponse:
    @dataclasses.dataclass
    class MenuItem:
        title: str
        properties: Dict[int, str]

    id: int
    dates: Dict[str, List[MenuItem]]


def get_restaurants(date: datetime.date) -> List[RestaurantResponse]:
    date_str = date.strftime("%Y-%m-%d")
    restaurant_ids_str = ','.join(str(rid) for rid in RESTAURANT_IDS)
    response = requests.get(KANTTIINIT_URL_MASK.format(restaurant_ids_str, date_str))
    return [RestaurantResponse(id, restaurant_json) for (id, restaurant_json) in response.json().items()]


def widget():
    st.text('restaurants')
    today_date = datetime.datetime.today().date()
    today_str = today_date.strftime("%Y-%m-%d")
    for restaurant in get_restaurants(today_date):
        st.text(restaurant.id)
        items = restaurant.dates.get(today_str)
        st.table(items)
