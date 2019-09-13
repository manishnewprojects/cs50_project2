import os

from flask import Flask, session, render_template, request, flash 
from flask import redirect, session, abort, url_for,session,logging,request 
from flask_socketio import SocketIO, join_room, leave_room, emit, disconnect

import logging, time



app = Flask(__name__)
socketio = SocketIO(app)

log = logging.getLogger('werkzeug')
log.disabled = True

#Defs to allow session
app.config['SESSION_TYPE']	 = 'filesystem'
app.secret_key 				 = os.urandom(12)

 
channel_id=-1
channel_list = {}
channel_message_history = [[[]]]
channel_messages = []
message_store=""
 
#Base 
@app.route('/')
def index():
	global channel_id
 	if session.get('logged_in'):
 	 	return render_template("chats.html", channel=session['channel'])
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
	#if request.method == "POST":
	return render_template("channels.html")
	#return render_template("dp_set.html")

@socketio.on('startup')
def on_startup():
	global channel_id, channel_list
	ch_list=""

	if (channel_id == -1):
		session['channel'] =""

	if channel_id > -1:
		for key in channel_list.keys():
			ch_list+="<li> <a href=\"chats/"+key+"\">"+key+"</a></li>"

 		emit('master_channel_list', { "ch_list" : ch_list}, broadcast=True)


@socketio.on('add channel')
def on_add_channel(channel_name):
	global channel_id, channel_list, error 
	ch_list=""
 	error=""

	if channel_name in channel_list.keys():
		error = "Channel already exists!"
		emit('error',{"error_msg" : error, "channel": channel_name})
	else:
		channel_id+=1
		session['channel_id']=channel_id
		channel_messages.append(channel_id)
		channel_messages[channel_id] = ""

		channel_message_history.append(channel_id)
		#channel_message_history[channel_id][0]=""

		channel_list.update({channel_name:channel_id})
		for key in channel_list.keys():
			ch_list+="<li> <a href=\"chats/"+key+"\">"+key+"</a></li>"

 		emit('current_channel_list', { "ch_list" :  ch_list }, broadcast=True)


@app.route("/chats/<channel>",  methods=["GET", "POST"])
def chats(channel):
	global channel_id

	session['channel'] = channel
	session['channel_id'] = channel_list.get(channel)
	channel_id = session['channel_id']

 	return render_template("chats.html", channel=channel)

@socketio.on('join_now')
def joining():
	global channel_id, channel_messages

	join_room(channel_id)
	emit('message_history',{"chat_so_far" : channel_messages[session['channel_id']]}, room=channel_id)

@socketio.on('leave_now')
def joining():
	global channel_id
	
	leave_room(channel_id)

@socketio.on('message posted')
def message_posted(message):
	global channel_id, channel_list, message_store, channel_messages

    
	#channel_message_history[session['channel_id']] += 1
	#channel_message_history[session['channel_id']][0] = message

	ts = time.gmtime()

	channel_messages[session['channel_id']] += ((time.strftime("%x %X", ts)+":"+session['dp_name']+":"+message+"<br>"))

	#message_store+=session['dp_name']+":"+message+"<br>"

 	emit('message_buffer',{"chat_history" : channel_messages[session['channel_id']]}, room=channel_id)
	

@app.route("/logout",  methods=["GET", "POST"])
def logout():
	session.pop('username', None)
	session['logged_in'] = False
	return redirect(url_for('index'))


if __name__ == '__main__':
    socketio.run(app)
