import os, genny, datetime
from flask import render_template, send_from_directory, g, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from flask_classful import FlaskView, route

from random import choice
from __init__ import app, csrf, login_manager

from models import db, User
from forms import LoginForm, RegistrationForm


class AuthView(FlaskView):
    
    def index(self):
        if g.user.is_authenticated:
            return redirect(request.args.get("next") or url_for("home"))
        else:
            return render_template('auth/index.html', zen=choice(quotes))

    def signup(self):
        return render_template('auth/register.html')


    """
    def register(self, methods=['GET', 'POST']):
        # Check if user is logged in
        if current_user.is_authenticated:
           flash('You are already logged in!', 'info')

           return redirect(url_for('login'))
        # Request a registration form from the server
        form = RegistrationForm(request.form)
        # Get The user's input
        if request.method == 'POST' and form.validate_on_submit():
            '''username = request.form.get('username')
            password = request.form.get('password')
            firstname = request.form.get('firstname').capitalize()
            lastname = request.form.get('lastname').capitalize()
            email = request.form.get('email')
            '''

            # Check for existing usernames
            is_existing = User.query.filter_by(
                username=request.form.get('username')).first()
            if is_existing:
                flash('That username has already been taken. Please Try another', 'warning')
                return render_template('register.html', form=form)
            # Create the user
            user = form.save_user(User())
            user.password_hash = user.make_password(request.form.get('password'))

            # Save the user
            db.session.add(user)
            db.session.commit()

            token = user.generate_confirmation_token()
            #tasks.send_email(user.email, 'Confirm Your Account',
            #                '/auth/email/confirm', user=user, token=token)
            flash('A confirmation email has been sent to you by email.')
            return redirect(url_for('login'))

        if form.errors:
            flash(form.errors, 'danger')
        return render_template('auth/register.html', form=form) """
    


    #@route("/login/", methods=["GET", "POST"])
    def login(self, methods=['GET', 'POST']):
    
        if request.method == "POST":
            #online_user = OnlineUser()
            form = LoginForm(request.form)
            if form.validate():
                login_user(form.user, remember=form.remember_me.data)

                '''existing_ = Online.query.filter_by(username=g.user.username).first()
                if existing_:
                    existing_.status_online()
                    existing_.login_timestamp = datetime.datetime.now()
                    db.session.commit()
                else:
                    online_user = Online(userid=g.user.id)
                    online_user.status_online()
                    online_user.login_timestamp = datetime.datetime.now()
                    online_user.save()'''

                print('{u} just logged in'.format(u=g.user.id))
                flash("Successfully logged in as %s." %
                    form.user.username, "success")
                return redirect(request.args.get("next"))# or url_for("/rate"))
        else:
            form = LoginForm()
        return render_template("auth/login.html", form=form)

