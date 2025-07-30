"""
Unit tests for the Baseball Position Guessing Game
"""
import unittest
import json
from app import app, BaseballGame

class TestBaseballGame(unittest.TestCase):
    """Test cases for the BaseballGame class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = BaseballGame()
        self.app = app.test_client()
        self.app.testing = True
    
    def test_sanitize_input(self):
        """Test input sanitization functionality."""
        # Test normal names
        self.assertEqual(self.game.sanitize_input("John Doe"), "John Doe")
        self.assertEqual(self.game.sanitize_input("Mike Trout"), "Mike Trout")
        
        # Test names with numbers and special characters
        self.assertEqual(self.game.sanitize_input("John123 Doe!"), "John Doe")
        self.assertEqual(self.game.sanitize_input("Mike@#$ Tr0ut"), "Mike Trut")
        
        # Test extra spaces
        self.assertEqual(self.game.sanitize_input("  John   Doe  "), "John Doe")
        
        # Test empty and None inputs
        self.assertEqual(self.game.sanitize_input(""), "")
        self.assertEqual(self.game.sanitize_input(None), "")
        
        # Test single names
        self.assertEqual(self.game.sanitize_input("John"), "John")
    
    def test_compare_names(self):
        """Test name comparison with fuzzy matching."""
        # Exact matches
        is_correct, similarity = self.game.compare_names("John Doe", "John Doe")
        self.assertTrue(is_correct)
        self.assertEqual(similarity, 1.0)
        
        # Case insensitive matches
        is_correct, similarity = self.game.compare_names("john doe", "John Doe")
        self.assertTrue(is_correct)
        self.assertEqual(similarity, 1.0)
        
        # Fuzzy matches (should be accepted)
        is_correct, similarity = self.game.compare_names("John Do", "John Doe")
        self.assertTrue(is_correct)
        
        # Completely different names
        is_correct, similarity = self.game.compare_names("John Doe", "Mike Trout")
        self.assertFalse(is_correct)
        
        # Empty inputs
        is_correct, similarity = self.game.compare_names("", "John Doe")
        self.assertFalse(is_correct)
        
        is_correct, similarity = self.game.compare_names("John Doe", "")
        self.assertFalse(is_correct)
    
    def test_has_designated_hitter(self):
        """Test designated hitter detection."""
        roster_with_dh = {'C': 'Player1', '1B': 'Player2', 'DH': 'Player3'}
        roster_without_dh = {'C': 'Player1', '1B': 'Player2', '3B': 'Player3'}
        
        self.assertTrue(self.game.has_designated_hitter(roster_with_dh))
        self.assertFalse(self.game.has_designated_hitter(roster_without_dh))
    
    def test_evaluate_guesses(self):
        """Test guess evaluation logic."""
        roster = {
            'C': 'John Doe',
            '1B': 'Mike Trout',
            '2B': 'Jose Altuve'
        }
        
        guesses = {
            'C': 'John Doe',      # Exact match
            '1B': 'Mike Trou',    # Fuzzy match
            '2B': 'Wrong Player'  # Incorrect
            # No guess for other positions
        }
        
        results, correct_count, total_guesses, percentage = self.game.evaluate_guesses(guesses, roster)
        
        # Check that we got results for all roster positions
        self.assertIn('C', results)
        self.assertIn('1B', results)
        self.assertIn('2B', results)
        
        # Check correct guess
        self.assertTrue(results['C']['correct'])
        
        # Check fuzzy match
        self.assertTrue(results['1B']['correct'])
        
        # Check incorrect guess
        self.assertFalse(results['2B']['correct'])
        
        # Check counts
        self.assertEqual(correct_count, 2)  # C and 1B should be correct
        self.assertEqual(total_guesses, 3)  # All three positions had guesses
        self.assertAlmostEqual(percentage, 66.67, places=1)  # 2/3 * 100, rounded

class TestFlaskRoutes(unittest.TestCase):
    """Test cases for Flask routes."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = app.test_client()
        self.app.testing = True
        app.config['SECRET_KEY'] = 'test-key'
    
    def test_index_route(self):
        """Test the main page route."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Baseball Position Guessing Game', response.data)
        self.assertIn(b'baseball-diamond', response.data)
    
    def test_submit_guesses_with_valid_data(self):
        """Test submitting guesses with valid data."""
        # First, get the main page to set up session
        with self.app as client:
            client.get('/')
            
            # Submit some guesses
            response = client.post('/submit_guesses', data={
                'C': 'John Doe',
                '1B': 'Mike Trout',
                '2B': 'Jose Altuve'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            
            # Check response structure
            self.assertIn('results', data)
            self.assertIn('correct_count', data)
            self.assertIn('total_guesses', data)
            self.assertIn('percentage', data)
            self.assertIn('year', data)
            self.assertIn('team', data)
    
    def test_submit_guesses_without_session(self):
        """Test submitting guesses without proper session data."""
        response = self.app.post('/submit_guesses', data={
            'C': 'John Doe'
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_new_game_route(self):
        """Test the new game route."""
        response = self.app.get('/new_game')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Baseball Position Guessing Game', response.data)
    
    def test_input_validation(self):
        """Test that input validation works through the web interface."""
        with self.app as client:
            client.get('/')
            
            # Submit guesses with invalid characters
            response = client.post('/submit_guesses', data={
                'C': 'John123 Doe!@#',
                '1B': 'Mike$%^ Trout',
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            
            # Check that results contain sanitized names
            if 'C' in data['results']:
                # The sanitized input should only contain letters and spaces
                guess = data['results']['C']['guess']
                self.assertTrue(all(c.isalpha() or c.isspace() for c in guess))

class TestDataLoading(unittest.TestCase):
    """Test cases for data loading functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = BaseballGame()
    
    def test_data_loading(self):
        """Test that data is loaded correctly."""
        self.assertIsInstance(self.game.data, list)
        self.assertGreater(len(self.game.data), 0)
        
        # Check data structure
        first_record = self.game.data[0]
        required_keys = ['year', 'team', 'position', 'player_name', 'games_played']
        for key in required_keys:
            self.assertIn(key, first_record)
    
    def test_get_random_team(self):
        """Test random team selection."""
        year, team = self.game.get_random_team()
        
        self.assertIsInstance(year, int)
        self.assertIsInstance(team, str)
        self.assertGreaterEqual(year, 2000)
        self.assertLessEqual(year, 2024)
        self.assertGreater(len(team), 0)
    
    def test_get_team_roster(self):
        """Test roster retrieval for a team."""
        # Use known data from sample
        year, team = 2020, 'Los Angeles Dodgers'
        roster = self.game.get_team_roster(year, team)
        
        self.assertIsInstance(roster, dict)
        # Should have at least some positions
        self.assertGreater(len(roster), 0)
        
        # Check that all positions are valid
        for position in roster.keys():
            self.assertIn(position, self.game.POSITIONS)

