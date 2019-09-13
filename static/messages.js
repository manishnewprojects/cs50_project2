

document.addEventListener('DOMContentLoaded', () => {

socket.emit('leave_now');

socket.emit('join_now');

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

    socket.emit('message posted', message);

    socket.on('message_buffer', function(data) {

        document.querySelector('#messages').innerHTML = data.chat_history ;

    });


     // Clear input field and disable button again
    document.querySelector('#message').value = '';
    document.querySelector('#message_submit').disabled = true;

    // Stop form from submitting
    return false;
 }

 

});
 