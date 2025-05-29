
import pytest
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine

def test_create_and_find_author():
    author = Author.create("Test Author")
    found = Author.find_by_id(author.id)
    assert found is not None
    assert found.name == "Test Author"

def test_author_articles_and_magazines():
    author = Author.create("Test Writer")
    mag = Magazine.create("Test Mag", "Test Category")
    art1 = Article.create("Test Article 1", author.id, mag.id)
    art2 = Article.create("Test Article 2", author.id, mag.id)

    articles = author.articles()
    magazines = author.magazines()

    assert len(articles) >= 2
    assert any(a.title == "Test Article 1" for a in articles)
    assert any(m.name == "Test Mag" for m in magazines)