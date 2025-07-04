from flask import Flask, request, session, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)


@app.route('/api/')
def index():
    if 'username' in session:
        user = session['username']
        return jsonify(status='ok', message=f'Logged in as {user}')
    
    return jsonify(status='fail', message='You are not logged in')


@app.post('/api/login')
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if username == 'admin' and password == '123':
<<<<<<< HEAD
        #session['username'] = username
        return jsonify(message='User Logged in'), 200
    else:
        return jsonify(message='Wrong credentials'), 401
=======
        session['username'] = username
        return jsonify(message='User Logged in'), 200
    else:
        return jsonify(message='Wrong password'), 401 #or fail_user
>>>>>>> f078be8f1c60f56a262fa983c6c30a6e2fac0c46


@app.route('/api/ping')
def ping():
    return jsonify(message='Pong!!!'), 200


if __name__ == '__main__':
    app.run()
