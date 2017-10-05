from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:catfish@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "catfish"

db = SQLAlchemy(app)

# database model classes to create tables from
class Blog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50))
	body = db.Column(db.String(255))
	
	def __init__(self, title, body):
		self.title = title
		self.body = body
		
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
		
		return redirect("/blog")
	
	return render_template("newpost.html")
		
if __name__ == "__main__":
	app.run()
