from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User


db_session.global_init("db/database.db")

class AddingForm(FlaskForm):
    db_sess = db_session.create_session()
    all_users = db_sess.query(User).all()
    data = [(u.id, u.name + " " + u.surname) for u in all_users]
    team_leader_id = SelectField("Ответственный", choices=[data])
    job = StringField('Описание', validators=[DataRequired()])
    work_size = IntegerField('Длительность в часах', validators=[DataRequired()])
    collaborators = StringField('Список id участников', validators=[DataRequired()])
    start_date = StringField('Дата начала')
    end_date = StringField('Дата конца')
    is_finished = BooleanField("Завершена", validators=[DataRequired()])