
 document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#submit').disabled = true;

    document.querySelector('#channel').onkeyup = () => {

 
        if (document.querySelector('#channel').value.length > 0)
            document.querySelector('#submit').disabled = false;
        else
            document.querySelector('#submit').disabled = true;
    };

    document.querySelector('#new-channel').onsubmit = () => {

        // Create new item for list

        var channel_name = document.getElementById("channel").value;

        socket.emit('add channel', channel_name);
        socket.on('current_channel_list', function(data) {

            document.querySelector('#channels').innerHTML =  data.ch_list;
        }); 
         
        // Clear input field and disable button again
        document.querySelector('#channel').value = '';
        document.querySelector('#submit').disabled = true;

        socket.on('error', function(data) {

            if ((data.error_msg != "") && (data.channel == channel_name)){
             alert("channel already exists");
             }
         });

        return false;

    };
 
 
});


        
