import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import bcrypt
from quizoo.db import get_db
from email_validator import validate_email, EmailNotValidError

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        mail = request.form['mail']
        password = request.form['password']
        db = get_db()
        error = None

        # Serverside validation; a bit rudimental - but the main validation should happen on the client side
        error = False

        if not username:
            flash('Username is required.')
            error = True
        
        if not password:
            flash('A password is required.')
            error = True
        elif len(password) > 72: # TODO: Check workaround with sha256 + base64
            flash('Your password is too long.')
            error = True
    
        if not firstname:
            flash('Firstname is required.')
            error = True
        if not mail:
            flash('Mail is required.')
            error = True

        # Validate mail
        try:
            # Validate.
            valid = validate_email(mail)
            # Update with the normalized form.
            mail = valid.email
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            error = str(e)
            flash(error)
            error = True

        if error is False:

            # Check if email already exists
            try:
                cur = g.db.cursor()
                cur.execute("""SELECT mail FROM user WHERE mail=?""", (mail,))
                if cur.fetchone():
                    flash(f'A user with this mail has been registered already!')
                else:
                    cur.execute("""SELECT username FROM user WHERE username=?""", (username))
                    if cur.fetchone():
                        flash(f'Username {username} already exists')
                    else:
                        db.execute(
                            "INSERT INTO user (username, mail, firstname, password) VALUES (?, ?, ?, ?)",
                            (username, mail, firstname, bcrypt.hashpw(password.encode(), bcrypt.gensalt())),
                        )
                        db.commit()
            except db.IntegrityError:
                flash(f"Unknown error. Please contact the website admin!")
        else:
            return redirect(url_for("user.login"))
    return render_template('user/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        if user:
            if bcrypt.checkpw(password.encode(), user['password']):
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('main'))
        
        flash('Username and/or Password are wrong!')

    return render_template('user/login.html')