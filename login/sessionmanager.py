import os
from datetime import datetime, timedelta
from login.database.UserDatabaseManager import get_user_db_connection

class SessionManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.session_timeout = timedelta(minutes=30)

    def create_session(self, username, ip_address, login_success=True):
        login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with get_user_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT session_id FROM sessions
                WHERE username = ? AND login_time = ?
            ''', (username, login_time))
            
            existing_session = cursor.fetchone()
            if existing_session:
                return existing_session[0]
            else:
                session_id = self._generate_session_id()
                expiration_time = datetime.now() + self.session_timeout

                cursor.execute('''
                    INSERT INTO sessions (session_id, username, expiration_time, login_time, last_activity_time, login_success, ip_address)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (session_id, username, expiration_time, login_time, login_time, login_success, ip_address))
                conn.commit()

                return session_id
        
    def logout(self, session_id):
        logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = self.db_connection.cursor()
        cursor.execute('''
            UPDATE sessions SET logout_time = ? WHERE session_id = ?
        ''', (logout_time, session_id))
        self.db_connection.commit()

        return cursor.rowcount > 0

    def cleanup_sessions(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            DELETE FROM sessions WHERE expiration_time < CURRENT_TIMESTAMP OR last_activity_time < ?
        ''', (datetime.now() - self.session_timeout,))
        self.db_connection.commit()

    def verify_session(self, session_id):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            SELECT username, last_activity_time FROM sessions
            WHERE session_id = ? AND expiration_time > CURRENT_TIMESTAMP
        ''', (session_id,))
        return cursor.fetchone()

    def end_session(self, session_id):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            DELETE FROM sessions WHERE session_id = ? AND logout_time IS NOT NULL
        ''', (session_id,))
        self.db_connection.commit()

        return cursor.rowcount > 0

    def update_last_activity(self, session_id):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            UPDATE sessions SET last_activity_time = ? WHERE session_id = ?
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), session_id))
        self.db_connection.commit()

    def _generate_session_id(self):
        return os.urandom(16).hex()
    
def create_session_table():
    with get_user_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                expiration_time DATETIME NOT NULL,
                login_time DATETIME NOT NULL,
                logout_time DATETIME,
                last_activity_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                login_success BOOLEAN NOT NULL DEFAULT 0,
                ip_address TEXT NOT NULL  
            )
        ''')
        conn.commit()

create_session_table()
