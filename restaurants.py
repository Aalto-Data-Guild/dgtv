import dataclasses
import datetime
from typing import Dict, List, Optional
from jinja2 import Template

import requests
import streamlit as st

KANTTIINIT_URL_MASK = "https://kitchen.kanttiinit.fi/menus?lang=en&restaurants={}&days={}"
RESTAURANT_IDS = [2, 3]
RESTAURANT_NAMES = {2: "CS", 3: "Täffä"}


@dataclasses.dataclass
class RestaurantResponse:
    @dataclasses.dataclass
    class MenuItem:
        title: str
        properties: Dict[int, str]

    id: int
    name: str
    dates: Dict[str, Optional[List[MenuItem]]]


def get_restaurants(date: datetime.date) -> List[RestaurantResponse]:
    date_str = date.strftime("%Y-%m-%d")
    restaurant_ids_str = ','.join(str(rid) for rid in RESTAURANT_IDS)

    response = requests.get(KANTTIINIT_URL_MASK.format(restaurant_ids_str, date_str))
    return [RestaurantResponse(int(id), RESTAURANT_NAMES.get(int(id), "Place"), restaurant_json) for (id, restaurant_json) in
            response.json().items()]


def widget():
    st.markdown('**Menu:**')
    today_date = datetime.datetime.today().date()
    today_str = today_date.strftime("%Y-%m-%d")
    with open("restaurants.html", "r") as f:
        template = Template(f.read())

    for restaurant in get_restaurants(today_date):
        st.markdown(f"#### :green[{restaurant.name}]")
        items = restaurant.dates.get(today_str)
        if not items:
            st.markdown("No menu available :cry:")
            continue
        menu = template.render(menu=items)
        st.markdown(menu, unsafe_allow_html=True)
