import sqlite3

class SQLreader:
    def __init__(self, route):
        self.route = route

    def get(self, expression, variables=()):
        connection = sqlite3.connect(self.route, check_same_thread=False)
        cursor = connection.cursor()

        data = cursor.execute(expression, variables).fetchone()
        # close connection and return data
        connection.close()
        return data
    
    def getall(self, expression, variables=()):
        connection = sqlite3.connect(self.route, check_same_thread=False)
        cursor = connection.cursor()

        data = cursor.execute(expression, variables).fetchall()
        # close connection and return data
        connection.close()
        return data
    
    def set(self, expression, variables=()):
        connection = sqlite3.connect(self.route, check_same_thread=False)
        cursor = connection.cursor()

        cursor.execute(expression, variables)

         # save changes and close connection
        connection.commit()
        connection.close()