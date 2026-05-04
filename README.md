# Fifty-Two Pickup

#### Video Demo:  <https://youtu.be/0OiBJzwWpZI>

#### Description:

A web-based application for practicing memory disciplines through the classic card memorization challenge of recalling a shuffled deck of 52 playing cards.

## About

**Fifty-Two Pickup** is designed for memory athletes and enthusiasts who want to improve their card memorization skills. The application presents a shuffled deck of 52 playing cards, gives you time to memorize the order, and then challenges you to recall the entire sequence from memory.

### How It Works

1. **Shuffle**: Click the shuffle button to generate and display a randomized deck of 52 cards
2. **Memorize**: Study the card order as it's displayed on screen
3. **Recall**: Input the cards in the order you remember them
4. **Score**: Get instant feedback on your accuracy, including:
   - Accuracy percentage
   - Number of correctly placed cards
   - Time taken to complete the challenge
5. **History**: View your historical attempts and progress over time

## Features

- 🎴 Full 52-card deck shuffling and memorization
- 👤 User registration and authentication
- 📊 Attempt history tracking with accuracy metrics
- ⏱️ Time tracking for each attempt
- 📈 Progress tracking across multiple attempts
- 🔐 Secure password hashing with Werkzeug
- 💾 SQLite database for persistent storage

## Technology Stack

- **Backend**: Python with Flask web framework
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML/Jinja2 templates with JavaScript
- **Authentication**: Flask session management with werkzeug password hashing
- **Security**: Password hashing (scrypt method)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/VDeml/fiftytwo-pickup.git
   cd fiftytwo-pickup
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**:
   ```bash
   python init_db.py
   ```

5. **Run the application**:
   ```bash
   flask run
   ```

The application will be available at `http://localhost:5000`

## Configuration

Create a `.flaskenv` file in the project root to configure Flask:

```
FLASK_APP=app.py
FLASK_ENV=development
```

## Project Structure

```
fiftytwo-pickup/
├── app.py              # Main Flask application
├── helpers.py          # Utility functions and decorators
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── .flaskenv          # Flask configuration
├── .gitignore         # Git ignore rules
├── static/            # Static files (CSS, JavaScript, images)
└── templates/         # HTML templates
```

## Usage

### Registration

1. Navigate to the application home page
2. Click "Register" to create a new account
3. Enter a username, email, and password
4. Confirm your password and submit

### Playing

1. Log in with your credentials
2. Click "Play" or "Shuffle" to start a new attempt
3. Study the displayed card deck
4. When ready, proceed to recall the cards
5. Enter each card in order using the interface
6. Submit your answer to see your score

### Viewing History

- Click "History" to view all your past attempts
- See detailed statistics including accuracy, duration, and card-by-card breakdown

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Securely hashed password
- `created_at`: Account creation timestamp

### Attempts Table
- `id`: Primary key
- `user_id`: Foreign key to users table
- `deck_order`: JSON-encoded shuffled deck order
- `recall_order`: JSON-encoded user's recalled card order
- `accuracy`: Accuracy percentage (0-100)
- `duration_seconds`: Time taken to complete the attempt
- `created_at`: Attempt timestamp

## Security Notes

⚠️ **Important**: The current implementation stores the Flask SECRET_KEY in plain text in `app.py`. For production deployment:
- Store the SECRET_KEY in an environment variable
- Use a strong, randomly generated key
- Never commit sensitive keys to version control

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to help improve the application.

## License

This project is unlicensed. See the repository for more details.

## Future Enhancements

Potential features for future development:
- Multiple card system variations
- Advanced memorization techniques (Major System, Dominic System, etc.)
- Leaderboards and competitions
- Statistics and analytics dashboard
- Mobile app version
- Dark mode interface
- Export attempt data

## Troubleshooting

**Database issues**: Delete the `instance/database.db` file and run `python init_db.py` again to reset the database.

**Port already in use**: Change the Flask port with:
```bash
flask run --port 5001
```

## Support

For issues, questions, or suggestions, please open a GitHub issue on the repository.

---

**Happy memorizing!** 🧠
