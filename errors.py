from flask import abort

def forbidden():
    abort(403)

def not_found():
    abort(404)