class TestAccessibility(unittest.TestCase):
    """Test cases for accessibility features."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_form_labels(self):
        """Test that form inputs have proper labels."""
        response = self.app.get('/')
        html_content = response.data.decode('utf-8')
        
        # Check that each input has an associated label
        positions = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']
        for position in positions:
            self.assertIn(f'for="{position}"', html_content)
            self.assertIn(f'id="{position}"', html_content)
    
    def test_aria_attributes(self):
        """Test that proper ARIA attributes are present."""
        response = self.app.get('/')
        html_content = response.data.decode('utf-8')
        
        # Check for ARIA attributes
        self.assertIn('aria-label', html_content)
        self.assertIn('pattern=', html_content)  # Input patterns for validation
    
    def test_semantic_html(self):
        """Test that semantic HTML elements are used."""
        response = self.app.get('/')
        html_content = response.data.decode('utf-8')
        
        # Check for semantic elements
        self.assertIn('<header', html_content)
        self.assertIn('<main', html_content)
        self.assertIn('<input', html_content)  # Form inputs instead of form tag
        self.assertIn('<table', html_content)

if __name__ == '__main__':
    # Create a test suite
    test_classes = [
        TestBaseballGame,
        TestFlaskRoutes,
        TestDataLoading,
        TestAccessibility
    ]
    
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with error code if tests failed
    exit(0 if result.wasSuccessful() else 1)
