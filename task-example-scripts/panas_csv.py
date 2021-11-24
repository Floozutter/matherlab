import json
import csv

PANAS_DATA_PATH = "example-data/panas.json"
OUTPUT_CSV_PATH = "output-csv/panas.csv"

with open(PANAS_DATA_PATH) as datafile:
    datatext = datafile.read()
timeline = json.loads(datatext)

with open(OUTPUT_CSV_PATH, "w") as csvfile:
    fieldnames = (
        "trial_type",
        "isRelevant",
        "dateTime",
        "rt",
        "interested",
        "distressed",
        "excited",
        "upset",
        "strong",
        "guilty",
        "scared",
        "hostile",
        "enthusiastic",
        "proud",
        "irritable",
        "alert",
        "ashamed",
        "inspired",
        "nervous",
        "determined",
        "attentive",
        "jittery",
        "active",
        "afraid",
    )
    writer = csv.DictWriter(
        csvfile,
        fieldnames = fieldnames,
        restval = "",
        extrasaction = "raise",
        dialect = csv.unix_dialect,
    )
    writer.writeheader()
    for trial in timeline:
        if trial.get("isRelevant", False):
            assert trial.get("trial_type") == "survey-likert"
            # start row with some of the key-value pairs in trial
            row = {
                "trial_type": trial["trial_type"],
                "isRelevant": trial["isRelevant"],
                "dateTime": trial["dateTime"],
                "rt": trial["rt"],
            }
            # add all of the key-value pairs in trial["response"] to row
            row.update(trial["response"])
            # write the row to the CSV file
            writer.writerow(row)
