from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.jobs import Job
from flask import jsonify


job_parser = reqparse.RequestParser()
# user_parser.add_argument('id', required=True, type=int)
job_parser.add_argument('team_leader_id', required=True, type=int)
job_parser.add_argument('job', required=True, type=str)
job_parser.add_argument('work_size', required=False, type=int)
job_parser.add_argument('collaborators', required=True, type=str)
job_parser.add_argument('start_date', required=False, type=str)
job_parser.add_argument('end_date', required=False, type=str)
job_parser.add_argument('is_finished', required=False, type=bool)


def abort_if_user_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Job).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobResource(Resource):
    def get(self, job_id):
        abort_if_user_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Job).get(job_id)
        return jsonify({'job': job.to_dict(
            only=("id", "team_leader_id", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished"))})

    def delete(self, job_id):
        abort_if_user_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Job).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class AllJobsResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Job).all()
        return jsonify(
            {
                "jobs":
                    [job.to_dict(
                    only=("id", "team_leader_id", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished"))
                    for job in jobs]
            })

    def post(self):
        args = job_parser.parse_args()
        db_sess = db_session.create_session()
        all_jobs = db_sess.query(Job).all()
        last_id = max(u.id for u in all_jobs)
        # print(last_id)
        job = Job(
            id=last_id + 1,
            team_leader_id=args["team_leader_id"],
            job=args["job"],
            work_size=args["work_size"],
            collaborators=args["collaborators"],
            start_date=args["start_date"],
            end_date=args["end_date"],
            is_finished=args["is_finished"]
        )
        db_sess.add(job)
        db_sess.commit()
        return jsonify({'success': 'OK'})