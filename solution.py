from flask import render_template, Flask

from data.db_session import global_init, create_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def table():
    global_init('db/mars_explorer.sqlite')
    db_sess = create_session()
    jobs = db_sess.query(Jobs).all()
    spis = []
    for job in jobs:
        title = job.job
        user = db_sess.query(User).filter(User.id == job.team_leader).first()
        team_lead = f'{user.surname} {user.name}'
        duration = f'{job.work_size} hours'
        col = job.collaborators
        if job.is_finished:
            is_finished = 'Is finished'
        else:
            is_finished = 'Is not finished'
        elements = [title, team_lead, duration, col, is_finished]
        spis.append(elements)
    return render_template('table.html', jobs=spis)


if __name__ == '__main__':
    app.run(port=500, host='127.0.0.1')
