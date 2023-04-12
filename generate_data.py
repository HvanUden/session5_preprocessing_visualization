from faker import Faker
from scipy import stats
from random import choices, randint, shuffle
import numpy as np
import pandas as pd

# You can ignore this script entirely; it is used to generate the data for this lecture.
# If you are interested, feel free to take a look, but it features several concepts that we haven't really covered in class.

fake = Faker()

# Define the participant structure
mean_age, std_age = 22, 5
participant_structure = {
    'first_name': fake.first_name,
    'last_name': fake.last_name,
    'age': lambda: int(stats.truncnorm.rvs(a=(18 - mean_age) / std_age, b=(80 - mean_age) / std_age, loc=mean_age, scale=std_age)),
    'gender': lambda: choices(['man', 'woman', 'non-binary', 'other'], weights=(0.3, 0.6, 0.05, 0.05))[0],
    'group': lambda: choices(['x', 'y', 'control'])[0],
    'id': lambda: randint(10000, 99999)
}

# Define the conditions, with true fixed effects
conditions = [('baseline', 0, 0.85), ('condition_a', 0.4, 0.75), ('condition_b', -0.1, 0.95)]

# Define the trial structure
trial_structure = {
    'id': lambda p, c, r, d: p.id,
    'condition': lambda p, c, r, d: c[0],
    'correct': lambda p, c, r, d: choices([True, False], weights=(c[2], 1 - c[2]))[0],
    'RT': lambda p, c, r, d: np.math.exp(stats.norm.rvs(loc=6 - 0.05 * (p.age - 22) / 5 + r + c[1], scale=d))
}

# Generate the participant data
n_participants = 32
participants = pd.DataFrame([{key: generator() for key, generator in participant_structure.items()} for i in range(n_participants)])
participants.to_csv('participants.csv', index=False)

# Generate the trial data
deviation = 0.5
n_trials = 40
for i, participant in participants.iterrows():
    random_effect = stats.norm.rvs(scale=0.25)
    trials = []
    for condition in conditions:
        trials.extend([{key: generator(participant, condition, random_effect, deviation)
                        for key, generator in trial_structure.items()} for i in range(n_trials)])
    shuffle(trials)
    trials = pd.DataFrame(trials)
    trials.to_csv(f'participants/{participant.id}.csv')
