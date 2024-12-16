from flask import session, redirect, url_for, abort

def login_required(f):
   
    def pembatas(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login.login'))  # Redirect ke halaman login
        return f(*args, **kwargs)
    pembatas.__name__ = f.__name__
    return pembatas

def role_required(*roles):
    
    def validator(f):
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] not in roles:
                return abort(403)  # Tampilkan halaman Forbidden
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return validator
