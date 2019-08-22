import os

from flask import Flask, session, render_template, request, flash 
from flask import redirect, session, abort, url_for,session,logging,request 
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

#Defs to allow session
app.config['SESSION_TYPE']	= 'filesystem'
app.secret_key 				= os.urandom(12)
app.config["SECRET_KEY"] 	= os.urandom(12)


#Base 
@app.route('/', methods=["GET", "POST"])
def index():
	if session.get('logged_in'):
		return render_template("channels.html")
	else:
		return redirect(url_for('dp_set'))



@app.route("/dp_set", methods=["GET", "POST"]) 
def dp_set():
	if request.method == "POST":
		dp_name = request.form["dp_name"]
 		if dp_name != '':
			session['logged_in'] = True
			session['dp_name']  = dp_name 
			return render_template("channels.html")

	return render_template("dp_set.html")


@app.route("/channels", methods=["GET", "POST"]) 
def channels():
	if request.method == "POST":
		return render_template("channels.html")

	return render_template("dp_set.html")


@app.route("/logout")
def logout():
	session.pop('username', None)
	session['logged_in'] = False
	return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app)
