import dataclasses
import datetime
from typing import Dict, List, Optional
from jinja2 import Template

import requests
import streamlit as st
from widgets.base_widget import BaseWidget

KANTTIINIT_URL_MASK = "https://kitchen.kanttiinit.fi/menus?lang=en&restaurants={}&days={}"
RESTAURANT_IDS = [2, 3, 5]
RESTAURANT_NAMES = {2: "CS", 3: "Täffä", 5: "TUAS"}


@dataclasses.dataclass
class RestaurantResponse:
    @dataclasses.dataclass
    class MenuItem:
        title: str
        properties: Dict[int, str]

    id: int
    name: str
    dates: Dict[str, Optional[List[MenuItem]]]


@st.cache_data
def get_restaurants(date: datetime.date) -> List[RestaurantResponse]:
    date_str = date.strftime("%Y-%m-%d")
    restaurant_ids_str = ','.join(str(rid) for rid in RESTAURANT_IDS)

    response = requests.get(KANTTIINIT_URL_MASK.format(restaurant_ids_str, date_str))
    return [RestaurantResponse(int(id), RESTAURANT_NAMES.get(int(id), "Place"), restaurant_json) for
            (id, restaurant_json) in response.json().items()]


class RestaurantsWidget(BaseWidget):
    name = 'Restaurants'

    def render(self):
        st.markdown("# Restaurants")

        today_date = datetime.datetime.today().date()
        today_str = today_date.strftime("%Y-%m-%d")
        with open("widgets/restaurants.html", "r") as f:
            template = Template(f.read())
        
        closed = []

        for restaurant in get_restaurants(today_date):
            items = restaurant.dates.get(today_str)
            if not items:
                closed.append(restaurant)
                continue

            if not items:
                st.markdown(f"{restaurant.name}: No menu available :cry:")
                continue
            else:
                menu = template.render(menu=items, restaurant=restaurant.name)
            st.html(menu)
        
        if closed:
            st.markdown("#### :red[Closed]")
            st.markdown(", ".join(restaurant.name for restaurant in closed))
