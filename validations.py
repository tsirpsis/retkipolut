def check_destination(title, content):
    if not title or len(title) > 50 or not content or len(content) > 2000:
        return False
    return True

def check_registration(username, password):
    if len(username) < 5 or len(username) > 25 or len(password) < 8 or len(password) > 30:
        return False
    return True

def check_classes(entries, all_classes):
    classes = []

    for entry in entries:
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                return None
            if class_value not in all_classes[class_title]:
                return None
            classes.append((class_title, class_value))
    return classes

def check_comment(content):
    if len(content) > 1000 or len(content) < 1:
        return False
    return True

def check_image_type(image_type):
    if image_type not in ["image/jpeg", "image/png"]:
        return False
    return True

def check_image_size(image):
    if len(image) > 500 * 1024:
        return False
    return True
