import click  # documentation https://click.palletsprojects.com/en/7.x/
import json
from fragdenstaat_client.api import APIClient


@click.group()
@click.pass_context
def main(ctx):
    ctx.obj = {
        "client": APIClient(),
    }

@main.command("config")
@click.pass_context
def show_config(ctx):
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    print(json.dumps(dict(username=username, password=password), indent=4))


@main.command("requests")
@click.pass_context
def froi_requests(ctx):
    client = ctx.obj["client"]
    print("Requesting data from Frag Den Staat")

    requests = client.retrieve_requests()
    print(json.dumps(requests, indent=4))


