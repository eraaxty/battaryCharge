
        function clearMessage() {
            setTimeout(function() {
                document.getElementById("response").value = "";
            }, 7000);
    }
window.onload = clearMessage;

    function showKvitto() {
            var kvittoDiv = document.getElementById("kvitto");
            kvittoDiv.style.display = "block"; // Show the div

            //setTimeout(function () {
            //  kvittoDiv.style.display = "none";
            //}, 7000);
        }

var socket = io.connect('http://' + window.location.hostname + ':' + location.port);
socket.on('new_message', function(data) {
    // Handle the payload here. For example, you can log it to the console:
    console.log(data.message);
});
