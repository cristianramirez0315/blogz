from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:criscr7madrid@localhost:8889/build-a-blog'
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

# home page, all the blogs are displayed here
@app.route('/')
def display_all_blogs():
    blogs = Blog.query.all()
    return render_template('blogs.html', blogs=blogs)

# when a user clicks on a blog title, it takes them to the individual blog
@app.route('/blog/<id>')
def blog(id):
    blog = Blog.query.filter_by(id=id).first()
    return render_template('blog.html', blog=blog)

# when a user clicks on add blog, it takes them to the form
@app.route('/newpost', methods=['POST','GET'])
def add():
    return render_template('add.html')

# when a user submits the form it goes here, adds to the database, and then redirects to the home page.
@app.route('/save', methods=['POST','GET'])
def save():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title or not body:
            return render_template('add.html', error='All fields must be filled')
        blog = Blog(title, body)
        db.session.add(blog)
        db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()

