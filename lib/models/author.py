from lib.db.connection import get_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        conn.commit()
        author_id = cursor.lastrowid
        conn.close()
        return cls(author_id, name)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["id"], row["name"])
        return None

    def articles(self):
        from lib.models.article import Article  
        return Article.find_by_author(self.id)

    def magazines(self):

        articles = self.articles()
        magazines = {article.magazine() for article in articles}
        return list(magazines)

    def __repr__(self):
        return f"<Author {self.name}>"
