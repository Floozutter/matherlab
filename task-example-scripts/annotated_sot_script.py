import json  # Python module for working with JSON.
import math


SPATIAL_ORIENTATION_DATA_PATH = "example-data/spatial-orientation.json"


# Decode the timeline data from text in JSON format into a Python object.
with open(SPATIAL_ORIENTATION_DATA_PATH) as datafile:  # Example of reading text from a file.
    datatext = datafile.read()
timeline = json.loads(datatext)  # Use `json.loads` to [load] a JSON [s]tring as a Python object.


# If the JSON was generated and loaded correctly, `timeline` should be a list of dictionaries.
# list: https://docs.python.org/3/tutorial/introduction.html#lists
# dict: https://docs.python.org/3/tutorial/datastructures.html#dictionaries

# Each dictionary in the list should correspond to a trial in the jsPysch experiment timeline.
# For a quick sanity check, uncomment the next line to print out the contents of `timeline`.
#print(timeline)  # This will probably show a lot of text!
# Does `timeline` look like a list of dictionaries?


# The number of trials recorded during the task should be the same as the length of the timeline.
number_of_trials = len(timeline)  # Use the `len` function to get the size of a Python list.

# The first trial completed should be at the front of the timeline.
first_trial = timeline[0]  # Use square brackets with an index to get an item from Python lists.
second_trial = timeline[1]  # Python indices start from 0, so `timeline[1]` is the second trial!
final_trial = timeline[-1]  # Negative indices refer to items starting from the back of a list.

# The data recorded for each trial is represented in key-value pairs.
# For example, the first trial in the timeline should be a header for a single set's timeline, and
# should contain a value for the "dateTime", which represents when the set was started.
start_dt = first_trial["dateTime"]  # Use square brackets with a key to get an item from dicts.

# A particularly important key is the "trial_type" key.
# This is because the key-value pairs a trial will record depends on its type.

# Every trial records a value for the "trial_type" key, except for header trials like the first.
second_trial_type = second_trial["trial_type"]
# Trying to get a value from a dict using a key that isn't present will result in a KeyError.
#first_trial_type = first_trial["trial_type"]  # This will throw a KeyError.

# To avoid a KeyError, first check if the dict contains the key, then try to access its value.
if "trial_type" in first_trial:  # Use the `in` operator to check if a dict contains a key.
    first_trial_type = first_trial["trial_type"]
else:
    first_trial_type = None  # None is used here as a value to represent no trial type.

# Alternatively, use the `dict.get` method to supply a default if the key isn't present.
first_trial_type_alt = first_trial.get("isRelevant", None)  # The second arg, None, is the default.

# Use square brackets to get a key's value when you know that the key-value pair should exist.
# If you can't assume that the key-value will exist, use an `if` statement or the `get` method.


# Let's try counting the number of spatial-orientation trials in the timeline.
number_of_sot_trials = 0  # Initialize count to 0.
# To loop over every trial in the timeline, use a `for` statement.
for trial in timeline:  # `trial` is the name that each item in timeline will be bound to.
    trial_type = trial.get("trial_type", None)  # Use `get` because the key may not be present.
    if trial_type == "spatial-orientation":  # Use `==` to test equality.
        number_of_sot_trials += 1

# Now, let's try counting all of the trials in the timeline with relevant data.
number_of_relevant_trials = 0
for trial in timeline:
    if trial.get("isRelevant", False):
        number_of_relevant_trials += 1


# Let's also try to filter the timeline to build a list of only the trials that are relevant.
relevant_timeline = []  # Initialize to empty list.
for trial in timeline:
    if trial.get("isRelevant", False):
        relevant_timeline.append(trial)  # Use `append` to push an item to the back of a list.

# `number_of_relevant_trials` should be equal to `len(relevant_timeline)`.
# Try comparing the two to verify.


# As a final example, let's get the average angular distance between the target radians and the
# response radians for all relevant spatial-orientation trials.

# First, make a list of all relevant spatial-orientation trials that were completed by the user.
important_sot_timeline = []
for trial in relevant_timeline:
    if trial["trial_type"] == "spatial-orientation" and trial["completionReason"] == "responded":
        important_sot_timeline.append(trial)

# Then, compute the total angular distance across all these spatial-orientation trials.
total_angular_distance = 0
for trial in important_sot_timeline:
        target_radians = trial["targetRadians"]
        response_radians = trial["responseRadians"]
        signed_angular_distance = math.atan2(
            math.sin(target_radians - response_radians),
            math.cos(target_radians - response_radians)
        )
        total_angular_distance += (abs(signed_angular_distance))

# Finally, compute the average angular distance.
average_angular_distance = total_angular_distance / len(important_sot_timeline)

print(
    "Average angular distance in radians for completed test-block SOT trials:",
    average_angular_distance
)
