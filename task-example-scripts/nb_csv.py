import json
import csv

NBACK_DATA_PATH = "example-data/n-back.json"
OUTPUT_CSV_PATH = "output-csv/n-back.csv"

with open(NBACK_DATA_PATH) as datafile:
    datatext = datafile.read()
timeline = json.loads(datatext)

with open(OUTPUT_CSV_PATH, "w") as csvfile:
    fieldnames = (
        "trial_type",
        "isRelevant",
        "dateTime",
        "n",
        "missed_count",
        "sequence",
        "index",
        "correct",
        "time_from_focus",
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
            assert trial.get("trial_type") == "n-back"
            shared = {
                "trial_type": trial["trial_type"],
                "isRelevant": trial["isRelevant"],
                "dateTime": trial["dateTime"],
                "n": trial["n"],
                "sequence": "".join(trial["sequence"]),
                "missed_count": len(trial["missedIndices"]),
            }
            for response in trial["responses"]:
                row = shared.copy()
                row.update({
                    "index": response["index"],
                    "correct": response["correct"],
                    "time_from_focus": response["time_from_focus"],
                })
                writer.writerow(row)
