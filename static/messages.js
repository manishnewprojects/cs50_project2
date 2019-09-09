

document.addEventListener('DOMContentLoaded', () => {



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

   //document.querySelector('#messages').innerHTML = data.chat_history['user']+":&nbsp"+data.chat_history['message']+"<br>";
   document.querySelector('#messages').innerHTML = data.chat_history['message'] ;

    });


     // Clear input field and disable button again
    document.querySelector('#message').value = '';
    document.querySelector('#message_submit').disabled = true;

    // Stop form from submitting
    return false;
 }

 

});
 