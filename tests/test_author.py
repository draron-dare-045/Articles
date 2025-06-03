import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture
def setup_database():
    conn = get_connection()
    try:
        with open('lib/db/schema.sql', 'r') as f:
            schema = f.read()
        with conn:
            conn.executescript(schema)
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO authors (name) VALUES ('John Doe')")
            author_id = cursor.lastrowid
            cursor.execute("INSERT INTO magazines (name, category) VALUES ('Tech Today', 'Technology')")
            magazine_id = cursor.lastrowid
            conn.commit()
        yield {"author_id": author_id, "magazine_id": magazine_id}
    finally:
        conn.close()

def test_author_validation():
    with pytest.raises(ValueError):
        Author("")
    with pytest.raises(ValueError):
        Author(None)

def test_author_save(setup_database):
    author = Author("Jane Smith").save()
    assert author.id is not None
    assert author.name == "Jane Smith"

def test_author_find_by_id(setup_database):
    author = Author.find_by_id(setup_database["author_id"])
    assert author is not None
    assert author.name == "John Doe"

def test_author_articles(setup_database):
    author = Author.find_by_id(setup_database["author_id"])
    magazine = Magazine.find_by_id(setup_database["magazine_id"])
    Article("Test Article", author, magazine).save()
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0]['title'] == "Test Article"