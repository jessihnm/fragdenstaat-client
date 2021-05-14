import click  # documentation https://click.palletsprojects.com/en/7.x/
import json
from fragdenstaat_client.api import Authenticator, APIClient, Configuration



@click.command()
def main():
    print("Requesting data from Frag Den Staat")

    config = Configuration()
    auth = Authenticator(config)
    client = APIClient(auth)

    requests = client.retrieve_requests()
    print(json.dumps(requests, indent=4))



