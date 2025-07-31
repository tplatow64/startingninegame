/**
 * Baseball Position Guessing Game - Client-side JavaScript
 */

class BaseballGame {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupInputValidation();
        this.setupAccessibility();
    }

    bindEvents() {
        // Submit button event
        const submitButton = document.getElementById('submitGuesses');
        if (submitButton) {
            submitButton.addEventListener('click', () => this.submitGuesses());
        }

        // New game button event
        const newGameButton = document.getElementById('newGame');
        if (newGameButton) {
            newGameButton.addEventListener('click', () => this.startNewGame());
        }

        // Enter key submission
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !this.isSubmitting) {
                e.preventDefault();
                this.submitGuesses();
            }
        });
    }

    setupInputValidation() {
        // Get all position input fields
        const inputFields = document.querySelectorAll('.position-field');
        
        inputFields.forEach(field => {
            // Less aggressive input validation - only validate on blur
            field.addEventListener('blur', (e) => {
                this.validateInput(e.target);
            });

            // Clear validation styles on focus
            field.addEventListener('focus', (e) => {
                e.target.classList.remove('correct', 'incorrect');
            });
            
            // Allow typing naturally - only block obviously invalid characters
            field.addEventListener('keypress', (e) => {
                const char = e.key;
                // Allow letters, spaces, backspace, delete, tab, enter, arrow keys
                if (char.length === 1 && !/[a-zA-Z\s'. ]/.test(char)) {
                    e.preventDefault();
                }
            });
        });
    }

    setupAccessibility() {
        // Add ARIA labels and descriptions
        const inputFields = document.querySelectorAll('.position-field');
        
        inputFields.forEach(field => {
            const label = field.previousElementSibling;
            if (label && label.classList.contains('position-label')) {
                field.setAttribute('aria-describedby', `${field.id}-help`);
                field.setAttribute('aria-label', `Enter player name for ${label.textContent}`);
            }
        });

        // Add keyboard navigation support
        this.setupKeyboardNavigation();
    }

    setupKeyboardNavigation() {
        const inputFields = document.querySelectorAll('.position-field');
        
        inputFields.forEach((field, index) => {
            field.addEventListener('keydown', (e) => {
                // Only handle Tab for navigation, let arrow keys work normally in text fields
                if (e.key === 'Tab') {
                    // Default tab behavior is fine, no need to override
                    return;
                }
                
                // Remove arrow key navigation - let them work normally in text input
                // Arrow keys should move cursor within the text field, not between fields
            });
        });
    }

    validateInput(field) {
        const value = field.value;
        const sanitized = this.sanitizeInput(value);
        
        // Only update if there's a meaningful difference (not just cursor position)
        if (value !== sanitized && sanitized !== value.replace(/[^a-zA-Z\s'. ]/g, '')) {
            const cursorPos = field.selectionStart;
            field.value = sanitized;
            // Try to maintain cursor position, but don't interfere with space typing
            if (cursorPos <= sanitized.length) {
                field.setSelectionRange(cursorPos, cursorPos);
            }
        }

        // Visual feedback for valid/invalid input
        if (sanitized && sanitized.length > 0) {
            field.classList.add('is-valid');
            field.classList.remove('is-invalid');
        } else {
            field.classList.remove('is-valid', 'is-invalid');
        }
    }

    sanitizeInput(input) {
        if (!input) return '';
        
        // Remove non-alphabetic characters except spaces
        let sanitized = input.replace(/[^a-zA-Z\s'. ]/g, '');
        
        // Remove extra spaces (keep single spaces between words)
        sanitized = sanitized.replace(/\s+/g, ' ');
        
        // Trim leading/trailing spaces
        sanitized = sanitized.trim();
        
        return sanitized;
    }

    async submitGuesses() {
        if (this.isSubmitting) return;
        
        try {
            this.isSubmitting = true;
            this.showLoading(true);
            
            // Get all form data
            const formData = new FormData();
            const inputFields = document.querySelectorAll('.position-field');
            let hasGuesses = false;
            
            inputFields.forEach(field => {
                const value = this.sanitizeInput(field.value);
                formData.append(field.name, value);
                if (value) hasGuesses = true;
            });

            // Check if user made any guesses
            if (!hasGuesses) {
                this.showError('Please enter at least one player name before submitting.');
                return;
            }

            // Submit to server
            const response = await fetch('/submit_guesses', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            // Display results
            this.displayResults(data);
            
        } catch (error) {
            console.error('Error submitting guesses:', error);
            this.showError('An error occurred while submitting your guesses. Please try again.');
        } finally {
            this.isSubmitting = false;
            this.showLoading(false);
        }
    }

    displayResults(data) {
        // Hide submit button, show new game button
        document.getElementById('submitGuesses').style.display = 'none';
        document.getElementById('newGame').style.display = 'inline-block';

        // Update score summary
        document.getElementById('correctCount').textContent = data.correct_count;
        document.getElementById('totalPlayers').textContent = data.num_players;
        document.getElementById('percentage').textContent = `${data.percentage}%`;

        // Update results table
        this.updateResultsTable(data.results);

        // Update input fields with results
        this.updateInputFields(data.results);

        // Show results section
        document.getElementById('resultsSection').style.display = 'block';

        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });

        // Announce results for screen readers
        this.announceResults(data);
    }

    updateResultsTable(results) {
        const tbody = document.getElementById('resultsTableBody');
        tbody.innerHTML = '';

        const positions = {
            'C': 'Catcher',
            '1B': 'First Base',
            '2B': 'Second Base',
            '3B': 'Third Base',
            'SS': 'Shortstop',
            'LF': 'Left Field',
            'CF': 'Center Field',
            'RF': 'Right Field',
            'DH': 'Designated Hitter'
        };

        for (const [position, positionName] of Object.entries(positions)) {
            if (results[position]) {
                const result = results[position];
                const row = document.createElement('tr');
                
                const guess = result.guess || 'No guess';
                const resultClass = result.correct ? 'result-correct' : 
                                  result.guess ? 'result-incorrect' : 'result-no-guess';
                
                row.innerHTML = `
                    <td><strong>${positionName}</strong></td>
                    <td>${guess}</td>
                    <td>${result.actual}</td>
                    <td class="${resultClass}">${result.message}</td>
                `;
                
                tbody.appendChild(row);
            }
        }
    }

    updateInputFields(results) {
        for (const [position, result] of Object.entries(results)) {
            const field = document.getElementById(position);
            if (field) {
                // Add visual feedback classes
                field.classList.remove('is-valid', 'is-invalid');
                if (result.correct) {
                    field.classList.add('correct');
                } else if (result.guess) {
                    field.classList.add('incorrect');
                }

                // Disable the field
                field.disabled = true;

                // Add ARIA label with result
                field.setAttribute('aria-label', 
                    `${field.getAttribute('aria-label')} - ${result.message}`);
            }
        }
    }

    announceResults(data) {
        // Create announcement for screen readers
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = 
            `Game complete! You got ${data.correct_count} out of ${data.total_guesses} correct, ` +
            `which is ${data.percentage}% accuracy.`;
        
        document.body.appendChild(announcement);
        
        // Remove after announcement
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 3000);
    }

    startNewGame() {
        window.location.href = '/new_game';
    }

    showLoading(show) {
        const spinner = document.getElementById('loadingSpinner');
        const submitButton = document.getElementById('submitGuesses');
        
        if (show) {
            spinner.style.display = 'block';
            submitButton.disabled = true;
            submitButton.textContent = 'Submitting...';
        } else {
            spinner.style.display = 'none';
            submitButton.disabled = false;
            submitButton.textContent = 'Submit Guesses';
        }
    }

    showError(message) {
        const errorModal = document.getElementById('errorModal');
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.textContent = message;
        
        // Show modal using Bootstrap
        const modal = new bootstrap.Modal(errorModal);
        modal.show();
    }
}

// Utility class for accessibility improvements
class AccessibilityHelper {
    static addSkipLink() {
        const skipLink = document.createElement('a');
        skipLink.href = '#main';
        skipLink.textContent = 'Skip to main content';
        skipLink.className = 'sr-only sr-only-focusable';
        skipLink.style.cssText = `
            position: absolute;
            top: -40px;
            left: 6px;
            z-index: 9999;
            color: white;
            background: #000;
            padding: 8px;
            text-decoration: none;
            border-radius: 4px;
        `;
        
        skipLink.addEventListener('focus', () => {
            skipLink.style.top = '6px';
        });
        
        skipLink.addEventListener('blur', () => {
            skipLink.style.top = '-40px';
        });
        
        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    static improveFormLabels() {
        const fields = document.querySelectorAll('.position-field');
        fields.forEach(field => {
            if (!field.getAttribute('aria-describedby')) {
                const helpId = `${field.id}-help`;
                field.setAttribute('aria-describedby', helpId);
                
                const helpText = document.createElement('div');
                helpText.id = helpId;
                helpText.className = 'sr-only';
                helpText.textContent = 'Enter the first and last name of the player for this position. Only letters and spaces are allowed.';
                
                field.parentNode.appendChild(helpText);
            }
        });
    }
}

// Initialize the game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new BaseballGame();
    AccessibilityHelper.addSkipLink();
    AccessibilityHelper.improveFormLabels();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Page is hidden, could pause any ongoing operations
    } else {
        // Page is visible again
    }
});

// Handle online/offline status
window.addEventListener('online', () => {
    console.log('Connection restored');
});

window.addEventListener('offline', () => {
    console.log('Connection lost');
});
