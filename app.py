from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from forms import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "HAHAHAH"

db = SQLAlchemy(app)
csrf = CSRFProtect()
csrf.init_app(app)


class Tasks(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.String, nullable=False)


@app.route('/')
def index():
	tasks = Tasks().query.all()
	submit = submitIt()
	return render_template('index.html', tasks=tasks, submit=submit)

@app.post('/')
def index_post():
	task = request.form['todo']
	new_task = Tasks(task=task)
	if len(task) < 60:
		db.session.add(new_task)
		db.session.commit()
		flash("Edited Message Successfully!", "success")
	else:
		flash("The Length of the task should be less than 60!", "warning")
	return redirect('/')

@app.route('/edit/<id>')
def edit(id):
	try:
		task = Tasks().query.filter_by(id=id).one()
		submit = submitIt()
		return render_template('edit.html',task=task,submit=submit)
	except:
		flash("The task doesn't exist!", "danger")
		return redirect('/')

@app.post('/edit/<id>')
def edit_post(id):
	try:
		task = Tasks().query.filter_by(id=id).one()
		new_task = request.form['todo']
		if len(new_task) < 60:
			task.task = new_task
			db.session.commit()
			flash("Edited Message Successfully!", "success")
		else:
			flash("The Length of the task should be less than 60!", "warning")
	except:
		flash("The task doesn't exist!", "danger")
	return redirect('/')


@app.route('/del/<id>')
def delete(id):
	Tasks().query.filter_by(id=id).delete()
	db.session.commit()
	return redirect('/')

if __name__ == '__main__':
	app.run(debug=True)