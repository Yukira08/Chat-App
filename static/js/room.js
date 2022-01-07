<script>
    var room_id = {{ room_id }};
    var roomName = {{ room_name_json }};
    console.log(document.getElementById('id_short_text').value);
    var chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + room_id + '/');
    chatSocket.onopen = function(){
        console.log("Connecting...");
        var prevmes = {{messages}};
        document.querySelector("#chat-log").value+=prevmes;
    }
    chatSocket.onmessage = function(e) {    
        var data = JSON.parse(e.data); var message = data['message'];
        console.log(data);
        document.querySelector('#chat-log').value += (message);
    };
    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
    document.querySelector('#id_short_text').focus();
    document.querySelector('#id_short_text').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };
    document.querySelector('#chat-message-submit').onclick = function(e) {
        var messageInputDom = document.querySelector('#id_short_text');
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({'message': message, 'room_id' : room_id,'raw': 'none'}));
        messageInputDom.value = '';
    };
</script>