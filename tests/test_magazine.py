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
            author1_id = cursor.lastrowid
            cursor.execute("INSERT INTO authors (name) VALUES ('Jane Smith')")
            author2_id = cursor.lastrowid
            cursor.execute("INSERT INTO magazines (name, category) VALUES ('Tech Today', 'Technology')")
            magazine_id = cursor.lastrowid
            conn.commit()
        yield {"author1_id": author1_id, "author2_id": author2_id, "magazine_id": magazine_id}
    finally:
        conn.close()

def test_magazine_validation():
    with pytest.raises(ValueError):
        Magazine("", "Technology")
    with pytest.raises(ValueError):
        Magazine("Tech Today", "")

def test_magazine_save(setup_database):
    magazine = Magazine("Science Weekly", "Science").save()
    assert magazine.id is not None
    assert magazine.name == "Science Weekly"
    assert magazine.category == "Science"

def test_magazine_contributors(setup_database):
    author1 = Author.find_by_id(setup_database["author1_id"])
    author2 = Author.find_by_id(setup_database["author2_id"])
    magazine = Magazine.find_by_id(setup_database["magazine_id"])
    Article("Article 1", author1, magazine).save()
    Article("Article 2", author2, magazine).save()
    contributors = magazine.contributors()
    assert len(contributors) == 2