from exceptions import UserNotFoundError, UserAlreadyExistsError, InvalidUserDataError

class UserDatabase:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, user_data):
        if user_id in self.users:
            raise UserAlreadyExistsError(f"User with ID {user_id} already exists.")
        if not isinstance(user_data, dict):
            raise InvalidUserDataError("User data must be a dictionary.")
        self.users[user_id] = user_data
        print(f"User {user_id} added successfully.")

    def remove_user(self, user_id):
        if user_id not in self.users:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        del self.users[user_id]
        print(f"User {user_id} removed successfully.")

    def update_user(self, user_id, user_data):
        if user_id not in self.users:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        if not isinstance(user_data, dict):
            raise InvalidUserDataError("User data must be a dictionary.")
        self.users[user_id].update(user_data)
        print(f"User {user_id} updated successfully.")

    def get_user(self, user_id):
        if user_id not in self.users:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        return self.users[user_id]

    def get_all_users(self):
        return self.users

def main():
    db = UserDatabase()

    try:
        db.add_user("1", {"name": "John Doe", "email": "john@example.com"})
        db.add_user("1", {"name": "Jane Doe", "email": "jane@example.com"})
    except UserAlreadyExistsError as e:
        print(e)

    try:
        db.remove_user("2")
    except UserNotFoundError as e:
        print(e)

    try:
        db.update_user("1", "invalid data")
    except InvalidUserDataError as e:
        print(e)

    try:
        print(db.get_user("3"))
    except UserNotFoundError as e:
        print(e)

if __name__ == "__main__":
    main()
