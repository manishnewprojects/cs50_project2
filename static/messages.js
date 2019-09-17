

document.addEventListener('DOMContentLoaded', () => {

socket.emit('leave_now');

socket.emit('join_now');

localStorage.setItem('channel',document.querySelector('#current_channel').innerHTML);

socket.on('message_history', function(data) {

        document.querySelector('#messages').innerHTML = data.chat_so_far ;

    });

// By default, submit button is disabled
document.querySelector('#message_submit').disabled = true;

// Enable button only if there is text in the input field
    document.querySelector('#message').onkeyup = () => {

 
        if (document.querySelector('#message').value.length > 0)
            document.querySelector('#message_submit').disabled = false;
        else
            document.querySelector('#message_submit').disabled = true;
    };

 document.querySelector('#new-message').onsubmit = () => {

	var message = document.getElementById("message").value;

    socket.emit('message posted', {'message':message, 'channel': localStorage.getItem('channel')});

    socket.on('message_buffer', function(data) {

 
        if ( data.channel.replace(/\s/g,"") == localStorage.getItem('channel').replace(/\s/g,"") )
        {
            document.querySelector('#messages').innerHTML = data.chat_history ;
        }

});


     // Clear input field and disable button again
document.querySelector('#message').value = '';
document.querySelector('#message_submit').disabled = true;

    // Stop form from submitting
return false;

 }


});
 