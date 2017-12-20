from flask import Flask, request, render_template
import json
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
db = SQLAlchemy(app)

# Connect to db
POSTGRES = {
	'user': 'postgres',
	'pw': 'password',
	'db': 'UserDB',
	'host': 'localhost',
	'port': '5432',
}

class Usersimilarity(db.Model):
	'''
		Database model for UserSimilarity object
	'''
	user_handle = db.Column(db.Integer, primary_key=True)
	similarity_score = db.Column(db.String(255))
	similar_user = db.Column(db.String(255))
	def __init__(self, user_handle, similarity_score):
		'''
			Initialize user handle, similarity score, similar users
		'''
		self.user_handle = user_handle
		self.similarity_score = similarity_score
		self.similar_user = similar_user

	def __repr__(self):
		return '<User %r>' % self.user_handle;



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


@app.route('/')
def index():
	'''
		Define default route
	'''
	return render_template('search.html')

@app.route('/search_user', methods=['POST'])
def get_similarity_score():
	'''
		Make a call to UserSimilarity table and fetch values
	'''
	user_handle = request.form['userhandle']
	user = Usersimilarity.query.filter_by(user_handle=int(user_handle))
	return render_template('search.html', userList=user)

if __name__ == '__main__':
	app.debug = True
	app.run()