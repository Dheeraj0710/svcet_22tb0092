from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server'
db = SQLAlchemy(app)

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    votes = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    polls = Poll.query.all()
    return render_template('index.html', polls=polls)

@app.route('/poll/<int:poll_id>', methods=['GET', 'POST'])
def poll(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    choices = Choice.query.filter_by(poll_id=poll.id).all()
    if request.method == 'POST':
        choice_id = request.form.get('choice')
        choice = Choice.query.get(choice_id)
        if choice:
            choice.votes += 1
            db.session.commit()
        return redirect(url_for('results', poll_id=poll.id))
    return render_template('poll.html', poll=poll, choices=choices)

@app.route('/results/<int:poll_id>')
def results(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    choices = Choice.query.filter_by(poll_id=poll.id).all()
    return render_template('results.html', poll=poll, choices=choices)

if __name__ == '__main__':
    app.run(debug=True)
