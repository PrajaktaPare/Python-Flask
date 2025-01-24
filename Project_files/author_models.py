import mysql.connector

class AuthorsModel:
    def __init__(self):
        self.conn = self.get_db_connection()

    def get_db_connection(self):
        return mysql.connector.connect(
            host="localhost",
            database="bookauradb",
            user="root",
            password="root"
        )

    # Fetch all authors
    def fetch_all_authors(self):
        cur = self.conn.cursor(dictionary=True)
        query = '''
            SELECT a.author_id, u.user_id, u.username, u.email, a.bio, a.is_verified, a.is_flagged, a.is_approved
            FROM authors a
            JOIN users u ON a.user_id = u.user_id
        '''
        cur.execute(query)
        authors = cur.fetchall()
        cur.close()
        return authors

    # Fetch an author by author_id
    def fetch_author_by_id(self, author_id):
        cur = self.conn.cursor(dictionary=True)
        query = '''
            SELECT a.author_id, u.user_id, u.username, u.email, a.bio, a.is_verified, a.is_flagged, a.is_approved
            FROM authors a
            JOIN users u ON a.user_id = u.user_id
            WHERE a.author_id = %s
        '''
        cur.execute(query, (author_id,))
        author = cur.fetchone()
        cur.close()
        return author

    # Create a new author
    def create_author(self, username, email, password_hash, bio):
        cur = self.conn.cursor()
        try:
            # Insert into the users table first
            user_query = 'INSERT INTO users (username, email, password_hash, role_id) VALUES (%s, %s, %s, %s)'
            cur.execute(user_query, (username, email, password_hash, 2))  # role_id = 2 for authors
            user_id = cur.lastrowid

            # Insert into the authors table
            author_query = 'INSERT INTO authors (user_id, bio) VALUES (%s, %s)'
            cur.execute(author_query, (user_id, bio))

            self.conn.commit()
            author_id = cur.lastrowid
            return author_id
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    # Update author details
    def update_author(self, author_id, username, email, password_hash, bio, is_verified, is_flagged, is_approved):
        cur = self.conn.cursor()
        try:
            # Update the users table
            user_query = '''
                UPDATE users
                SET username = %s, email = %s, password_hash = %s
                WHERE user_id = (SELECT user_id FROM authors WHERE author_id = %s)
            '''
            cur.execute(user_query, (username, email, password_hash, author_id))

            # Update the authors table
            author_query = '''
                UPDATE authors
                SET bio = %s, is_verified = %s, is_flagged = %s, is_approved = %s
                WHERE author_id = %s
            '''
            cur.execute(author_query, (bio, is_verified, is_flagged, is_approved, author_id))

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    # Delete an author
    def delete_author(self, author_id):
        cur = self.conn.cursor()
        try:
            # First delete from the authors table
            cur.execute('DELETE FROM authors WHERE author_id = %s', (author_id,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    # Authenticate an author by email and password
    def authenticate_author(self, email, password_hash):
        cur = self.conn.cursor(dictionary=True)
        query = '''
            SELECT a.author_id, u.user_id, u.username, u.email
            FROM authors a
            JOIN users u ON a.user_id = u.user_id
            WHERE u.email = %s AND u.password_hash = %s
        '''
        cur.execute(query, (email, password_hash))
        author = cur.fetchone()
        cur.close()
        return author

    # Close the database connection
    def close_connection(self):
        self.conn.close()
