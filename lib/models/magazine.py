from lib.db.connection import get_connection
from lib.models.author import Author
from collections import Counter

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @classmethod
    def create(cls, name, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)",
            (name, category)
        )
        conn.commit()
        mag_id = cursor.lastrowid
        conn.close()
        return cls(mag_id, name, category)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["id"], row["name"], row["category"])
        return None

    def articles(self):
        from lib.models.article import Article  
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row["id"], row["title"], row["author_id"], row["magazine_id"]) for row in rows]

    def contributors(self):
        articles = self.articles()
        author_ids = {a.author_id for a in articles}
        return [Author.find_by_id(aid) for aid in author_ids]

    def article_titles(self):
        return [article.title for article in self.articles()]

    def contributing_authors(self):
        articles = self.articles()
        counts = Counter([a.author_id for a in articles])
        return [Author.find_by_id(aid) for aid, count in counts.items() if count > 1]

    def __repr__(self):
        return f"<Magazine {self.name} - {self.category}>"