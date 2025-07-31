"""
Baseball Position Guessing Game - Main Flask Application
"""
from flask import Flask, render_template, request, jsonify, session
import csv
import random
import re
from difflib import SequenceMatcher
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

class BaseballGame:
    """Main game logic for the baseball position guessing game."""
    
    POSITIONS = {
        'C': 'Catcher',
        '1B': 'First Base',
        '2B': 'Second Base',
        '3B': 'Third Base',
        'SS': 'Shortstop',
        'LF': 'Left Field',
        'CF': 'Center Field',
        'RF': 'Right Field',
        'DH': 'Designated Hitter'
    }
    
    def __init__(self, csv_file='baseball_data.csv'):
        self.csv_file = csv_file
        self.data = self._load_data()
    
    def _load_data(self):
        """Load baseball data from CSV file."""
        data = []
        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append({
                        'year': int(row['year']),
                        'team': row['team'].strip(),
                        'position': row['position'].strip(),
                        'player_name': row['player_name'].strip(),
                        'games_played': int(row['games_played'])
                    })
        except FileNotFoundError:
            # Create sample data if file doesn't exist
            data = self._create_sample_data()
            self._save_sample_data(data)
        return data
    
    def _create_sample_data(self):
        """Create sample data for demonstration."""
        sample_data = [
            # 2020 Los Angeles Dodgers (World Series Champions)
            {'year': 2020, 'team': 'Los Angeles Dodgers', 'position': 'C', 'player_name': 'Austin Barnes', 'games_played': 30},
            {'year': 2020, 'team': 'Los Angeles Dodgers', 'position': '1B', 'player_name': 'Max Muncy', 'games_played': 58},
            {'year': 2020, 'team': 'Los Angeles Dodgers', 'position': '2B', 'player_name': 'Gavin Lux', 'games_played': 23},
            {'year': 2020, 'team': 'Los Angeles Dodgers', 'position': '3B', 'player_name': 'Justin Turner', 'games_played': 42},
            {'year': 2020, 'team': 'Los Angeles Dodgers', 'position': 'SS', 'player_name': 'Corey Seager', 'games_played': 52},
            {'year': 2020, 'team': 'Los Angeles Dodgers', 'position': 'LF', 'player_name': 'AJ Pollock', 'games_played': 55},
            {'year': 2020, 'team': 'Los Angeles Dodgers', 'position': 'CF', 'player_name': 'Cody Bellinger', 'games_played': 56},
            {'year': 2020, 'team': 'Los Angeles Dodgers', 'position': 'RF', 'player_name': 'Mookie Betts', 'games_played': 55},
            {'year': 2020, 'team': 'Los Angeles Dodgers', 'position': 'DH', 'player_name': 'Edwin Rios', 'games_played': 15},
            
            # 2021 Atlanta Braves (World Series Champions)
            {'year': 2021, 'team': 'Atlanta Braves', 'position': 'C', 'player_name': 'Travis d\'Arnaud', 'games_played': 82},
            {'year': 2021, 'team': 'Atlanta Braves', 'position': '1B', 'player_name': 'Freddie Freeman', 'games_played': 159},
            {'year': 2021, 'team': 'Atlanta Braves', 'position': '2B', 'player_name': 'Ozzie Albies', 'games_played': 156},
            {'year': 2021, 'team': 'Atlanta Braves', 'position': '3B', 'player_name': 'Austin Riley', 'games_played': 160},
            {'year': 2021, 'team': 'Atlanta Braves', 'position': 'SS', 'player_name': 'Dansby Swanson', 'games_played': 160},
            {'year': 2021, 'team': 'Atlanta Braves', 'position': 'LF', 'player_name': 'Eddie Rosario', 'games_played': 109},
            {'year': 2021, 'team': 'Atlanta Braves', 'position': 'CF', 'player_name': 'Ronald Acuna Jr', 'games_played': 82},
            {'year': 2021, 'team': 'Atlanta Braves', 'position': 'RF', 'player_name': 'Jorge Soler', 'games_played': 137},
        ]
        return sample_data
    
    def _save_sample_data(self, data):
        """Save sample data to CSV file."""
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['year', 'team', 'position', 'player_name', 'games_played']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    def get_random_team(self):
        """Get a random team from a random year between 2000-2024."""
        year = random.randint(2000, 2024)
        teams_for_year = list(set([row['team'] for row in self.data if row['year'] == year]))
        
        if not teams_for_year:
            # Fallback to any available team if no teams for selected year
            year = random.choice(list(set([row['year'] for row in self.data])))
            teams_for_year = list(set([row['team'] for row in self.data if row['year'] == year]))
        
        team = random.choice(teams_for_year)
        return year, team
    
    def get_team_roster(self, year, team):
        """Get the roster for a specific team and year."""
        roster = {}
        team_data = [row for row in self.data if row['year'] == year and row['team'] == team]
        
        first_nine = team_data[:9]  # Get first nine players for the roster
        if first_nine[8]['position'] != 'DH':
            # If we did not have a primary DH, ignore it
            team_data = first_nine[:8]
        else:
            # If we have a DH, include it
            team_data = first_nine

        for row in team_data:
            position = row['position']
            if position in self.POSITIONS:  # Only include defined positions
                roster[position] = row['player_name']
        
        return roster
    
    def has_designated_hitter(self, roster):
        """Check if the team uses a designated hitter."""
        return 'DH' in roster
    
    def sanitize_input(self, name):
        """Sanitize user input to only allow alphabetic characters, spaces, apostrophes, and periods."""
        if not name:
            return ""
        # Remove any non-alphabetic characters except spaces, apostrophes, and periods
        sanitized = re.sub(r"[^a-zA-Z\s'.]", '', name.strip())
        # Remove extra spaces
        sanitized = re.sub(r'\s+', ' ', sanitized)
        return sanitized
    
    def compare_names(self, guess, actual):
        """Compare names with fuzzy matching (case-insensitive, 2 character tolerance)."""
        if not guess or not actual:
            return False, 0
        
        guess = guess.lower().strip()
        actual = actual.lower().strip()
        
        # Exact match
        if guess == actual:
            return True, 1.0
        
        # Calculate similarity using SequenceMatcher
        similarity = SequenceMatcher(None, guess, actual).ratio()
        
        # Check if names are within 2 characters using edit distance approximation
        # A similarity of 0.8 or higher typically indicates close matches
        if similarity >= 0.8:
            return True, similarity
        
        return False, similarity
    
    def evaluate_guesses(self, guesses, roster):
        """Evaluate user guesses against the correct roster."""
        results = {}
        correct_count = 0
        total_guesses = 0
        
        for position, position_name in self.POSITIONS.items():
            if position in roster:  # Only evaluate positions that exist in roster
                guess = guesses.get(position, "")
                actual = roster[position]
                
                if guess:  # User made a guess
                    total_guesses += 1
                    sanitized_guess = self.sanitize_input(guess)
                    is_correct, similarity = self.compare_names(sanitized_guess, actual)
                    
                    if is_correct:
                        correct_count += 1
                        results[position] = {
                            'guess': sanitized_guess,
                            'actual': actual,
                            'correct': True,
                            'message': 'Correct!' if similarity == 1.0 else 'Correct (close match)!',
                            'similarity': similarity
                        }
                    else:
                        results[position] = {
                            'guess': sanitized_guess,
                            'actual': actual,
                            'correct': False,
                            'message': f'Incorrect. The correct answer is: {actual}',
                            'similarity': similarity
                        }
                else:  # No guess made
                    results[position] = {
                        'guess': '',
                        'actual': actual,
                        'correct': False,
                        'message': 'No guess made',
                        'similarity': 0
                    }
        
        num_players = len(roster)

        percentage = (correct_count / num_players * 100) if total_guesses > 0 else 0
        
        return results, correct_count, num_players, percentage

