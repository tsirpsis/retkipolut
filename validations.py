def check_destination(title, content):
    if not title or len(title) > 50 or len(content) > 1000:
        return False
    return True
