import sqlite3
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def get_connection():
    return sqlite3.connect('database.db')

def seed_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

    authors = [
        Author("John Doe"),
        Author("Jane Smith"),
        Author("Bob Johnson")
    ]
    for author in authors:
        author.save()

    magazines = [
        Magazine("Tech Today", "Technology"),
        Magazine("Science Weekly", "Science"),
        Magazine("Business Insights", "Business")
    ]
    for magazine in magazines:
        magazine.save()

    articles = [
        Article("The Future of AI", authors[0].id, magazines[0].id),
        Article("Quantum Computing", authors[1].id, magazines[1].id),
        Article("Market Trends", authors[2].id, magazines[2].id),
        Article("Python Programming", authors[0].id, magazines[0].id),
        Article("Space Exploration", authors[1].id, magazines[1].id),
        Article("Startup Funding", authors[2].id, magazines[2].id),
        Article("Machine Learning", authors[0].id, magazines[0].id),
        Article("Genetic Engineering", authors[1].id, magazines[1].id)
    ]
    for article in articles:
        article.save()

    print("Database seeded successfully!")