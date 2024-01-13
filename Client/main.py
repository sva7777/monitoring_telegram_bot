import click
import logging
from sys import stdout
import openapi_client
from pprint import pprint

# ToDo: add param debug_level(all commands). Default debug. Make it enum.
# ToDO: can be mon_type be enum?


@click.command()
@click.option(
    "--server_address",
    default="http://0.0.0.0:8500",
    help="Address and port of monitoring server",
)
@click.option("--chat_id", prompt="chat_id", help="telegram chat_id", type=click.INT)
@click.option("--token", prompt="token", help="telegram bot token")
@click.option("--ip_address", prompt="ip_address", help="ip address to monitor")
@click.option(
    "--mon_type",
    default="ping",
    help="Monitoring tool. Currently only ping is supported",
)
def add_mon(server_address, chat_id, token, ip_address, mon_type):
    # Defining the host is optional and defaults to http://localhost
    # See configuration.py for a list of all supported configuration parameters.
    configuration = openapi_client.Configuration(host=server_address)

    # Enter a context with an instance of the API client
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.DefaultApi(api_client)
        telegram_chat_data = openapi_client.TelegramChatData(
            chat_id=chat_id, token=token, ip_address=ip_address, tool=mon_type
        )
        try:
            # Add Telegram
            api_response = api_instance.add_telegram_add_telegram_post(
                telegram_chat_data
            )
            pprint("The response of DefaultApi->add_telegram_add_telegram_add_post:\n")
            integer = int(api_response["id"])
            pprint(integer)
        except Exception as e:
            logger.error(
                "Exception when calling DefaultApi->add_telegram_add_telegram_add_post: %s\n"
                % e
            )


@click.command()
@click.option(
    "--server_address",
    default="http://0.0.0.0:8500",
    help="Address and port of monitoring server",
)
@click.option(
    "--id", prompt="mon id to delete", help="mon id to delete", type=click.INT
)
def del_mon(server_address, id):
    # Defining the host is optional and defaults to http://localhost
    # See configuration.py for a list of all supported configuration parameters.
    configuration = openapi_client.Configuration(host=server_address)

    # Enter a context with an instance of the API client
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.DefaultApi(api_client)

        try:
            # Del Telegram
            api_response = api_instance.del_telegram_del_telegram_post(int(id))
            pprint(api_response)

        except Exception as e:
            logger.error(
                "Exception when calling DefaultApi->del_telegram_del_telegram_post: %s\n"
                % e
            )


@click.command()
@click.option(
    "--server_address",
    default="http://0.0.0.0:8500",
    help="Address and port of monitoring server",
)
def list_mon(server_address):
    # Defining the host is optional and defaults to http://localhost
    # See configuration.py for a list of all supported configuration parameters.
    configuration = openapi_client.Configuration(host=server_address)

    # Enter a context with an instance of the API client
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.DefaultApi(api_client)

        try:
            # list Telegram
            api_response = api_instance.list_telegram_list_telegram_post()
            pprint(api_response)

        except Exception as e:
            logger.error(
                "Exception when calling DefaultApi->list_telegram_list_telegram_post: %s\n"
                % e
            )


@click.group()
def group():
    pass


group.add_command(add_mon)
group.add_command(del_mon)
group.add_command(list_mon)


if __name__ == "__main__":
    # Define logger
    logger = logging.getLogger("mylogger")
    # Set default logger level. Can be overwritten by command line
    logger.setLevel(logging.DEBUG)

    logFormatter = logging.Formatter(
        "%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s"
    )
    consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    group()
