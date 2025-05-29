
import pytest
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine

def test_magazine_articles_and_contributors():
    author = Author.create("Mag Author")
    mag = Magazine.create("Tech Monthly", "Technology")
    Article.create("AI in 2025", author.id, mag.id)
    Article.create("Quantum Boom", author.id, mag.id)

    articles = mag.articles()
    contributors = mag.contributors()

    assert len(articles) >= 2
    assert any(a.title == "AI in 2025" for a in articles)
    assert any(a.name == "Mag Author" for a in contributors)