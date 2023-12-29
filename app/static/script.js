
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

var brocker= new EventSource('/sse');

brocker.onmessage = function(event) {
    var sseData = document.getElementById('sse-data');
    sseData.value = event.data;
};