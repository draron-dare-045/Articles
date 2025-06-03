from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database

def run_queries():
    print("Seeding database...")
    seed_database()
    print("Database seeded successfully!\n")

    print("Example 1: Get all articles written by John Doe")
    john = Author.find_by_name("John Doe")
    john_articles = john.articles()
    for article in john_articles:
        print(f"- {article['title']}")
    print()

    print("Example 2: Find all magazines Jane Smith has contributed to")
    jane = Author.find_by_name("Jane Smith")
    jane_magazines = jane.magazines()
    for magazine in jane_magazines:
        print(f"- {magazine['name']} ({magazine['category']})")
    print()

    print("Example 3: Get all authors who have written for Tech Today")
    tech_today = Magazine.find_by_name("Tech Today")
    tech_authors = tech_today.contributors()
    for author in tech_authors:
        print(f"- {author['name']}")
    print()

    print("Example 4: Magazines with articles by at least 2 authors")
    all_magazines = Magazine.get_all()
    for magazine in all_magazines:
        authors_count = len(magazine.contributors())
        if authors_count >= 2:
            print(f"- {magazine.name} has {authors_count} authors")
    print()

    print("Example 5: Article count per magazine")
    for magazine in all_magazines:
        count = len(magazine.articles())
        print(f"- {magazine.name}: {count} articles")
    print()

    print("Example 6: Author with most articles")
    authors = Author.get_all()
    max_articles = 0
    top_author = None
    for author in authors:
        article_count = len(author.articles())
        if article_count > max_articles:
            max_articles = article_count
            top_author = author
    print(f"- {top_author.name} with {max_articles} articles")
    print()

    print("Example 7: Article titles in Science Weekly")
    science_weekly = Magazine.find_by_name("Science Weekly")
    titles = science_weekly.article_titles()
    for title in titles:
        print(f"- {title}")
    print()

    print("Example 8: Contributing authors to Tech Today (with >2 articles)")
    tech_today = Magazine.find_by_name("Tech Today")
    john = Author.find_by_name("John Doe")
    Article("Another Tech Article", john.id, tech_today.id).save()
    Article("Yet Another Tech Article", john.id, tech_today.id).save()
    
    contributors = tech_today.contributing_authors()
    if contributors:
        for author in contributors:
            print(f"- {author['name']}")
    else:
        print("No authors with more than 2 articles in this magazine")
    print()

    print("Example 9: Jane Smith's topic areas")
    jane = Author.find_by_name("Jane Smith")
    topics = jane.topic_areas()
    for topic in topics:
        print(f"- {topic}")
    print()

    print("Example 10: Magazine with most articles")
    top_publisher = Magazine.top_publisher()
    print(f"- {top_publisher.name} with {len(top_publisher.articles())} articles")

if __name__ == '__main__':
    run_queries()