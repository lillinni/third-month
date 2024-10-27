import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path
    
    def create_tables(self):
        with sqlite3.connect(self.path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS survey_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, 
                    phone_number TEXT,
                    visit_date TEXT,
                    food_rating INTEGER,
                    cleanliness_rating INTEGER,
                    extra_comments TEXT,
                    tg_id INTEGER                         
            )
        """)

        connection.commit()