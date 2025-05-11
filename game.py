import random
import pandas as pd

def check_guesses(true_lineup, guesses):
    total = len(guesses)
    correct = 0
    true_players = {}
    for item in true_lineup:
        true_pos = item['Pos']
        true_player = item['Player']
        true_players[true_pos] = true_player
    
    for pos in guesses:
        if(true_players[pos].lower() == guesses[pos].lower()):
            correct = correct + 1
    show_guesses(true_players)
    print(f"You got {correct} out of {total} right.")

def show_guesses(guesses, year=None, team=None):
    if(year != None and team != None):
        print(f"{year} {team} Lineup:")
    else:
        print("Correct Answers:")
    for item in guesses:
        print(f"{item}: {guesses[item]}")

true_lineup = []
df = pd.read_csv('SampleData.csv')
year = 2024
team = 'Philadelphia Phillies'
true_lineup = df[(df['Year'] == year) & (df['Team'] == team)].to_dict('records')

guessed_lineup = {}
for player in true_lineup:
    guessed_lineup[player['Pos']] = "_____"

pos_response = ""
player_response = ""
while not pos_response.lower() == 'submit':
    show_guesses(guessed_lineup, year, team)
    pos_response = input("Enter position, or submit: ").upper()
    if(pos_response in guessed_lineup):
        player_response = input(f"Enter guess at {pos_response}: ")
        guessed_lineup[pos_response] = player_response
    elif(pos_response.lower() == "submit"):
        break
    else:
        print("Invalid position.")

#guessed_lineup = {'2B': 'chase utley', '1B': 'Ryan Howard', 'LF': 'Pat burrell', 'CF': '_____', 'SS': '_____', 'RF': 'Jayson Werth', '3B': '_____', 'C': '_____'}

check_guesses(true_lineup, guessed_lineup)