from flask import Flask, render_template, redirect, request, make_response, session, jsonify, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_login import login_required, logout_user, current_user, LoginManager, login_user
from flask_mail import Mail, Message
import json

from data import db_session
from data.models import User, Detection

from random import choice
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 100
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=10)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'virus.self.isolation@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'virus.self.isolation@gmail.com'
app.config['MAIL_PASSWORD'] = 'V!13wirM_TR'

mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    mail = StringField('Почта',
                       validators=[InputRequired("Необходимо ввести email")])
    name = StringField('Имя',
                           validators=[InputRequired("Необходимо ввести имя")])
    surname = StringField('Фамилия',
                           validators=[InputRequired("Необходимо ввести фамилию")])
    password = PasswordField('Пароль',
                             validators=[InputRequired("Необходимо ввести пароль"),
                                         Length(min=9, message='Пароль должен содержать больше 8 символов')])
    remember_me = BooleanField('Запомнить меня')
    submit_res = SubmitField('Зарегистрироваться')
    submit_sign = SubmitField('Войдите')


class CheckEmailForm(FlaskForm):
    code = StringField('Код подтверждения',
                             validators=[Length(min=6, max=6, message='код состоит из 6 символов')])
    submit_code = SubmitField('Подтвердить')


class SignIn(FlaskForm):
    mail = StringField('Почта',
                       validators=[InputRequired("Необходимо ввести email")])
    password = PasswordField('Пароль',
                             validators=[InputRequired("Необходимо ввести пароль"),
                                         Length(min=9, message='Пароль должен содержать больше 8 символов')])
    submit_sign = SubmitField('Вход')


users_codes = {}


def send_code(user):
    code = get_code()
    users_codes[user.id] = code

    msg = Message("Подтверждение почты", recipients=[user.email])
    msg.body = f"Ваш код подтверждения: {code}"
    mail.send(msg)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.submit_res.data:
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.mail.data).first():
                return render_template("login.html", form=form,
                                       message="Пользователь с такой почтой уже есть")
            user = User()
            user.name = form.name.data
            user.surname = form.surname.data
            user.email = form.mail.data
            user.set_password(form.password.data)

            session.add(user)
            session.commit()

            try:
                send_code(user=user)
            except:
                session.delete(user)
                session.commit()
                return render_template("login.html", form=form,
                                       message="Почта введена некорректно")

            #login_user(user)

            return redirect(url_for('.check', user=user.id))

    if form.submit_sign.data:
        return redirect('/signin')
    return render_template('login.html', form=form)


@app.route('/check', methods=['GET', 'POST'])
def check():
    user_id = request.args['user']
    print(user_id)
    user = load_user(user_id)

    form = CheckEmailForm()
    print(user.name)
    if form.submit_code.data:
        print(users_codes[user.id])
        if form.code.data != users_codes[user.id]:
            return render_template('/check.html', form=form, message='Неверный код')
        login_user(user, remember=True)
        return redirect('/index')
    print(user.id)
    return render_template('/check.html', form=form)
        # print(current_user.get_id())
    #return render_template('/login')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignIn()
    if form.submit_sign.data:
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.mail.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect('/')
        return render_template('sign_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('sign_in.html', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return str(current_user.get_id())


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    pass

def get_code():
    nums = [str(n) for n in range(10)]
    return ''.join([choice(nums) for _ in range(6)])


def main():
    db_session.global_init("test.sqlite")
    app.run(host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
