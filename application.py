import os

from flask import Flask, session, render_template, request, flash 
from flask import redirect, session, abort, url_for,session,logging,request 
from flask_socketio import SocketIO, join_room, emit, disconnect


app = Flask(__name__)
socketio = SocketIO(app)

#Defs to allow session
app.config['SESSION_TYPE']	 = 'filesystem'
app.secret_key 				 = os.urandom(12)

 
i=-1
channel_list = [] 
error = ""


#Base 
@app.route('/')
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

@socketio.on('startup')
def on_startup():
	global i, channel_list

	if i>-1:
		emit('master_channel_list', { "master_channel_list" : channel_list, "items" : i}, broadcast=True)
 
@socketio.on('add channel')
def on_add_channel(channel_name):
	global i, channel_list, error

	error=""
	if channel_name in channel_list:
		error = "Channel already exists!"
		emit('error',{"error_msg" : error}, broadcast=True)
	else:
		i = i+1
		channel_list.append(channel_name)
 		emit('current_channel_list', { "ch_list" : channel_list, "items" : i}, broadcast=True)

@app.route("/join",  methods=["GET", "POST"])
def join_room():
	 
	return render_template("chats.html")


@app.route("/logout",  methods=["GET", "POST"])
def logout():
	session.pop('username', None)
	session['logged_in'] = False
	return redirect(url_for('index'))


if __name__ == '__main__':
    socketio.run(app)
