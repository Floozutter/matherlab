import json
import csv

DAILY_STRESSORS_DATA_PATH = "example-data/daily-stressors.json"
OUTPUT_CSV_PATH = "output-csv/daily-stressors.csv"

with open(DAILY_STRESSORS_DATA_PATH) as datafile:
    datatext = datafile.read()
timeline = json.loads(datatext)

with open(OUTPUT_CSV_PATH, "w") as csvfile:
    fieldnames = (
        "trial_type",
        "isRelevant",
        "dateTime",
        "Q0",
        "Q1",
        "Q2",
        "Q3",
        "Q4",
        "Q5",
        "Q6",
        "Q7",
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
            assert trial.get("trial_type") == "survey-multi-choice"
            row = {
                "trial_type": trial["trial_type"],
                "isRelevant": trial["isRelevant"],
                "dateTime": trial["dateTime"],
            }
            row.update(trial["response"])
            writer.writerow(row)