# Initialize the game
game = BaseballGame()

@app.route('/')
def index():
    """Main game page."""
    # Get a new random team for this session
    year, team = game.get_random_team()
    roster = game.get_team_roster(year, team)
    
    # Store game data in session
    session['year'] = year
    session['team'] = team
    session['roster'] = roster
    
    # Check if team has designated hitter
    has_dh = game.has_designated_hitter(roster)
    
    return render_template('index.html', 
                         year=year, 
                         team=team, 
                         positions=game.POSITIONS,
                         has_dh=has_dh)

@app.route('/submit_guesses', methods=['POST'])
def submit_guesses():
    """Process user guesses and return results."""
    try:
        # Get data from session
        roster = session.get('roster', {})
        year = session.get('year')
        team = session.get('team')
        
        if not roster:
            return jsonify({'error': 'No active game found'}), 400
        
        # Get user guesses from form
        guesses = {}
        for position in game.POSITIONS.keys():
            guess = request.form.get(position, '').strip()
            if guess:
                guesses[position] = guess
        
        # Evaluate guesses
        results, correct_count, num_players, percentage = game.evaluate_guesses(guesses, roster)
        
        return jsonify({
            'results': results,
            'correct_count': correct_count,
            'num_players': num_players,
            'percentage': round(percentage, 1),
            'year': year,
            'team': team
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/new_game')
def new_game():
    """Start a new game with a different team."""
    return index()

if __name__ == '__main__':
    app.run(debug=True)
