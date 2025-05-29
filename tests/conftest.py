
import pytest
from lib.db.connection import get_connection

@pytest.fixture(scope='session', autouse=True)
def initialize_db():
    conn = get_connection()
    with open('lib/db/schema.sql', 'r') as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
