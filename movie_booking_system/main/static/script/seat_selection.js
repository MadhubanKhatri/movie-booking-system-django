document.addEventListener("DOMContentLoaded", function () {
  const show_date = document.getElementById("show_date");
  show_date.innerHTML = localStorage.getItem('booking_date');

  const show_time = document.getElementById("show_time");
  show_time.innerHTML = localStorage.getItem('show_time');


  const seats = document.querySelectorAll(".seat");
  let selectedSeats = [];

  seats.forEach(seat => {
      seat.addEventListener("click", () => {
          seat.classList.toggle("selected");
          const seatNumber = seat.dataset.seat;
          
          if (selectedSeats.includes(seatNumber) || seat.classList.contains("occupied")) {
              selectedSeats = selectedSeats.filter(s => s !== seatNumber);
          } else {
              selectedSeats.push(seatNumber);
          }

          if(selectedSeats.length===0){
            document.getElementById("confirm-selection").style.display = "none";
         }else{
            document.getElementById("confirm-selection").style.display = "block";
         }  
      });
  }); 

    

    booked_seats = localStorage.getItem('booked_seats').split(',')

    if(booked_seats.length===1 && booked_seats[0]===""){
      booked_seats = [];
    }
    booked_seats.forEach(seat => {
      document.getElementById(seat).classList.add("occupied");
      document.getElementById(seat).style.backgroundColor = "#e0c4c4";
    });


     document.getElementById("confirm-selection").addEventListener("click", () => {
       if(selectedSeats.length===0){
         alert("Please select at least one seat to book.");
         return;
       }
       fetch("/payment_checkout/", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken")  // Ensure CSRF protection
            },
            body: JSON.stringify({ 
              seats: selectedSeats, 
              user: localStorage.getItem('user'), 
              movieId: localStorage.getItem('movie_id'), 
              showTime: localStorage.getItem('show_time'), 
              booking_date: localStorage.getItem('booking_date'),
              theatre_id: localStorage.getItem('theatre_id'), 
              show_price: localStorage.getItem('show_price') 
            })
       }).then(response => response.json())
       .then(data => {
        if(data.message){
          var options = {
      
            // Enter the Key ID generated from the Dashboard
            key: data.context["razorpay_merchant_key"], 
            amount: data.context["razorpay_amount"], 
            currency: data.context["currency"],
            name: "Dj Razorpay", 
            order_id: data.context["razorpay_order_id"], 
            callback_url: data.context["callback_url"],
          };
          
          // initialise razorpay with the options.
          var rzp1 = new Razorpay(options);
          rzp1.open();

        }
       })
        
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