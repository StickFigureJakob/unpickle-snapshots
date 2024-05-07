import os
import json
import pickle
import base64
from pprint import pprint

path_to_read = "pickled_snapshots/"
path_to_write = "unpickled_snapshots/"


def main():
    json_files = [pos_json for pos_json in os.listdir(path_to_read)]

    print("Available files to load:")
    print("Enter 'a' for all or 'q' to quit")
    for index, file_name in enumerate(json_files):
        print(f"{index}. {file_name}")

    while True:
        choice = input("Enter the number of the file you want to load: ")
        if choice.lower() == "q":
            print("Exiting.")
            return
        if choice.lower() == "a":
            process_all(json_files)
            return
        try:
            choice_index = int(choice)
            if 0 <= choice_index < len(json_files):
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")

    file_name = json_files[choice_index]
    process_selcted(file_name)


def process_all(json_files):
    for file_name in json_files:
        process_selcted(file_name)


def process_selcted(file_name):
    snapshot = load_snapshot(f"{path_to_read}{file_name}")
    timestamp, data = transform_snapshot(snapshot)
    store_snapshot(timestamp, data, f"{path_to_write}{file_name}")


def load_snapshot(file_path):
    file = open(file_path)
    data = json.load(file)
    return data


def transform_snapshot(loaded_snapshot):
    encoded_string = loaded_snapshot["value"]["$binary"]["base64"]
    base64_bytes = encoded_string.encode("latin1")
    sample_string_bytes = base64.b64decode(base64_bytes)
    timestamp, data = pickle.loads(sample_string_bytes, encoding="latin1")
    return timestamp, data


def store_snapshot(timestamp, data, file_path):
    with open(file_path, "w") as file:
        file.write(f"Timestamp: {timestamp}\n")
        file.write("Data:\n")
        pprint(data, stream=file)
        print(f"\n stored at {file_path}")


if __name__ == "__main__":
    main()
