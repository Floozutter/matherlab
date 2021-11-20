import json
import csv

SPATIAL_ORIENTATION_DATA_PATH = "example-data/spatial-orientation.json"
OUTPUT_CSV_PATH = "spatial-orientation.csv"

with open(SPATIAL_ORIENTATION_DATA_PATH) as datafile:
    datatext = datafile.read()
timeline = json.loads(datatext)

with open(OUTPUT_CSV_PATH, "w") as csvfile:
    fieldnames = (
        "trial_type",
        "isRelevant",
        "dateTime",
        "completionReason",
        "rt",
        "targetRadians",
        "responseRadians",
    )
    writer = csv.DictWriter(
        csvfile,
        fieldnames = fieldnames,
        restval = "",
        extrasaction = "ignore",
        dialect = csv.unix_dialect,
    )
    writer.writeheader()
    for trial in timeline:
        if trial.get("isRelevant", False):
            assert trial.get("trial_type") == "spatial-orientation"
            writer.writerow(trial)
