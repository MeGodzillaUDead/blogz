from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from sort import reverse_bubble_sort

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:catfish@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "catfish"

db = SQLAlchemy(app)

# database model classes to create tables from
class Blog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50))
	body = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __init__(self, title, body, user):
		self.title = title
		self.body = body
		self.user = user
		
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(24), unique=True)
	password = db.Column(db.String(24))
	blogs = db.relationship('Blog', backref='user')
	
	def __init__(self,username,password):
		self.username = username
		self.password = password

# Flask handler routes
@app.route("/blog")
def blog():
	# if there is an id argument render just that blog
	if request.args.get('id'):
		blog_id = request.args.get('id')
		blog = Blog.query.filter_by(id=blog_id).first()
		
		return render_template("one-blog.html", blog = blog)
	
	else:
		# for get requests without args render the landing page
		entries = Blog.query.all()
		# need to reverse sort
		reverse_bubble_sort(entries)
		
		return render_template("blog.html", entries=entries)
	
@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
	if request.method == 'POST':
		if not request.form['title'] or not request.form['body']:
			if not request.form['title']:
				flash("Title cannot be blank.")
			if not request.form['body']:
				flash("Body cannot be empty.")
			return render_template("newpost.html")
		
		blog_title = request.form['title']
		blog_body = request.form['body']
		post = Blog(blog_title, blog_body)
		db.session.add(post)
		db.session.commit()
		
		flash("New post created.")
		
		id = str(post.id)
		
		return redirect("/blog?id=" + id)
	
	return render_template("newpost.html")
	
## signup GET and POST routes
@app.route("/signup", methods=['GET', 'POST'])
def signup():
	return render_template("signup.html")
		
## login GET and POST routes


if __name__ == "__main__":
	app.run()
