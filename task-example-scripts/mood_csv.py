import json
import csv

MOOD_DATA_PATH = "example-data/mood-memory.json"
OUTPUT_CSV_PATH = "output-csv/mood-memory.csv"

with open(MOOD_DATA_PATH) as datafile:
    datatext = datafile.read()
timeline = json.loads(datatext)

with open(OUTPUT_CSV_PATH, "w") as csvfile:
    fieldnames = (
        "trial_type",
        "isRelevant",
        "dateTime",
        "Good Mood",
        "Bad Mood",
        "Neutral Mood",
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
            assert trial.get("trial_type") == "percent-sum"
            row = {
                "trial_type": trial["trial_type"],
                "isRelevant": trial["isRelevant"],
                "dateTime": trial["dateTime"],
            }
            response = trial["response"]
            if isinstance(response, dict):
                # response is in updated format (variable-size dict)
                row.update(response)
            elif isinstance(response, list):
                # response is in old format (homogenous array of fixed-key dicts)
                for record in response:
                    row[record["field"]] = record["value"]
            else:
                # something terrible has happened
                raise AssertionError("unexpected response type")
            writer.writerow(row)
