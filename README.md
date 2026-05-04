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

Full 52-card deck shuffling and memorization
User registration and authentication
Attempt history tracking with accuracy metrics
Time tracking for each attempt
Progress tracking across multiple attempts
Secure password hashing with Werkzeug
SQLite database for persistent storage

## Technology Stack

**Backend**: Python with Flask web framework
**Database**: SQLite with SQLAlchemy ORM
**Frontend**: HTML/Jinja2 templates with JavaScript
**Authentication**: Flask session management with werkzeug password hashing
**Security**: Password hashing (scrypt method)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/VDeml/fiftytwo-pickup.git
   cd fiftytwo-pickup