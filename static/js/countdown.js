// Set your target date and time here (year, month (0-11), day, hour, minute, second)
var targetDate = new Date(2023, 0, 1, 0, 0, 0).getTime();

// Function to update the countdown
function updateCountdown() {
    var currentDate = new Date().getTime();
    var timeLeft = targetDate - currentDate;

    if (timeLeft <= 0) {
        // Time's up, perform your automatic redirect
        window.location.replace("https://example.com"); // Replace with your URL
        return;
    }

    var days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
    var hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

    document.getElementById("days").querySelector(".timer-number").innerHTML = days;
    document.getElementById("hours").querySelector(".timer-number").innerHTML = hours;
    document.getElementById("minutes").querySelector(".timer-number").innerHTML = minutes;
    document.getElementById("seconds").querySelector(".timer-number").innerHTML = seconds;
}

// Update the countdown every second
setInterval(updateCountdown, 1000);

// Initial call to set the countdown
updateCountdown();
