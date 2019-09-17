import os

from flask import Flask, session, render_template, request, flash 
from flask import redirect, session, abort, url_for,session,logging,request 
from flask_socketio import SocketIO, join_room, leave_room, emit, disconnect

import logging, datetime, collections, random, requests

from collections import deque
 


app = Flask(__name__)
socketio = SocketIO(app)

log = logging.getLogger('werkzeug')
log.disabled = True

#Defs to allow session
app.config['SESSION_TYPE']	 = 'filesystem'
app.secret_key 				 = os.urandom(12)

 
channel_id				= -1
channel_message 		= []
channel_list 			= {}
channel_message_history = []
joke 					= []
dp_names 				= []
 
 
@app.route('/')
def user_login():
 	if (session.get('channel')!=None and session.get('dp_name')!=""):
 	 	return render_template("chats.html", channel=session['channel'])
 	elif session.get('dp_name'):
 		return render_template("channels.html")
 	else:
		return redirect(url_for('index'))


@app.route("/index", methods=["GET", "POST"]) 
def index():
	if request.method == "POST":
		dp_name = request.form["dp_name"]

		if dp_name in dp_names:
			error = 'Display name already taken. Please try again!'
			return render_template("index.html", error=error)
		elif dp_name != '':
			session['logged_in'] = True
			session['dp_name']  = dp_name 
			dp_names.append(dp_name)
			return render_template("channels.html", dp_name=dp_name)
		return render_template("index.html")

	return render_template("index.html")


@app.route("/channels", methods=["GET", "POST"]) 
def channels():
	global channel_id
	
	session['channel'] =""
 	return render_template("channels.html")
 
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
	global channel_id, channel_list, error , channel_messages 

	channel_message_deck = deque(maxlen=100)
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
		channel_message_history[channel_id] = channel_message_deck

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
	global channel_id, channel_messages, channel_message_history
	composed_message=""

	join_room(channel_id)

	if channel_message_history[session['channel_id']]:
		current_channel_length = len(channel_message_history[session['channel_id']])

		i=0
		while i < current_channel_length:
			composed_message+=channel_message_history[session['channel_id']][i]
			i+=1
		emit('message_history',{"chat_so_far" : composed_message}, room=channel_id)

	else:
		emit('message_history',{"chat_so_far" : ""}, room=channel_id)
 
@socketio.on('leave_now')
def leaving():
	global channel_id
	
	leave_room(channel_id)

@socketio.on('message posted')
def message_posted(message):
	global channel_id, channel_list, channel_messages, channel_message_history
	formatted_message = ""
	composed_message=""
	current_time = datetime.datetime.now()

	setup_jokes()
	if (message=="/joke"):
		message = joke[random.randint(0,6)]
	elif (message == "/fact"):
		request = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
		r_json = request.json()
		message = r_json['text']

	current_channel_length = len(channel_message_history[session['channel_id']])

	if current_channel_length == 100:
		channel_message_history[session['channel_id']].popleft()
		current_channel_length-=1

	formatted_message = session['dp_name']+"["+current_time.strftime("%I:%M")+"]"+"::"+message+"<br>"

	channel_message_history[session['channel_id']].append(formatted_message)

	i=0
	while i <= current_channel_length:
		composed_message+=channel_message_history[session['channel_id']][i]
		i+=1

	channel_messages[session['channel_id']] += formatted_message

	emit('message_buffer',{"chat_history" : composed_message}, room=channel_id)
 
 	
@app.route("/logout",  methods=["GET", "POST"])
def logout():

	session['logged_in'] = False
	session['dp_name'] = ""

	session.pop('username', None)
	session.pop('channel', None)
	return redirect(url_for('index'))

def setup_jokes():
	joke.append("Did you hear about the crook who stole a calendar? He got twelve months.")
	joke.append("The worst time to have a heart attack is during a game of charades")
	joke.append("Why are eggs not very much into jokes? Because they could crack up.")
	joke.append("Does your horse smoke? \"No\". Well, then I think your stable is burning.")
	joke.append("I ran into my ex in town yesterday. Then I ran over him and backed up to run into him again.")


if __name__ == '__main__':
    socketio.run(app)
