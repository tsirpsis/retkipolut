def check_destination(title, content):
    if not title or len(title) > 50 or len(content) > 1000:
        return False
    return True

def check_registration(username, password):
    if len(username) < 5 or len(password) < 8:
        return False
    return True
