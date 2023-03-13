import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin



class Job(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "jobs"
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    team_leader_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    team_leader = orm.relationship("User")
    job = sqlalchemy.Column(sqlalchemy.String)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    collaborators = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.String)
    end_date = sqlalchemy.Column(sqlalchemy.String)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)