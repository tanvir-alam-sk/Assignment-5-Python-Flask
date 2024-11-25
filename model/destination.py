import os
import json

destination_file_path = os.path.join("db", "destinations.py")

# Ensure the destination file exists
if not os.path.exists(destination_file_path):
    with open(destination_file_path, "w") as file:
        json.dump([], file)

# Read destinations
def read_destination():
    with open(destination_file_path, "r") as file:
        return json.load(file)

# Write destinations
def write_destination(destination):
    with open(destination_file_path, "w") as file:
        json.dump(destination, file, indent=4)
