import click  # documentation https://click.palletsprojects.com/en/7.x/
import json
from pathlib import Path
from fragdenstaat_client.api import APIClient
from fragdenstaat_client.converter import (
    validate_file_names,
    convert_multiple_json_to_csv,
)


@click.group()
@click.option("-u", "--username", default=None)
@click.option("-p", "--password", default=None)
@click.pass_context
def main(ctx, username, password):
    ctx.obj = {
        "client": APIClient(username, password),
        "username": username,
        "password": password,
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


@main.command("json-to-csv")
@click.argument("target-csv")
@click.argument("json-file-names", nargs=-1)
@click.option("-f", "--force", is_flag=True)
@click.pass_context
def json_to_csv(ctx, target_csv, json_file_names, force):
    paths = validate_file_names(json_file_names)

    target_csv_path = Path(target_csv)
    if target_csv_path.exists() and not force:
        print(
            f"\033[1;31m{target_csv_path} already exists use --force if you want to really do it\033[0m"
        )
        raise SystemExit(1)

    print("Converting JSON to CSV")
    convert_multiple_json_to_csv(target_csv_path, *paths)
