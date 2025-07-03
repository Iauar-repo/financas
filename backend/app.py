from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'iauar'

@app.route('/api/login', methods=['POST',])
def login():
    data = request.get_json()

    if not data:
        return {"message": "Dados ausentes"}, 400

    username = data.get('username')
    password = data.get('password')

    #print(f"Usuário: {username}")
    #print(f"Senha: {password}")
    if username == 'admin' and password == '123':
        print('OK')
        return jsonify({"message": "ok"})
    else:
        return jsonify({"message": "fail_pass"}) #or fail_user


if __name__ == '__main__':
    app.run()