from flask import Flask, render_template, redirect, flash, session
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, IntegerField
from wtforms.validators import DataRequired
from . import crypto, config
import os
import base64

app = Flask(__name__)
app.config.from_object(config)


class RegisterForm(FlaskForm):
    login = TextField('login', validators=[DataRequired()])


class LoginForm(FlaskForm):
    login = TextField('login', validators=[DataRequired()])
    otp = IntegerField('otp', validators=[DataRequired()])


# users = {}
# users["admin"] = crypto.User(username="admin")
contexts = {}


def uid_mgr():
    global contexts
    if 'uid' in session:
        uid = session["uid"]
    else:
        uid = base64.b64encode(os.urandom(16)).decode()
        session["uid"] = uid
    if uid not in contexts:
        contexts[uid] = crypto.context()
    return uid, contexts[uid]


@app.route('/')
@app.route('/index')
def index():
    uid_mgr()
    return render_template('base.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    uid, context = uid_mgr()
    form = RegisterForm()
    if form.validate_on_submit():
        login = form.login.data
        if login in context.users:  # !!
            flash("Your login exists")
            return redirect("/register")
        context.users[login] = crypto.User(username=login, context=context)  # !!
        flash(f"Good, your seed {context.users[login].get_seed()} and first password {context.users[login].gen_pass()}")  # !!
    return render_template('reg.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    uid, context = uid_mgr()
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        otp = form.otp.data
        if login not in context.users:  # !!
            flash("Your login not exists")
            return redirect("/register")
        if otp == context.users[login].gen_pass():  # !!
            if login == "admin":
                flash("kks{s33ms_l1k3_y0u_s0_5ucc3ssful_1n_r4nd0m_pr3d1ct10n}")
            else:
                flash("Login successful!!")
        else:
            flash(f"go away")
    return render_template('login.html', form=form)


@app.route('/regen', methods=["GET", "POST"])
def regen():
    uid, context = uid_mgr()
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        otp = form.otp.data
        if login not in context.users:  # !!
            flash("Your login not exists")
            return redirect("/register")
        if otp == context.users[login].gen_pass():  # !!
            flash("go away stranger")
            return redirect("/regen")
        context.users[login].regen_seed()  # !!
        flash(f"Okay, here your new seed {context.users[login].get_seed()} and first password {context.users[login].gen_pass()}")  # !!
    return render_template('regen.html', form=form)


if __name__ == "__main__":
    app.run()
