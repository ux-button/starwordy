from sqlreader import SQLreader

db = SQLreader('./starword.db')
user = 'alex'

users = db.get('SELECT * FROM words')
print(users[0], users[1], users[2], users[3], users[4])