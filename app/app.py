from flask import Flask, request
import os

app = Flask(__name__)
USERNAME = "admin"
PASSWORD = "password123"  # Hardcoded credentials

@app.route('/')
def home():
    return '''
        <h2>Login</h2>
        <form action="/login" method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit">
        </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    pwd = request.form.get('password')
    if user == USERNAME and pwd == PASSWORD:
        return '''
            <h3>Welcome, admin!</h3>
            <form action="/ping" method="post">
                Host to ping: <input name="host"><br>
                <input type="submit" value="Ping">
            </form>
        '''
    return "Invalid credentials."

@app.route('/ping', methods=['POST'])
def ping():
    host = request.form.get('host')
    result = os.popen(f"ping -c 2 {host}").read()  # Command Injection
    return f"<pre>{result}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Debug mode enabled
