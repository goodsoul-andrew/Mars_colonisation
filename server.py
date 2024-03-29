from flask import Flask, render_template, redirect
from data import db_session
from api import jobs_api
from data.users import User
from data.jobs import Job
from flask_login import LoginManager, login_user
from flask import make_response, jsonify
from forms.user import RegisterForm, LoginForm
from forms.job import AddingForm
from flask_restful import Api
from api.users_resource import UserResource, AllUsersResource
from  api.jobs_resource import JobResource, AllJobsResource

app = Flask(__name__, template_folder="templates")
api = Api(app)
api.add_resource(AllUsersResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(JobResource, '/api/jobs/<int:job_id>')
api.add_resource(AllJobsResource, '/api/jobs')
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).filter()
    return render_template("jobs.html", jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


'''@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = AddingForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        all_jobs = db_sess.query(Job).all()
        last_id = max(u.id for u in all_jobs)
        job = Job(
            id=last_id + 1,
            team_leader_id=form.team_leader_id.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/index')
    return render_template('add_job.html', title='Добавить задание', form=form)'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/database.db")
    app.register_blueprint(jobs_api.blueprint)


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
