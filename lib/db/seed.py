from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_data():
    author1 = Author.create("Alice Walker")
    author2 = Author.create("Chinua Achebe")
    author3 = Author.create("Ngugi wa Thiong'o")

    mag1 = Magazine.create("Literary Digest", "Literature")
    mag2 = Magazine.create("African Voices", "Culture")

    Article.create("Why I Write", author1.id, mag1.id)
    Article.create("Roots and Routes", author1.id, mag2.id)
    Article.create("The Storyteller", author2.id, mag2.id)
    Article.create("Language as Resistance", author3.id, mag2.id)
    Article.create("The River Between", author3.id, mag2.id)

    print("data created successfully:")

if __name__ == "__main__":
    seed_data()