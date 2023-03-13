from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.users import User
from flask import jsonify
from werkzeug.security import generate_password_hash


user_parser = reqparse.RequestParser()
# user_parser.add_argument('id', required=True, type=int)
user_parser.add_argument('name', required=True, type=str)
user_parser.add_argument('surname', required=False, type=str)
user_parser.add_argument('age', required=False, type=int)
user_parser.add_argument('position', required=False, type=str)
user_parser.add_argument('speciality', required=True, type=str)
user_parser.add_argument('address', required=False, type=str)
user_parser.add_argument('email', required=True, type=str)
user_parser.add_argument('password', required=True, type=str)
user_parser.add_argument('about', required=False, type=str)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=("id", "surname", "name", "age", "position", "speciality", "address", "email", "about", "hashed_password"))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=("id", "surname", "name", "age", "position", "speciality", "address", "email", "about", "hashed_password"))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class AllUsersResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {
                "users":
                    [user.to_dict(
                    only=("id", "surname", "name", "age", "position", "speciality", "address", "email", "about", "hashed_password"))
                    for user in users]
            })

    def post(self):
        args = user_parser.parse_args()
        db_sess = db_session.create_session()
        all_users = db_sess.query(User).all()
        last_id = max(u.id for u in all_users)
        # print(last_id)
        user = User(
            id=last_id + 1,
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            about=args['about'],
            hashed_password=generate_password_hash(args['password']),
        )
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})