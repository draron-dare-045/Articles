
import pytest
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine

def test_create_and_find_article():
    author = Author.create("Article Author")
    mag = Magazine.create("World View", "News")
    article = Article.create("Breaking Views", author.id, mag.id)

    assert article.title == "Breaking Views"
    assert article.magazine().name == "World View"