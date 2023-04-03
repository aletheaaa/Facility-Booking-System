<template>
    <div class="booking-cta">
        <h1 class="display-1 text-light font-weight-bold">SMU <br>Facilities Booking System</h1>
        <!-- test button -->
        <button class="btn btn-primary" @click="getCurrentUserEmail()">Get user email </button>
    </div>
    <div class="container">
        <table class="table table-light">
            <thead>
                <tr>
                    <th scope="col">Room ID</th>
                    <th scope="col">Room Name</th>
                    <th scope="col">Room Status</th>
                    <th scope="col">Booking Date</th>
                    <th scope="col">Start Time</th>
                    <th scope="col">End Time</th>
                </tr>
            </thead>
            <tbody id="booked">
                <tr>
                    <td scope="col">{{ bookedRooms.roomId }}</td>
                    <td scope="col">{{ roomName }}</td>
                    <td scope="col">{{ bookedRooms.roomStatus }}</td>
                    <td scope="col">{{ bookingDate }}</td>
                    <td scope="col">{{ startTime }}</td>
                    <td scope="col">{{ endTime }}</td>
                </tr>
            </tbody>
        </table>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th scope="col">Room ID</th>
                    <th scope="col">Room Name</th>
                    <th scope="col">Booking Date</th>
                    <th scope="col">Room Status</th>
                </tr>
            </thead>
            <tr>
                <td scope="col">Room ID</td>
                <td scope="col">Room Name</td>
                <td scope="col">Booking Date</td>
                <td><button class="btn btn-primary" @click="confirmBooking()">Confirm Booking</button></td>
            </tr>
        </table>
    </div>
</template>

<script>
import { getCurrentUserEmail } from '../utils'
export default {
    name: 'Account',
    data() {
        return {
            bookedRooms: [],
            userID: 0,
            roomID: 0,
            roomName: '',
            startTime: '',
            endTime: '',
            bookingDate: '',
        }
    },
    
    mounted() {
        getCurrentUserEmail()
        .then(userEmail => {
            console.log(userEmail);
            if (userEmail) {
                return fetch(`http://localhost:5002/payment/getAccountID/${userEmail}`)
            }
            throw new Error('User email not found');
        })
        .then(response => response.json())
        .then(data => {
            this.userID = data.data.accountID;
            console.log(this.userID)
            return fetch('http://localhost:5001/bookinglog/' + this.userID);
        })
        .then(response => response.json())
        .then(data => {
            if (data.code === 200) {
                this.bookedRooms = data.data;
                console.log(this.bookedRooms)
                this.roomID = this.bookedRooms.roomId;
                console.log(this.roomID)
                this.startTime = this.bookedRooms.startTime.slice(-11,-3);
                this.endTime = this.bookedRooms.endTime.slice(-11,-3);
                this.bookingDate = this.bookedRooms.startTime.slice(0,10);
                const allAccepted = this.bookedRooms.coBooker.every(coBooker => coBooker.acceptStatus === 'True');
                this.bookedRooms.roomStatus = allAccepted ? 'Confirmed' : 'Unconfirmed';
                this.roomName = fetch('http://localhost:8080/room/' + this.roomID)
            } else {
                console.log('Failed to fetch booking data.');
            }
        })
        .catch(error => console.error(error));
    }
    ,
    
    
    methods: {
        confirmBooking() {
            // alert("Booking Confirmed!")
        },
        getCurrentUserEmail
    },
}
</script>