import json  # Python module for working with JSON.
import math


# Decode the timeline data from text in JSON format into a Python object.
with open("example_sot_data.json") as datafile:  # Example of reading text from a file.
    datatext = datafile.read()
data = json.loads(datatext)  # Use `json.loads` to [load] a JSON [s]tring as a Python object.


# If the JSON was generated and loaded correctly, `data` should be a list of dictionaries.
# list: https://docs.python.org/3/tutorial/introduction.html#lists
# dict: https://docs.python.org/3/tutorial/datastructures.html#dictionaries

# Each dictionary in the list should correspond to a trial in the jsPysch experiment timeline.
# To remind us about the structure of our data, let's alias our variable.
timeline = data  # (Not a copy! Both `timeline` and `data` now refer to the same object.)

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
# For example, every trial at least records a value for the key "trial_type".
first_type = first_trial["trial_type"]  # Use square brackets with a key to get an item from dicts.

# The key-value pairs a trial will record depends on its type.
# Trying to get a value from a dict with a key that isn't present will result in an error.
# For example, "isRelevant" is a key that may not be present in every trial.
# To avoid this, first check if the dict contains the key, then try to access its value.
if "isRelevant" in first_trial:  # Use the `in` operator to check if a dict contains a key.
    first_is_relevant = first_trial["isRelevant"]
else:
    first_is_relevant = False
# Alternatively, use the `dict.get` method to supply a default if the key isn't present.
first_relevant_alt = first_trial.get("isRelevant", False)


# Let's try counting the number of spatial-orientation trials in the timeline.
number_of_sot_trials = 0  # Initialize count to 0.
# To loop over every trial in the timeline, use `for` statements.
for trial in timeline:  # `trial` is the name that each item in timeline will be bound to.
    if trial["trial_type"] == "spatial-orientation":  # Use `==` to test equality.
        number_of_sot_trials += 1

# Now, let's try counting all of the trials in the timeline with relevant data.
number_of_relevant_trials = 0
for trial in timeline:
    if trial.get("isRelevant", False):  # `get` is used here because the key may not be present.
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

# First, make a list of all relevant spatial-orientation trials.
relevant_sot_timeline = []
for trial in relevant_timeline:
    if trial["trial_type"] == "spatial-orientation":
        relevant_sot_timeline.append(trial)

# Then, compute the total angular distance across all relevant spatial-orientation trials.
total_angular_distance = 0
for trial in relevant_sot_timeline:
    target_radians = trial["targetRadians"]
    response_radians = trial["responseRadians"]
    signed_angular_distance = math.atan2(
        math.sin(target_radians - response_radians),
        math.cos(target_radians - response_radians)
    )
    total_angular_distance += abs(signed_angular_distance)

# Finally, compute the average angular distance.
average_angular_distance = total_angular_distance / len(relevant_sot_timeline)

print("Average angular distance in radians for test block SOT trials:", average_angular_distance)
