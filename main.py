from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_ngrok import run_with_ngrok

from forms import RegisterForm, LoginForm, PostForm

from orm.models import User, Post
from orm import db_session

app = Flask('Cool-blogs')
app.config['SECRET_KEY'] = 'TOP_SECRET'
run_with_ngrok(app)

login_manager = LoginManager(app)
login_manager.init_app(app)

db_session.init('db/db.sqlite')


@login_manager.user_loader
def get_user(id):
    session = db_session.create()
    user = session.query(User).get(id)
    session.close()
    return user


@app.route('/', methods=['GET', 'POST'])
def home_page():
    post_form = PostForm()
    session = db_session.create()
    if post_form.validate_on_submit():
        post = Post(content=post_form.content.data, author_id=current_user.id)
        session.add(post)
        session.commit()
    posts = session.query(Post).all()
    response = render_template('home.html', title='Блог', form=post_form, posts=posts)
    session.close()
    return response


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create()
        user = session.query(User).filter(User.login == form.login.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template('login.html',
                                   form=form,
                                   title='Авторизация',
                                   message='Такого пользователя не существует или пароль введен неверно!')
        login_user(user)
        session.close()
    return render_template('login.html', form=form, title='Авторизация')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create()
        user = User(login=form.login.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        session.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/like/<int:id>')
def like_processor(id):
    session = db_session.create()
    post = session.query(Post).get(id)
    post.likes += 1
    session.commit()
    session.close()
    return redirect('/')


# db
if __name__ == '__main__':
    app.run()
