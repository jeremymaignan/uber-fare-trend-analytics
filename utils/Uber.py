from utils.ConfManager import get_conf

from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from termcolor import colored
from time import sleep, strftime
from datetime import datetime

class Uber():
    def __init__(self):
        self.token = get_conf("uber_app_id")

    def get_estimation(self, from_, to, seat_count):
        session = Session(server_token=self.token)
        client = UberRidesClient(session)
        response = client.get_price_estimates(
            start_latitude= from_["lat"],
            start_longitude= from_["long"],
            end_latitude= to["lat"],
            end_longitude= to["long"],
            seat_count=seat_count
        )
        estimations = {
            "request_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "modes": {}
        }
        response = response.json.get('prices')
        for mode in response:
            estimations["modes"][mode["localized_display_name"]] = {
                "prices": {
                    "low": int(mode["low_estimate"]),
                    "high": int(mode["high_estimate"])
                },
                "ride_information": {
                    "distance": mode["distance"],
                    "duration": mode["duration"]
                },
                "top": {},
                "fluctuations": {
                    "dynamic": {
                        "trends": "=",
                        "value": 0
                    },
                    "global": {
                        "trends": "=",
                        "value": 0
                    }
                }
            }
        return estimations


# if "surge_multiplier" in mode.keys():
#         print(colored(mode["surge_multiplier"], 'red'))
            