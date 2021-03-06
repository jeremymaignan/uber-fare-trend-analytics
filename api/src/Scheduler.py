from datetime import datetime
from utils.Mongodb import Mongodb
from utils.ConfManager import get_conf

import logging
import grequests

def scheduler():
    mongo = Mongodb('rides')
    rides = list(mongo.get_pending_rides(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    logging.info("{} Rides found".format(len(rides)))
    async_list = []
    for ride in rides:
        logging.info(ride["_id"])
        action_item = grequests.get("{}/rides/{}?size=0&update=True&apps=*".format(get_conf("api_hostname"), ride["_id"])) #,  verify=False)
        async_list.append(action_item)
        #requests.get("http://0.0.0.0:5000/weleave/{}".format(ride["_id"]))
    grequests.map(async_list)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    scheduler()