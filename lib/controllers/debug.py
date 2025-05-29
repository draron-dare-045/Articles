
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def test():
    authors = [Author.find_by_id(1), Author.find_by_id(2), Author.find_by_id(3)]
    for author in authors:
        print(author)
        print("Articles:", author.articles())
        print("Magazines:", author.magazines())

    mag = Magazine.find_by_id(2)
    print(mag)
    print("Contributors:", mag.contributors())
    print("Titles:", mag.article_titles())
    print("Power authors:", mag.contributing_authors())

if __name__ == "__main__":
    test()