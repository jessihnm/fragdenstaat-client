import json
import csv
from tempfile import NamedTemporaryFile
from sure import expect
from io import StringIO
from pathlib import Path
from fragdenstaat_client.converter import (
    json_to_csv,
    flatten_item,
    convert_multiple_json_to_csv,
)


fixures_path = Path(__file__).parent.joinpath(".fixtures").absolute()


def load_fixture(filename: str) -> dict:
    with fixures_path.joinpath(filename).open() as fd:
        return json.load(fd)


def test_convert_to_csv_escaping_propertly():
    "It should escape the line breaks from the description field"

    # Given that I open a file that contains a multiple line description
    json_fixture_data = load_fixture("jsonNo73900.json")
    objects = list(map(flatten_item, json_fixture_data["objects"][:1]))

    json_fixture_data["objects"] = objects
    fd_read = StringIO(json.dumps(json_fixture_data))

    # And that I have a in-memory buffer
    fd_write = StringIO()

    # When I call json_to_csv
    json_to_csv(fd_read, fd_write)

    # Then I seek the the beginning of the file
    fd_write.seek(0)

    converted_objects = list(map(dict, csv.DictReader(fd_write)))
    assert len(converted_objects) == len(objects)
    assert objects == converted_objects


def test_convert_multiple_json_files_to_single_csv():
    # Given that I have a couple of json files
    json_no_400 = fixures_path.joinpath("jsonNo400.json")
    json_no_500 = fixures_path.joinpath("jsonNo500.json")

    # And that I have an output file
    output_csv = NamedTemporaryFile()
    csv_file_path = Path(output_csv.name)

    # When I call convert_csv
    convert_multiple_json_to_csv(csv_file_path, json_no_400, json_no_500)

    # Then it should write a valid CSV to my file
    csv_file_path.exists().should.be.true

    converted_objects = list(map(dict, csv.DictReader(csv_file_path.open("r"))))
    assert len(converted_objects) == 100
