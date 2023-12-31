import time

import openapi_client
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://0.0.0.0:8500"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    item_id = 56
    telegram_chat_data = openapi_client.TelegramChatData(chat_id =1, token = "test", ip_address ="127.0.0.1", tool= "ping")
    integer =0

    try:
        # Add Telegram
        api_response = api_instance.add_telegram_add_telegram_post(telegram_chat_data)
        print("The response of DefaultApi->add_telegram_add_telegram_add_post:\n")
        integer= int(api_response["id"] )
        pprint(integer)
    except Exception as e:
        print("Exception when calling DefaultApi->add_telegram_add_telegram_add_post: %s\n" % e)

    time.sleep(10)

    try:
        # Del Telegram
        api_response = api_instance.del_telegram_del_telegram_post(integer)
        pprint(api_response)

    except Exception as e:
        print("Exception when calling DefaultApi->add_telegram_add_telegram_add_post: %s\n" % e)

