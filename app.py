from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app)

messages = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html')

@socketio.on('message')
def handleMessage(msg):
    username = session.get('username')
    message = f"{username}: {msg}"
    messages.append(message)
    send(message, broadcast=True)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
