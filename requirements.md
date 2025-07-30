# Baseball Position Guessing Game - Requirements

## Project Overview
A web-based baseball game where users guess player names for specific positions on a randomly selected team from a given year.

## Technical Requirements

### Framework & Technology
1. Must be written in Flask (Python web framework)
2. Must have unit tests for all interfaces
3. All code must follow Python coding standards and best practices (PEP 8, PEP 257, etc.)

### Data Requirements
4. The spreadsheet must be in CSV format with columns: `year`, `team`, `position`, `player_name`, `games_played`
5. All name comparisons should be case-insensitive and ignore leading/trailing whitespace
6. Support fuzzy matching (names within 2 characters of correct name are considered correct)

### Security & Validation
7. All user input must be sanitized and validated on the server side
8. All user input must be limited to alpha characters only in the input boxes

### UI/UX Requirements
9. The UI must be responsive and accessible (WCAG 2.1 AA compliant)
10. Starting page should display a baseball diamond layout
11. Each field position should have a text field for entering player name guesses
12. Exclude pitcher position from the guessing game
13. Only show designated hitter field if the team uses a designated hitter
14. Users enter first name and last name for each position
15. Single submit button to submit all guesses at once

### Documentation Requirements
16. The project must include a README file with setup instructions, usage, and description
17. The project must include a CHANGELOG file to track all significant changes and updates

## Game Flow

### 1. Game Initialization
- Randomly pick a year from 2000 through 2024
- Query the data to select a random team from the selected year
- Load the team's roster for that year

### 2. User Interface
- Display baseball diamond with interactive text fields for each position
- Position fields (excluding pitcher):
  - Catcher
  - First Base
  - Second Base
  - Third Base
  - Shortstop
  - Left Field
  - Center Field
  - Right Field
  - Designated Hitter (if applicable)

### 3. Game Processing
For each filled field:
- Check if the entered name matches the actual player at that position
- **Correct Match**: Display success message
- **Incorrect Match**: Display error message and show the correct name
- **Fuzzy Match**: Accept names within 2 characters of correct name
- **Empty Field**: Display message indicating no guess was made

### 4. Results Display
- Show a comprehensive results table with:
  - All positions
  - User guesses
  - Correct answers
  - Feedback for each guess
- Display total number of correct guesses
- Calculate and show percentage correct

## Success Criteria
- Functional web application built with Flask
- Complete unit test coverage
- Responsive and accessible user interface
- Accurate game logic with fuzzy matching
- Proper input validation and security measures
- Complete documentation (README and CHANGELOG)