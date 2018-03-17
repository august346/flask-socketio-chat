from flask import Flask, render_template, session, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.debug = True
socketio = SocketIO(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def json(self):
        return 'username'


def get_user(name, pswd):
    return User.query.filter_by(username=name, password=pswd).first()




@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form['username']
    # pswd = request.form['password']
    # session['user'] = get_user(name, pswd).json()
    session['user'] = name
    print(session['user'])
    return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user')
    return redirect(url_for('index'))


if __name__ == '__main__':
    socketio.run(app)
