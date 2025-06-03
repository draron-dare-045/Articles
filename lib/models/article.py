import sqlite3
from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author, magazine, id=None):
        self._id = id
        self._title = None
        self._author = author
        self._magazine = magazine
        self.title = title

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string")
        self._title = value

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine

    def save(self):
        conn = get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                if self._id:
                    cursor.execute(
                        "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                        (self._title, self._author.id, self._magazine.id, self._id)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                        (self._title, self._author.id, self._magazine.id)
                    )
                    self._id = cursor.lastrowid
                conn.commit()
                return self
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        from .author import Author
        from .magazine import Magazine
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT a.*, au.name as author_name, m.name as magazine_name, m.category
                FROM articles a
                JOIN authors au ON a.author_id = au.id
                JOIN magazines m ON a.magazine_id = m.id
                WHERE a.id = ?
                """,
                (id,)
            )
            row = cursor.fetchone()
            if row:
                author = Author(row['author_name'], row['author_id'])
                magazine = Magazine(row['magazine_name'], row['category'], row['magazine_id'])
                return cls(row['title'], author, magazine, row['id'])
            return None
        finally:
            conn.close()

    @classmethod
    def find_by_title(cls, title):
        from .author import Author
        from .magazine import Magazine
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT a.*, au.name as author_name, m.name as magazine_name, m.category
                FROM articles a
                JOIN authors au ON a.author_id = au.id
                JOIN magazines m ON a.magazine_id = m.id
                WHERE a.title = ?
                """,
                (title,)
            )
            row = cursor.fetchone()
            if row:
                author = Author(row['author_name'], row['author_id'])
                magazine = Magazine(row['magazine_name'], row['category'], row['magazine_id'])
                return cls(row['title'], author, magazine, row['id'])
            return None
        finally:
            conn.close()