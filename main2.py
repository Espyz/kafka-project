from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session, jsonify
from flask_script import Manager, Command, Shell
from forms import ContactForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_folder="static_dir", template_folder="jinja_templates")
app.config['SECRET_KEY'] = '33215033'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://sammy:33215033@localhost:5432/sammy'

manager = Manager(app=app)
db = SQLAlchemy(app)

class Faker(Command):
    def run(self):
        print('Fake data Entered')

manager.add_command("faker", Faker())

@manager.command
def foo():
    print("foo command executed")

def shell_context():
    import os, sys
    return dict(app=app, os=os, sys=sys)

manager.add_command("shell", Shell(make_context=shell_context))

@app.route('/')
def index():
    return render_template('index.html', name='Jerry')

@app.route('/user/<int:user_id>/')
def user_profile(user_id):
    return "Profile page of user #{}".format(user_id)

@app.route('/books/<genre>/')
def books(genre):
    return "All Books in {} category".format(genre)

@app.route('/login/', methods=['post', 'get'])
def login():
    message = ''
    username = None
    password = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    print(request.method)
    if username == 'Espyz' and password == 'Univers':
        
        message = "Correct username and password"
    else:
        message = "Wrong username or password"

    return render_template('login.html', message=message)

@app.route('/contact/', methods=['get', 'post'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        print(name)
        print(Post)
        print(email)
        print(message)

        # здесь логика базы данных
        feedback = Feedback(name=name, email=email, message=message)
        db.session.add(feedback)
        db.session.commit()

        print("\nData received. Now redirecting ...")
        flash("Message Received", "success")
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)

@app.route('/cookie/')
def cookie():
    if not request.cookies.get('foo'):
        res = make_response("Setting a cookie")
        res.set_cookie('foo', 'bar', max_age=60*60*24*365*2)
    else:
        res = make_response("Value of cookie foo is {}".format(request.cookies.get('foo')))
    return res

@app.route('/delete-cookie/')
def delete_cookie():
    res = make_response("Cookie Removed")
    res.set_cookie('foo', 'bar', max_age=0)
    return res

@app.route('/article/', methods=['POST',  'GET'])
def article():
    if request.method == 'POST':
        print(request.form)
        res = make_response("")
        res.set_cookie("font", request.form.get('font'), 60*60*24*15)
        res.headers['location'] = url_for('article')
        return res, 302

    return render_template('article.html',)

@app.route('/front-end-events/')
def front_end_events():
    data = db.session.query(Events).filter(Events.warning == 'Снижение производительности').limit(30)
    # return render_template('front.html', data = data)
    cols = ['id', 'wheel_id', 'warning']
    result = [{col: getattr(d, col) for col in cols} for d in data]
    response = make_response(jsonify(result=result), 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/front-end-idle/')
def front_end_idle_events():
    data = db.session.query(IdleEvents).all()
    cols = ['wheel_id', 'start_downtime', 'end_downtime']
    result = [{col: getattr(d, col) for col in cols} for d in data]
    response = make_response(jsonify(result=result), 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/back/', methods=['post'])
def del_date():
    data = request.get_json()
    print(data)
    wheel_id = data["wheel_id"]
    data = db.session.query(Events).filter(Events.wheel_id == wheel_id).first()
    db.session.delete(data)
    db.session.commit()
    return make_response(jsonify({ "success": True }), 200)

@app.route('/api/test/')
def test():
    d = { "message": "hello" }
    response = make_response(jsonify(d), 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/visits-counter/')
def visits():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
	    session['visits'] = 1
    return "Total visits: {}".format(session.get('visits'))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))

    def __repr__(self):
	    return "<{}:{}>".format(self.id,  self.title[:10])

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer(), primary_key=True, onupdate = True)
    wheel_id = db.Column(db.Integer(), nullable=False)
    time = db.Column(db.Text(), nullable=False)
    warning = db.Column(db.Text(), nullable=True)
    ts = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<{}, {}:{}>'.format(self.id, self.wheel_id, self.warning) 

class IdleEvents(db.Model):
    __tablename__ = 'idle_events'
    id = db.Column(db.Integer(), primary_key=True, onupdate = True)
    part = db.Column(db.Text(), nullable=False)
    wheel_id = db.Column(db.Integer(), nullable=False)
    start_downtime = db.Column(db.Text(), nullable=False)
    end_downtime = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<{}, {}, {}>'.format(self.wheel_id, self.start_downtime, self.end_downtime) 

@app.route('/session/')
def updating_session():
    res = str(session.items())

    cart_item = {'pineapples': '10', 'apples': '20', 'mangoes': '30'}
    if 'cart_item' in session:
	    session['cart_item']['pineapples'] = '100'
	    session.modified = True
    else:
	    session['cart_item'] = cart_item

    return res

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post', backref='category')

    def __repr__(self):
	    return "<{}:{}>".format(id, self.name)

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post', secondary=post_tags, backref='tags')

    def __repr__(self):
	    return "<{}:{}>".format(id, self.name)

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
	    return "<{}:{}>".format(self.id, self.name)

@app.route('/delete-visits/')
def delete_visits():
    session.pop('visits', None)  # удаление данных о посещениях
    return 'Visits deleted'

if __name__ == "__main__":
    manager.run()