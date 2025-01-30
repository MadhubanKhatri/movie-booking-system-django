const seats = document.querySelectorAll(".seat");
let selectedSeats = [];

seats.forEach(seat => {
    seat.addEventListener("click", () => {
        seat.classList.toggle("selected");
        const seatNumber = seat.dataset.seat;

        if (selectedSeats.includes(seatNumber)) {
            selectedSeats = selectedSeats.filter(s => s !== seatNumber);
        } else {
            selectedSeats.push(seatNumber);
        }
    });
});    


document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("confirm-selection").addEventListener("click", () => {
        fetch("/book-seats/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")  // Ensure CSRF protection
          },
          body: JSON.stringify({ seats: selectedSeats, user: localStorage.getItem('user'), 
            movieId: localStorage.getItem('movie_id'), showTime: localStorage.getItem('show_time') })
        }).then(response => response.json())
        .then(data => {
          console.log(data); // Logs the JSON response
          if (data.message) {
            alert(data.message);
          } else {
            alert("Error occurred while booking.");
          }
        });
      });
});



// Helper function to get CSRF token
function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.substring(0, name.length + 1) === `${name}=`) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
    }
    }
}
return cookieValue;
}