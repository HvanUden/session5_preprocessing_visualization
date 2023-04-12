import pandas as pd

participants = pd.read_csv('participants.csv')

# Load in each participant dataset and add it to a list
trials_per_participant = []
for participant_id in participants['id']:
    participant_data = pd.read_csv(f'participants/{participant_id}.csv')
    trials_per_participant.append(participant_data)

# Merge the list, and rename the index column as trial_order
trials = pd.concat(trials_per_participant)
trials.rename(columns={'Unnamed: 0': 'trial_order'}, inplace=True)

# Save a single file with all trials
trials.to_csv('trials.csv', index=False)
