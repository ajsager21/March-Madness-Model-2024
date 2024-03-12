#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Read CSV file into DataFrame
team_ratings = pd.read_csv('March Madness.csv')

# Define team adjustments
team_adjustments = {
    'South Florida': 'Final Four',
    'UC Irvine': 'Elite Eight',
    'Appalachian State': 'Elite Eight',
    'Vermont': 'Elite Eight',
    'Alabama': 'Sweet Sixteen',
    'Baylor': 'Elite Eight',
    'Houston': 'Elite Eight'
}

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("March Madness Predictor"),
    html.Label("Team 1:"),
    dcc.Input(id='team1', type='text', value=''),
    html.Label("Team 2:"),
    dcc.Input(id='team2', type='text', value=''),
    html.Button('Predict', id='predict-button', n_clicks=0),
    html.Div(id='prediction-output')
])

# Define function to calculate win probabilities
def get_win_probability(team_1, team_2, team_ratings, team_adjustments):
    # Retrieve ratings for the specified teams
    rating_1 = team_ratings.loc[team_ratings['Team'] == team_1, 'New Rating'].values[0]
    rating_2 = team_ratings.loc[team_ratings['Team'] == team_2, 'New Rating'].values[0]
    
    # Calculate the difference in ratings
    rating_difference = rating_1 - rating_2
    
    # Calculate win probability for team 1
    win_probability_1 = 1 / (1 + 10 ** (-rating_difference / 20))
    
    # Calculate win probability for team 2
    win_probability_2 = 1 - win_probability_1
    
    # Adjust win probability based on team adjustments
    team1_category = calculate_likelihood(team_1, team_adjustments)
    team2_category = calculate_likelihood(team_2, team_adjustments)
    
    # Return both win probabilities
    return win_probability_1, win_probability_2, team1_category, team2_category

# Define function to calculate team likelihood based on adjustments
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

# Define callback to update prediction output
@app.callback(
    Output('prediction-output', 'children'),
    [Input('predict-button', 'n_clicks')],
    [dash.dependencies.State('team1', 'value'), dash.dependencies.State('team2', 'value')]
)
def update_prediction(n_clicks, team1, team2):
    if n_clicks > 0:
        # Call the get_win_probability function to get win probabilities
        win_probability_1, win_probability_2, team1_category, team2_category = get_win_probability(team1, team2, team_ratings, team_adjustments)
        
        # Add spaces and line breaks
        output = html.Div([
            f"{team1} ({team1_category}) vs {team2} ({team2_category})",
            html.Br(),
            html.P(f"Win Probability for {team1}: {win_probability_1:.2f}"),
            html.P(f"Win Probability for {team2}: {win_probability_2:.2f}")
        ])
        
        return output

if __name__ == '__main__':
    app.run_server(port=8052, debug=True)


# In[ ]:




