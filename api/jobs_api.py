import json

import flask
from data import db_session
from data.jobs import Job
from flask import jsonify, request

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()
    return jsonify(
        {
            'jobs':
                [job.to_dict(only=('job', 'team_leader_id', 'collaborators')) for job in jobs]
        }
    )

@blueprint.route("/api/jobs/<int:job_id>")
def get_job(job_id: int):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': jobs.to_dict(only=('job', 'team_leader_id', 'collaborators'))
        }
    )


@blueprint.route("/api/jobs", methods=["POST"])
def add_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["id", "team_leader_id", "job", "work_size", "collaborators", "start_date"]):
        return jsonify({'error': 'Bad request'})
    with open("save.json", "w") as save:
        json.dump(request.json, save)
    db_sess = db_session.create_session()
    '''all_jobs = db_sess.query(Job).all()
    last_id = max(job.id for job in all_jobs)
    print(last_id)'''
    job = Job(
        id=request.json["id"],
        team_leader_id=request.json["team_leader_id"],
        job=request.json["job"],
        work_size=request.json["work_size"],
        collaborators=request.json["collaborators"],
        start_date=request.json["start_date"]
    )
    db_sess.add(job)
    db_sess.commit()

    return jsonify({'success': 'OK'})