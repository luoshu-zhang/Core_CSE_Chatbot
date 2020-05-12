import requests
# import json
from datetime import date
import ast


def get_entities(user_response):
    # Set the headers
    headers = {
        'Authorization': 'Bearer PAS26APID43B65U32KXQF3JXGX7P7JTE',
    }

    # Set the params
    today = date.today()
    d = today.strftime("%Y%m%d")
    params = (
        ('v', d),
        ('q', user_response),
    )

    # Generate response
    response = requests.get('https://api.wit.ai/message', headers=headers, params=params)
    entity_dict = ast.literal_eval(response.text)
    return entity_dict
