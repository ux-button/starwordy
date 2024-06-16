import random
from sqlreader import SQLreader

db = SQLreader('starword.db')

class Group:
    def __init__(self, id, name):
        self.id = id
        self.name = name


    @classmethod
    def new(cls, name, user):
        name = name.strip().lower().capitalize()
        db.set('INSERT INTO groups (user_id, group_name) VALUES (?, ?)', (user, name,))
        rows = db.get('SELECT id FROM groups WHERE user_id = ?', (user,))
        return cls(rows[0], name)


    @classmethod
    def load(cls, user_id):
        rows = db.getall('SELECT id, group_name FROM groups WHERE user_id = ?', (user_id,))
        groups = list()
        for row in rows:
            group = cls(row[0], row[1])
            groups.append(group)
        return groups


    @classmethod
    def load_group(cls, name, user):
        rows = db.get('SELECT id FROM groups WHERE user_id = ? AND group_name = ?', (user, name,))
        if len(rows) == 0:
            return None
        return cls(rows[0], name)


    @classmethod
    def delete(cls, group_id):
        # Delete all words related to group
        db.set('DELETE FROM words WHERE group_id = ?', (group_id,))

        # Delete group
        db.set('DELETE FROM groups WHERE id = ?', (group_id,))


class Flipcard:
    def __init__(self, word_id, group_id, word, definition, curve):
        self.word_id = word_id
        self.group_id = group_id
        self.word = word
        self.definition = definition
        self.curve = curve


    @classmethod
    def new(cls, group_id, word, definition):
        db.set('INSERT INTO words (group_id, word, definition, curve) VALUES (?, ?, ?, 0)',
                   (group_id, word, definition,))
        rows = db.get('SELECT * FROM words WHERE group_id = ? AND word = ? AND definition = ?',
                          (group_id, word, definition,))
        return cls(rows[0], rows[1], rows[2], rows[3], rows[4])


    # Load all flipcard of the group
    @classmethod
    def load(cls, group_id):
        rows = db.getall('SELECT * FROM words WHERE group_id = ?', (group_id,))
        flipcards = list()
        for row in rows:
            flipcard = cls(row[0], group_id, row[2], row[3], row[4])
            flipcards.append(flipcard)
        return flipcards


    # Load n random cards from group
    @classmethod
    def load_random(cls, group_id, quantity):
        rows = db.getall('SELECT * FROM words WHERE group_id = ?', (group_id,))
        flipcards = list()
        for row in rows:
            flipcard = cls(row[0], group_id, row[2], row[3], row[4])
            flipcards.append(flipcard)
        random.shuffle(flipcards)
        return flipcards[:quantity]


    @classmethod
    def delete(cls, id):
        db.set('DELETE FROM words WHERE id = ?', (id,))


    def increase(self):
        self.curve += 1


    def decrease(self):
        if self.curve != 0:
            self.curve -= 1


class User:
    def __init__(self, id, username, groups, flipcards):
        self.id = id
        self.username = username
        self.groups = groups
        self.flipcards = flipcards

    @classmethod
    def get(cls, id):
        # Load all users groups
        all_groups = Group.load(id)

        # Load all users flipcards
        all_flipcards = []
        for group in all_groups:
            flipcards = Flipcard.load(group.id)
            for flipcard in flipcards:
                all_flipcards.append(flipcard)

        # Load username
        username = db.get('SELECT user_id FROM users WHERE id = ?', (id,))
        username = str(username[0]).capitalize()

        # Return user object
        return cls(id, username, all_groups, all_flipcards)

