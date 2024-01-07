
        function clearMessage() {
            setTimeout(function() {
                document.getElementById("response").value = "";
            }, 7000);
    }

window.onload = function() {
    clearMessage();

    setInterval(function() {
        var now = new Date();
        var hours = now.getHours();
        var minutes = now.getMinutes();

        // Add leading zeros if necessary
        hours = (hours < 10) ? "0" + hours : hours;
        minutes = (minutes < 10) ? "0" + minutes : minutes;

        var timeString = hours + ":" + minutes;

        document.getElementById('time').value = timeString;
    }, 1000);

};

var brocker= new EventSource('/sse');

brocker.onmessage = function(event) {
    var sseData = document.getElementById('sse-data');
    sseData.value = event.data;

    var controlInputs = document.getElementById('part_control').getElementsByTagName('input');

    // Loop through each input element
    for (var i = 0; i < controlInputs.length; i++) {
        // Add an event listener to the input element
        controlInputs[i].addEventListener('input', function(e) {
            // Get the id of the input element in the part_feedback form
            var feedbackInputId = e.target.id + '_feedback';

            // Get the input element in the part_feedback form
            var feedbackInput = document.getElementById(feedbackInputId);

            // Update the value of the input element in the part_feedback form
            if (feedbackInput) {
                feedbackInput.value = e.target.value;
            }
        });
    }

};





