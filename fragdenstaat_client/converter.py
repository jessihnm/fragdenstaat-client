#!/usr/bin/env python

import json
import csv
import argparse
from typing import List
from pathlib import Path

# base_path = Path(
#     "~/Documents/Uni/3.Semester/Data_SL_Ue/Projekt_FDS_Index/dataCollection/20210525_Data/20210525_data_full_json/"
# ).expanduser()


# target_path = Path(
#         "~/Documents/Uni/3.Semester/Data_SL_Ue/Projekt_FDS_Index/dataCollection/20210525_Data/20210525_data_8.csv"
# ).expanduser()


base_path = Path("./")
target_path = Path("./jsonNo400.csv")


def extract_objects_from_fragdenstaat_json_data(data: dict) -> List[dict]:
    return data.get("objects") or []


def prefix_dict_keys(prefix: str, data: dict) -> dict:
    result = {}
    for key, value in data.items():
        result[f"{prefix}_{key}"] = value
    return result


def flatten_item(item: dict):
    result = {}
    for key, value in item.items():
        # if key == "due_date":
        #     import ipdb;ipdb.set_trace()  # fmt: skip
        if not isinstance(value, dict) and not isinstance(value, (str, bytes)):
            result[key] = json.dumps(value)
        elif isinstance(value, dict):
            result.update(flatten_item(prefix_dict_keys("institution", value)))
        else:  # str
            result[key] = value

    return result


def json_to_csv(fd_read, fd_write, write_header: bool = True):
    writer = csv.writer(fd_write, delimiter=",", strict=True)
    data = json.load(fd_read)

    objects = map(flatten_item, extract_objects_from_fragdenstaat_json_data(data))
    for index, obj in enumerate(objects):
        if write_header and index is 0:  # write the keys to the first line of the CSV
            writer.writerow(obj.keys())

        writer.writerow(obj.values())


def convert_multiple_json_to_csv(target_path: Path, *args):
    with target_path.open("a", encoding="utf-8-sig", newline="") as fd_write:
        for index, source_path in enumerate(args):
            is_first_file = index == 0
            with source_path.open("r") as fd_read:
                print(f"adding json data from {source_path} to {target_path}")
                json_to_csv(fd_read, fd_write, write_header=is_first_file)


def validate_file_names(names: List[Path]) -> List[Path]:
    paths = list(map(Path, names))
    for path in paths:
        if not path.exists():
            print(f"{path} does not exist")
            raise SystemExit(1)

        if not path.is_file():
            print(f"{path} exists but is not a file")
            raise SystemExit(1)

    return paths
