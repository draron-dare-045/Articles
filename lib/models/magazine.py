import sqlite3
from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self._id = id
        self._name = None
        self._category = None
        self.name = name
        self.category = category

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

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Category must be a non-empty string")
        self._category = value

    def save(self):
        conn = get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                if self._id:
                    cursor.execute(
                        "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                        (self._name, self._category, self._id)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO magazines (name, category) VALUES (?, ?)",
                        (self._name, self._category)
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
            cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
            row = cursor.fetchone()
            return cls(row['name'], row['category'], row['id']) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
            row = cursor.fetchone()
            return cls(row['name'], row['category'], row['id']) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
            rows = cursor.fetchall()
            return [cls(row['name'], row['category'], row['id']) for row in rows]
        finally:
            conn.close()

    def articles(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE magazine_id = ?",
                (self._id,)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def contributors(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT DISTINCT a.* FROM authors a
                JOIN articles art ON a.id = art.author_id
                WHERE art.magazine_id = ?
                """,
                (self._id,)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def article_titles(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT title FROM articles WHERE magazine_id = ?",
                (self._id,)
            )
            return [row['title'] for row in cursor.fetchall()]
        finally:
            conn.close()

    def contributing_authors(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT a.* FROM authors a
                JOIN articles art ON a.id = art.author_id
                WHERE art.magazine_id = ?
                GROUP BY a.id, a.name
                HAVING COUNT(*) > 2
                """,
                (self._id,)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT m.*, COUNT(a.id) as article_count
                FROM magazines m
                LEFT JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id, m.name, m.category
                ORDER BY article_count DESC
                LIMIT 1
                """
            )
            row = cursor.fetchone()
            return cls(row['name'], row['category'], row['id']) if row else None
        finally:
            conn.close()

    @classmethod
    def magazines_with_multiple_authors(cls):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT m.*, COUNT(DISTINCT a.author_id) as author_count
                FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id, m.name, m.category
                HAVING author_count >= 2
                """
            )
            rows = cursor.fetchall()
            return [cls(row['name'], row['category'], row['id']) for row in rows]
        finally:
            conn.close()

    @classmethod
    def article_counts(cls):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT m.name, COUNT(a.id) as article_count
                FROM magazines m
                LEFT JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id, m.name
                """
            )
            return {row['name']: row['article_count'] for row in cursor.fetchall()}
        finally:
            conn.close()