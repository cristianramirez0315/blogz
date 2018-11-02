from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from migrations import User, Blog

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:criscr7madrid@localhost:8889/blogz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B';


# controllers
# home page, all users are displayed here
@app.route('/')
def display_all_users():
    return render_template('users.html', users=User.query.all())



@app.route('/<uid>')
def display_all_blogs(uid):
    user = User.query.filter_by(id=uid).first()
    if user is None:
        flash('User not found', 'danger')
        return redirect('/')
    return render_template('blogs.html', user=user)


# when a user clicks on a blog title, it takes them to the individual blog
@app.route('/<uid>/blog/<id>')
def blog(uid, id):
    user = User.query.filter_by(id=uid).first()
    if user is None:
        flash('User not found', 'danger')
        return redirect('/')

    blog = Blog.query.filter_by(id=id, owner_id=user.id).first()
    if blog is None:
        flash('Blog post not found', 'danger')
        return redirect('/' + uid)
    return render_template('blog.html', blog=blog)


# when a user clicks on add blog, it takes them to the form
@app.route('/newpost', methods=['POST', 'GET'])
def add():
    return render_template('add.html')


# when a user submits the form it goes here, adds to the database, and then redirects to the home page.
@app.route('/save', methods=['POST', 'GET'])
def save():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner_id = session['user_id']

        if not title or not body:
            flash('error message here', 'danger')
            return redirect('/newpost')
        blog = Blog(title, body, owner_id)
        db.session.add(blog)
        db.session.commit()

        return redirect('/' + str(session['user_id']) + '/blog/' + str(blog.id))


@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in', 'success')
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'danger')
            return redirect('/login')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user and password == verify:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registered successfully', 'success')
            return redirect('/')
        elif len(username) < 3 or len(password) < 3 or len(verify) < 3:
            flash("No fields can be less than 3 characters", 'danger')
        elif existing_user:
            flash("Username already exists", 'danger')
        elif password != verify:
            flash("Passwords don't match", 'danger')

    return render_template('register.html')


@app.route('/logout')
def logout():
    del session['username']
    del session['user_id']
    return redirect('/')


if __name__ == '__main__':
    app.run()
