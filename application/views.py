
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, session
from flask_login import login_user, login_required, logout_user, UserMixin
from application import db
from application.models import User, Kanban
from application.forms import RegistrationForm, LoginForm


views_blueprint = Blueprint('views_blueprint', __name__)


# -- routes to home | blog | register | login | logout | user -- #
@views_blueprint.route('/about')
def about():

    return render_template('about.html')


@views_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)

        db.session.add(user)
        db.session.commit()
        #flash('Thanks for registration!')
        return redirect(url_for('views_blueprint.login'))

    return render_template('register.html', form=form)


#as we have forms in this page, we'll need methods 'GET' and 'POST'
@views_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        #grab user from our User models table
        user = User.query.filter_by(username=form.username.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            #flash('You are logged in')

            #if a user was trying to visit a page that requires a login flask saves that URL as 'next'
            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('views_blueprint.user')

            return redirect(next)

    return render_template('login.html', form=form)


@views_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    #flash("Logged out")
    return redirect(url_for('home'))


@views_blueprint.route('/user')
@login_required #with this decorator, if you try to visit the page 'user', you'll be redirect to login page
def user():

    todos = Kanban.query.filter_by(status=0)
    doing = Kanban.query.filter_by(status=1)
    done = Kanban.query.filter_by(status=2)

    return render_template("user.html", todos=todos, doing=doing, done=done)


@views_blueprint.route("/")
def home():

    return render_template("home.html")

@views_blueprint.route("/add", methods = ["POST"])
def add():
    todo = Kanban(text=request.form['todoitem'], status=0)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for("views_blueprint.user"))

@views_blueprint.route("/todo/<id>")
def todo(id):
    todo = Kanban.query.filter_by(id=int(id)).first()
    todo.status = 0
    db.session.commit()
    return redirect(url_for("views_blueprint.user"))

@views_blueprint.route("/doing/<id>")
def doing(id):
    doing = Kanban.query.filter_by(id=int(id)).first()
    doing.status = 1
    db.session.commit()
    return redirect(url_for("views_blueprint.user"))

@views_blueprint.route("/done/<id>")
def done(id):
    done = Kanban.query.filter_by(id=int(id)).first()
    done.status = 2
    db.session.commit()
    return redirect(url_for("views_blueprint.user"))

@views_blueprint.route("/remove/<id>")
def remove(id):
    remove = Kanban.query.filter_by(id=int(id)).first()
    db.session.delete(remove)
    db.session.commit()
    return redirect(url_for("views_blueprint.user"))
