# Articles Code Challenge

This project is a Python-based application designed to manage authors, articles, and magazines. It includes a database schema, models for interacting with the database, controllers for handling transactions, and tests to ensure the functionality of the application.

## Project Structure

The project is organized into the following directories:
articles-code-challenge/ ├── lib/ │ ├── db/ │ │ ├── connection.py │ │ ├── schema.sql │ ├── models/ │ │ ├── init.py │ │ ├── author.py │ │ ├── article.py │ │ ├── magazine.py ├── controllers/ │ ├── transactions.py ├── tests/ │ ├── init.py │ ├── test_author.py │ ├── test_article.py │ ├── test_magazine.py


### Key Components

#### 1. **Database**
- **`lib/db/schema.sql`**: Defines the database schema, including tables for authors, articles, and magazines.
- **`lib/db/connection.py`**: Provides a function to establish a connection to the SQLite database.

#### 2. **Models**
- **`lib/models/author.py`**: Defines the `Author` model, which represents authors in the database.
- **`lib/models/article.py`**: Defines the `Article` model, which represents articles written by authors and associated with magazines.
- **`lib/models/magazine.py`**: Defines the `Magazine` model, which represents magazines that contain articles.

#### 3. **Controllers**
- **`controllers/transactions.py`**: Contains the `add_author_with_articles` function, which handles adding an author and their articles in a single database transaction.

#### 4. **Tests**
- **`tests/test_author.py`**: Contains tests for the `Author` model.
- **`tests/test_article.py`**: Contains tests for the `Article` model.
- **`tests/test_magazine.py`**: Contains tests for the `Magazine` model, including database setup and validation.

## Features

### Models
- **Author**: Represents an author with attributes like `id` and `name`.
- **Article**: Represents an article with attributes like `id`, `title`, `author_id`, and `magazine_id`.
- **Magazine**: Represents a magazine with attributes like `id`, `name`, and `category`.

### Transactions
- **Add Author with Articles**: The `add_author_with_articles` function in `transactions.py` allows adding an author and their articles in a single transaction. If any part of the transaction fails, it rolls back the changes.

### Testing
- The project uses `pytest` for testing.
- Fixtures are used to set up the database for tests.
- Tests cover model validation, saving records, and relationships between authors, articles, and magazines.

## Setup and Usage

### Prerequisites
- Python 3.13 or higher
- SQLite

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd articles-code-challenge