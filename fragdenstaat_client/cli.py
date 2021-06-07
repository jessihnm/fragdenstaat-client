"""
fragdenstaat_client.cli - command-line module of the python package fragdenstaat

The functions in this module are using the python library `click` to parse command-line options, its full documentation can be found in this link: 
https://click.palletsprojects.com/en/7.x/

"""
import click  # documentation
import json
from pathlib import Path
from fragdenstaat_client.api import APIClient
from fragdenstaat_client.converter import (
    validate_file_names,
    convert_multiple_json_to_csv,
)


@click.group()
@click.pass_context
def main(ctx):
    """main function that is executed when the command-line script `fragdenstaat-client`is 
    invoked from the console terminal."""


@main.command("requests", help="downloads requests from fragdenstaat.de")
@click.option("-m", "--max-pages", type=int, default=3392)
@click.option("-o", "--offset-increment", type=int, default=50)
@click.pass_context
def froi_requests(ctx, max_pages, offset_increment):
    """handles the command `fragdenstaat-client requests`

    the parameter max_pages is hardcoded to 3392 which is the number of pages 
    we saw were available at the time we scraped the data, it might need to be updated according to website updates.
    """
    # first we instantiate the APIClient class which downloads the data
    client = APIClient()

    offset = 0

    # then we iterate over a count from 0 up to 3392 (max pages)
    for page in range(0, max_pages):  
        # for each page we save a new json file on the disk
        dataname = f"jsonNo{offset}.json" 

        print(f"Requesting data from Frag Den Staat page {page + 1} of {max_pages}")

        # here we finally make a request to:
        #     https:fragdenstaat.de/api/v1/request/?format=json&offset={offset}
        requests = client.retrieve_requests(offset)

        # then we save the json file on the disk
        with open(dataname, "w") as fd:
            json.dump(requests, fd, indent=4)
            print(f"written {dataname}")

        # increment the offset to ensure unique json filenames
        offset += offset_increment

    print("finished")


@main.command("json-to-csv", help="converts json files with fragdenstaat data to csv")
@click.argument("target-csv")
@click.argument("json-file-names", nargs=-1)
@click.option("-f", "--force", is_flag=True)
@click.pass_context
def json_to_csv(ctx, target_csv, json_file_names, force):
    """handles the command `fragdenstaat-client json-to-csv`

    On the command-line it takes N positional arguments, the first argument us the name of the target csv file where the data from all json files will be merged together
    All subsequent argument are json file names that will be processed.

    The `--force` option is a safety feature to prevent us to mistakenly overwrite an existing file.
    """

    # first, we take the list of json file names and ensure that all of them exist and prevent our took from crashing midway processing the files
    paths = validate_file_names(json_file_names)

    # second, we validate that the CSV already exists
    target_csv_path = Path(target_csv)
    if target_csv_path.exists() and not force:
        print(
            f"\033[1;31m{target_csv_path} already exists use --force if you want to REALLY do it\033[0m"
        )
        raise SystemExit(1)

    print("Converting JSON to CSV")
    # finally we call the function that converts the json files to csv
    convert_multiple_json_to_csv(target_csv_path, *paths)
