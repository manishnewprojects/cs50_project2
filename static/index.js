
 document.addEventListener('DOMContentLoaded', () => {


    // By default, submit button is disabled
    document.querySelector('#submit').disabled = true;

    // Enable button only if there is text in the input field
    document.querySelector('#channel').onkeyup = () => {

        document.querySelector('#error_message').innerHTML = ""

        if (document.querySelector('#channel').value.length > 0)
            document.querySelector('#submit').disabled = false;
        else
            document.querySelector('#submit').disabled = true;
    };

    document.querySelector('#new-channel').onsubmit = () => {

        // Create new item for list
        //const li = document.createElement('li');
        //li.innerHTML = document.querySelector('#channel').value;

        var channel_name = document.getElementById("channel").value;

        socket.emit('add channel', channel_name);

        socket.on('current_channel_list', function(data) {

            document.querySelector('#channels').innerHTML =  data.ch_list;
        }); 
         
        // Clear input field and disable button again
        document.querySelector('#channel').value = '';
        document.querySelector('#submit').disabled = true;

        // Stop form from submitting
        return false;
    };

    socket.on('error', function(data) {
         if (data.error_msg != "") {
            document.querySelector('#error_message').innerHTML = data.error_msg;
        }
    });

 
});


        
