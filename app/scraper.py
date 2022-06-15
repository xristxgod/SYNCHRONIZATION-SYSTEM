from src.models import AccountModel
from src.inc.schemas import RequestPrivateData
from src.inc.controller import request_controller


class Account:
    """Account"""
    def __init__(self, api_name: str, user_id: int):
        self.api_name = api_name
        self.user_id = user_id

    def get_data(self):
        pass



def scrape(api_name: str, user_id: int):
    up_to_date = False
    weight_used, sleeps, processed, updated_positions, new_positions, updated_orders = 0, 0, 0, 0, 0, 0

    if weight_used < 1000:
        response_headers, response_data = await request_controller.private(data=RequestPrivateData(
            apiData=()
        ))
