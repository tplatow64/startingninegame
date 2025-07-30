# Baseball Position Guessing Game

A web-based interactive game where users guess player names for specific positions on randomly selected baseball teams from World Series champions (2000-2023).

## Features

- **Interactive Baseball Diamond**: Visual representation of baseball positions with input fields
- **Random Team Selection**: Automatically selects a random World Series champion team from 2000-2023
- **Fuzzy Name Matching**: Accepts player names that are within 2 characters of the correct answer
- **Real-time Input Validation**: Sanitizes input to only allow alphabetic characters
- **Comprehensive Results**: Shows detailed feedback for each guess with correct answers
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Accessibility Compliant**: WCAG 2.1 AA compliant with screen reader support
- **Unit Testing**: Complete test coverage for all functionality

## Requirements

- Python 3.7+
- Flask 2.3+
- Modern web browser with JavaScript enabled

## Installation

1. **Clone or download the project files to your local machine**

2. **Navigate to the project directory**:
   ```bash
   cd baseball-position-game
   ```

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

1. **Start the Flask development server**:
   ```bash
   python app.py
   ```

2. **Open your web browser and navigate to**:
   ```
   http://localhost:5000
   ```

3. **Play the game**:
   - A random team and year will be displayed
   - Enter player names in the input fields for each position
   - Click "Submit Guesses" to see your results
   - Click "New Game" to try with a different team

### Game Rules

- **Objective**: Guess the correct player names for each position on the displayed team
- **Input**: Enter first and last names (e.g., "Derek Jeter")
- **Validation**: Only alphabetic characters and spaces are allowed
- **Scoring**: 
  - Exact matches are counted as correct
  - Names within 2 characters of the correct answer are accepted (fuzzy matching)
  - Empty fields are marked as "No guess made"
- **Positions Included**: All field positions except pitcher
- **Designated Hitter**: Only shown for American League teams that used a DH

### Data Source

The game includes data for World Series champion teams from 2000-2023, featuring the starting lineups for each position. The data is stored in `baseball_data.csv` and includes:

- Year and team name
- Player positions (C, 1B, 2B, 3B, SS, LF, CF, RF, DH)
- Player names and games played

## Testing

### Running Unit Tests

Run the complete test suite:
```bash
python test_app.py
```

### Test Coverage

The test suite includes:
- **Game Logic Tests**: Input sanitization, name comparison, fuzzy matching
- **Flask Route Tests**: All endpoints and error handling
- **Data Loading Tests**: CSV parsing and team selection
- **Accessibility Tests**: ARIA attributes, semantic HTML, form labels

## Project Structure

```
baseball-position-game/
├── app.py                 # Main Flask application
├── test_app.py           # Unit tests
├── baseball_data.csv     # Game data (World Series champions 2000-2023)
├── requirements.txt      # Python dependencies
├── requirements.md       # Project requirements document
├── README.md            # This file
├── CHANGELOG.md         # Version history
├── static/
│   ├── css/
│   │   └── style.css    # Application styles
│   └── js/
│       └── game.js      # Client-side game logic
└── templates/
    └── index.html       # Main game template
```

## Configuration

### Environment Variables

For production deployment, set the following environment variables:

- `SECRET_KEY`: Flask secret key for session management
- `FLASK_ENV`: Set to "production" for production deployment

### Customization

- **Add More Teams**: Edit `baseball_data.csv` to include additional teams and years
- **Modify Fuzzy Matching**: Adjust the similarity threshold in the `compare_names()` method
- **Change Styling**: Modify `static/css/style.css` for custom appearance
- **Update Game Logic**: Edit the `BaseballGame` class in `app.py`

## Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+
- Internet Explorer 11+ (limited support)

## Accessibility Features

- **Keyboard Navigation**: Tab through all interactive elements
- **Screen Reader Support**: Proper ARIA labels and semantic HTML
- **High Contrast Mode**: Supports Windows high contrast themes
- **Reduced Motion**: Respects user's motion preferences
- **Focus Management**: Clear focus indicators and logical tab order

## Security Features

- **Input Sanitization**: All user input is cleaned server-side
- **CSRF Protection**: Flask session management with secure secret key
- **XSS Prevention**: Template escaping enabled by default
- **Input Validation**: Client and server-side validation

## Performance

- **Lightweight**: Minimal JavaScript and CSS for fast loading
- **Efficient**: O(1) data lookup for team rosters
- **Responsive**: CSS Grid and Flexbox for optimal layout
- **Caching**: Static assets can be cached by browsers

## Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Use a different port
   python app.py --port 5001
   ```

2. **Missing Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **CSV File Not Found**:
   - Ensure `baseball_data.csv` is in the project root directory
   - The app will create sample data if the file is missing

4. **JavaScript Errors**:
   - Check browser console for errors
   - Ensure JavaScript is enabled
   - Try refreshing the page

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is for educational purposes. Baseball statistics and player names are used under fair use guidelines.

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review the test cases for expected behavior
3. Check browser console for JavaScript errors
4. Ensure all requirements are properly installed
