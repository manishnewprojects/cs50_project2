import os

from flask import Flask, session, render_template, request, flash 
from flask import redirect, session, abort, url_for,session,logging,request 
from flask_socketio import SocketIO, join_room, emit, disconnect


app = Flask(__name__)
socketio = SocketIO(app)

#Defs to allow session
app.config['SESSION_TYPE']	 = 'filesystem'
app.secret_key 				 = os.urandom(12)

 
channel_count=-1
channel_list = {}
channel_data = [[[]]]
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
	global channel_count, channel_list
	ch_list=""

	if channel_count > -1:
		for value in channel_list.values():
			ch_list+="<li> <a href=\"chats/"+value+"\">"+value+"</a></li>"

 		emit('master_channel_list', { "ch_list" : ch_list}, broadcast=True)


@socketio.on('add channel')
def on_add_channel(channel_name):
	global channel_count, channel_list, error 
	ch_list=""
 	error=""
 	
	if channel_name in channel_list.values():
		error = "Channel already exists!"
		emit('error',{"error_msg" : error}, broadcast=True)
	else:
		channel_count+=1
		channel_list.update({channel_count:channel_name})
		for value in channel_list.values():
			ch_list+="<li> <a href=\"chats/"+value+"\">"+value+"</a></li>"

 		emit('current_channel_list', { "ch_list" :  ch_list }, broadcast=True)


@app.route("/chats/<channel>",  methods=["GET", "POST"])
def chats(channel):
	session['channel'] = channel
 	return render_template("chats.html", channel=channel)


@socketio.on('message posted')
def message_posted(message):
	global chat_history, channel_list, channel_map, channel_count

 	print("dict", channel_list, "session", session['channel'])
	 
	emit('message_buffer',{"chat_history" : message}, broadcast=True)
	

@app.route("/logout",  methods=["GET", "POST"])
def logout():
	session.pop('username', None)
	session['logged_in'] = False
	return redirect(url_for('index'))


if __name__ == '__main__':
    socketio.run(app)
