<template>
    <div class="booking-cta">
        <h1 class="display-1 text-light font-weight-bold">SMU <br>Facilities Booking System</h1>
    </div>
    <div id="app">
        <div id="booking" class="container">
            <div class="booking-form w-100 p-5 bg-light">
                <h2>Please confirm your booking!</h2>
                <div class="container">
                    <h3>Booking details:</h3>
                    <ul>
                        <li>Room ID: {{ bookingInfo.roomId }}</li>
                        <li>Room Name: {{ bookingInfo.roomName }}</li>
                        <li>Room Type: {{ bookingInfo.roomType }}</li>
                        <li>Location: {{ bookingInfo.location }}</li>
                        <li>Capacity: {{ bookingInfo.capacity }}</li>
                        <!-- <li>Price: {{ price }}</li> -->
                    </ul>
                </div>
                <div class="container">
                    <h3>Booking time:</h3>
                    <ul>
                        <!-- TODO: get this info from prev page as well -->
                        <li>Date: {{ date }}</li>
                        <li>Start time: {{ startTime }}</li>
                        <li>End time: {{ endTime }}</li>
                    </ul>
                </div>
                <div class="container">
                    <h3>Co-Booker Details</h3>
                    <ol v-show="this.cobooker.length > 0" >
                        <li v-for="booker in this.cobooker">
                            Email : {{ booker }}
                        </li>
                    </ol>
                    <p v-show="this.cobooker.length == 0">
                        No co-bookers
                    </p>
                    <p>Enter new email:
                        <input type="email" name="" id="newBooker" style="margin-right: 10px"> 
                        <button class="btn btn-primary" @click="addCoBooker">Add</button>
                    </p>
   

                </div>
                <button class="btn btn-lg btn-danger mt-3" @click="createBooking">
                    <!-- TODO: add makeBooking functionality -->
                    Confirm Booking
                </button>
            </div>
        </div>
        
    </div>
</template>
<script>
// import axios from axios;
export default {
    name: 'BookRoom',
    data() {
        return {
            bookingInfo: JSON.parse(this.$route.query.bookingInfo),
            date: this.$route.query.date,
            startTime: this.$route.query.startTime,
            endTime: this.$route.query.endTime,
            bookingLogs: "http://localhost:5100/makeBooking",
            accountInfo: "http://localhost:5002/payment/getAccountID/",
            cobooker: [],
        };
    },
    
    mounted() {
        // this.bookingInfo = JSON.parse(this.$route.query.bookingInfo);
        console.log(this.bookingInfo);
        
        // Changing Time Format
        // From UI, format is like this:
        const startTimeInHrs = this.$route.query.startTime; // this.startTime = '1500';
        const endTimeInHrs = this.$route.query.endTime;     // this.endTime = '1700';
        const dateChosen = this.$route.query.date           // this.date = '2021-01-13';
        // Need to change to below format to match makeBooking service input reqs e.g. startTime = "YYYY-MM-DD HH:MM:SS";
        this.startTime = dateChosen + " " + startTimeInHrs.slice(0,2) + ':' + startTimeInHrs.slice(2) + ':00';
        this.endTime   = dateChosen + " " + endTimeInHrs.slice(0,2) + ':' + endTimeInHrs.slice(2) + ':00';
        console.log(this.bookingInfo);




    },
    methods: {
        addCoBooker() {
            const newBooker = document.getElementById("newBooker").value;
            if (newBooker !== '') {
            this.cobooker.push(newBooker);
            console.log(newBooker)
            document.getElementById("newBooker").value = "";
            console.log(newBooker)

            }
        },

        createBooking(){
            const newBooking = {
                // "accountID": this.getAccountID(), // get accountID from payment[email]
                "accountID": 1,

                "startTime": this.startTime,
                "endTime": this.endTime,

                // "price": this.getPrice(), // get price from rooms service[cost]
                "price": 5,

                // "roomID": this.bookingInfo.roomId,
                "roomID": 1,

                "coBooker": this.cobooker
            }
            console.log(newBooking);
            fetch(this.bookingLogs, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newBooking)
            })
            .then(response => response.json()) 
            .then(data => {
                console.log(data)
            }) 
            .catch(error => console.error(error));
        },


        // created a function get accountID from payment but it always throw error saying no CORS access
        getAccountID() {
            fetch(this.accountInfo + this.email) // from Login page
            .then(response => response.json()) // Parse response body as JSON
            .then(response => {
            
                const accountData = response;
                console.log(accountData.data)
                this.accountID = [accountData.data.account];
                console.log(accountID)
                return this.accountID;
                
            })
            .catch(err => {
                console.log(`Error getting accountID`, err);
            });
        },
        
        getPrice(){
            fetch('localhost:8080/rooms/' + this.bookingInfo.roomId) 
            .then(response => response.json()) 
            .then(response => {
            
                const accountData = response;
                console.log(accountData.data)
                this.price = accountData.data.cost;
                console.log(this.price)
                // Rooms has a function called getCost() but i'm not sure how to use it 
                return this.price;
                
            }) 
            .catch(err => {
                console.log(`Error getting price`, err);
            });
        }

    }
}
</script>