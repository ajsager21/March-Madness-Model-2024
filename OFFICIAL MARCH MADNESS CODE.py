#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Read Excel file into DataFrame
data = pd.read_csv('March Madness.csv')


# In[2]:


team_ratings = pd.read_csv('March Madness.csv')


# In[4]:


def calculate_likelihood(team_name, team_adjustments):
    # Check if the team has a specific adjustment
    if team_name in team_adjustments:
        return team_adjustments[team_name]
    
    # Define thresholds and associated categories based on your data
    ranges = [(0, 18), (18, 23.5), (23.5, 26), (26, 28), (28, float('inf'))]  # Example ranges
    categories = ['Round of 32', 'Sweet Sixteen', 'Elite Eight', 'Final Four', 'Champion']  # Define categories for each range
    
    # Find the team's rating based on the team name
    rating = team_ratings.loc[team_ratings['Team'] == team_name, 'New Rating'].values[0]
    
    # Find the category based on the team rating
    for i, (lower, upper) in enumerate(ranges):
        if lower <= rating < upper:
            return categories[i]
    return 'Not qualified'  # Default category if rating is below all ranges

def get_win_probability(team_1, team_2, team_ratings, team_adjustments, kill_shot_data):
    # Retrieve ratings for the specified teams
    rating_1 = team_ratings.loc[team_ratings['Team'] == team_1, 'New Rating'].values[0]
    rating_2 = team_ratings.loc[team_ratings['Team'] == team_2, 'New Rating'].values[0]
    
    # Calculate the difference in ratings
    rating_difference = rating_1 - rating_2
    
    # Calculate win probability for team 1 based on rating difference
    win_probability_1 = 1 / (1 + 10 ** (-rating_difference / 20))
    
    # Calculate win probability for team 2
    win_probability_2 = 1 - win_probability_1
    
    # Adjust win probability based on team adjustments
    team1_category = calculate_likelihood(team_1, team_adjustments)
    team2_category = calculate_likelihood(team_2, team_adjustments)
    
    # Apply kill shot adjustments
    if team_1 in kill_shot_data['Team'].values:
        team_1_kill_shot_o = kill_shot_data.loc[kill_shot_data['Team'] == team_1, 'O Kill Shot?'].values[0]
        team_1_kill_shot_d = kill_shot_data.loc[kill_shot_data['Team'] == team_1, 'D Kill Shot?'].values[0]
        team_1_kill_shot_bad_d = kill_shot_data.loc[kill_shot_data['Team'] == team_1, 'D Kill Shot (BAD)'].values[0]
        
        if team_1_kill_shot_o == 1:
            win_probability_1 += 0.05  # Positive impact on win probability
        if team_1_kill_shot_d == 1:
            win_probability_1 += 0.05  # Positive impact on win probability
        if team_1_kill_shot_bad_d == 1:
            win_probability_1 -= 0.1   # Negative impact on win probability
        
        # If opponent has a kill shot (BAD), adjust win probability even more positively
        if team_2 in kill_shot_data['Team'].values:
            team_2_kill_shot_bad_d = kill_shot_data.loc[kill_shot_data['Team'] == team_2, 'D Kill Shot (BAD)'].values[0]
            if team_2_kill_shot_bad_d == 1:
                win_probability_1 += 0.1  # Additional positive impact on win probability
    
    # Print teams with their adjusted rounds
    print(f"{team_1} ({team1_category}) vs {team_2} ({team2_category})")
    
    # Return both win probabilities
    return win_probability_1, win_probability_2

team_adjustments = {
    'South Florida': 'Final Four',
    'UC Irvine': 'Elite Eight',
    'Appalachian State': 'Elite Eight',
    'Vermont': 'Elite Eight',
    'Alabama': 'Sweet Sixteen',
    'Baylor': 'Elite Eight',
    'Houston': 'Elite Eight'
}

# Example usage:
team1 = 'Minnesota'
team2 = 'Nebraska'
kill_shot_data = pd.read_csv('March Madness.csv')  # Assuming the kill shot data is in the same CSV file
win_probability = get_win_probability(team1, team2, team_ratings, team_adjustments, kill_shot_data)
print(f"The probability of {team1} winning against {team2} is {win_probability[0]:.2f}")
print(f"The probability of {team2} winning against {team1} is {win_probability[1]:.2f}")


# In[ ]:





# In[ ]:




