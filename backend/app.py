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

    if not data:
        return jsonify(status=400, message='Missing data')
    
    username = data.get('username')
    password = data.get('password')

    if username == 'admin' and password == '123':
        session['username'] = username
        return jsonify(message='User Logged in'), 200
    else:
        return jsonify(message='Wrong password'), 401 #or fail_user


@app.route('/api/test')
def test():
    if 'username' in session:
        session['username'] = ''
    
    return jsonify(status='ok', message='User has logged out.')


if __name__ == '__main__':
    app.run()
