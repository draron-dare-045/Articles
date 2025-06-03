import sqlite3
from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self._id = id
        self._name = None
        self.name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string")
        self._name = value

    def save(self):
        conn = get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                if self._id:
                    cursor.execute(
                        "UPDATE authors SET name = ? WHERE id = ?",
                        (self._name, self._id)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO authors (name) VALUES (?)",
                        (self._name,)
                    )
                    self._id = cursor.lastrowid
                conn.commit()
                return self
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
            row = cursor.fetchone()
            return cls(row['name'], row['id']) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
            row = cursor.fetchone()
            return cls(row['name'], row['id']) if row else None
        finally:
            conn.close()

    def articles(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE author_id = ?",
                (self._id,)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def magazines(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT DISTINCT m.* FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
                """,
                (self._id,)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def add_article(self, magazine, title):
        from .article import Article
        article = Article(title, self, magazine)
        return article.save()

    def topic_areas(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT DISTINCT m.category FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
                """,
                (self._id,)
            )
            return [row['category'] for row in cursor.fetchall()]
        finally:
            conn.close()

    @classmethod
    def most_articles(cls):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT a.*, COUNT(art.id) as article_count
                FROM authors a
                LEFT JOIN articles art ON a.id = art.author_id
                GROUP BY a.id, a.name
                ORDER BY article_count DESC
                LIMIT 1
                """
            )
            row = cursor.fetchone()
            return cls(row['name'], row['id']) if row else None
        finally:
            conn.close()