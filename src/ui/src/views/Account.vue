<template>
    <!-- <div class="booking-cta">
        <h1 class="display-1 text-light font-weight-bold">SMU <br>Facilities Booking System</h1>
    </div> -->
    <div class="container">
        <h1 class="display-1 text-light font-weight-bold">Upcoming Bookings</h1>
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
                <tr v-for="room in bookedRooms" :key="room.bookingID">
                    <td>{{ room.bookingID }}</td>
                    <td>{{ room.roomName }}</td>
                    <td>{{ room.roomStatus }}</td>
                    <td>{{ room.bookingDate }}</td>
                    <td>{{ room.startTime }}</td>
                    <td>{{ room.endTime }}</td>
                </tr>
            </tbody>
        </table>
        <h1 class="display-1 text-light font-weight-bold mt-5">Co-Booked Rooms</h1>
        <table class="table table-light">
            <thead>
                <tr>
                    <th scope="col">Room ID</th>
                    <th scope="col">Room Name</th>
                    <th scope="col">Room Status</th>
                    <th scope="col">Booking Date</th>
                    <th scope="col">Start Time</th>
                    <th scope="col">End Time</th>
                    <th scope="col">Confirm Booking</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="room in coBookedRooms" :key="room.bookingID">
                    <td>{{ room.bookingID }}</td>
                    <td>{{ room.roomName }}</td>
                    <td>{{ room.roomStatus }}</td>
                    <td>{{ room.bookingDate }}</td>
                    <td>{{ room.startTime }}</td>
                    <td>{{ room.endTime }}</td>
                    <td><button class="btn btn-primary" @click="confirmBooking(room.bookingID)">Confirm Booking</button></td>
                </tr>
            </tbody>
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
            coBookedRooms: [],
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
            return fetch('http://localhost:5001/bookinglog/getByaccountID/' + this.userID);
        })
        .then(response => response.json())
        .then(data => {
            this.bookedRooms = data.data.bookinglogs;
            console.log(this.bookedRooms)
            // for each room in the list of bookedRooms, we will get the relevant information using the bookingID to call getbybookingID
            // to get the bookingDate, startTime, endTime, and roomStatus
            for (let i = 0; i < this.bookedRooms.length; i++) {
                console.log(this.bookedRooms[i].bookingID)
                fetch('http://localhost:5001/bookinglog/getBybookingID/' + this.bookedRooms[i].bookingID)
                .then(response => response.json())
                .then(data => {
                    // console.log(data.data)
                    Object.assign(this.bookedRooms[i], data.data)
                    // console.log(this.bookedRooms[i])
                    this.bookedRooms[i].bookingDate = this.bookedRooms[i].startTime.slice(0,16);
                    this.bookedRooms[i].startTime = this.bookedRooms[i].startTime.slice(-11,-3);
                    this.bookedRooms[i].endTime = this.bookedRooms[i].endTime.slice(-11,-3);
                    const allAccepted = this.bookedRooms[i].coBooker.every(coBooker => coBooker.acceptStatus === 'True');
                    this.bookedRooms[i].roomStatus = allAccepted ? 'Confirmed' : 'Unconfirmed';
                    fetch('http://localhost:8080/rooms/' + this.bookedRooms[i].roomId)
                    .then(response => response.json())
                    .then(data => {
                        this.bookedRooms[i].roomName = data.data.roomName;
                        console.log(this.bookedRooms[i].roomName)
                    }).catch(error => console.error(error));
                }).catch(error => console.error(error));
            }
        }).catch(error => console.error(error));

        // get coBookedRooms
        fetch('http://localhost:5001/bookinglog/coBooker/2' )
        .then(response => response.json())
        .then(data => {
            this.coBookedRooms = data.data.bookinglogs;
            console.log(this.coBookedRooms)
            // for each room in the list of coBookedRooms, we will get the relevant information using the bookingID to call getbybookingID
            // to get the bookingDate, startTime, endTime, and roomStatus
            for (let i = 0; i < this.coBookedRooms.length; i++) {
                console.log(this.coBookedRooms[i].bookingID)
                fetch('http://localhost:5001/bookinglog/getBybookingID/' + this.coBookedRooms[i].bookingID)
                .then(response => response.json())
                .then(data => {
                    // console.log(data.data)
                    Object.assign(this.coBookedRooms[i], data.data)
                    // console.log(this.coBookedRooms[i])
                    this.coBookedRooms[i].bookingDate = this.coBookedRooms[i].startTime.slice(0,16);
                    this.coBookedRooms[i].startTime = this.coBookedRooms[i].startTime.slice(-11,-3);
                    this.coBookedRooms[i].endTime = this.coBookedRooms[i].endTime.slice(-11,-3);
                    const allAccepted = this.coBookedRooms[i].coBooker.every(coBooker => coBooker.acceptStatus === 'True');
                    this.coBookedRooms[i].roomStatus = allAccepted ? 'Confirmed' : 'Unconfirmed';
                    // now we get room name using getroombyroomid
                    fetch('http://localhost:8080/rooms/' + this.coBookedRooms[i].roomId)
                    .then(response => response.json())
                    .then(data => {
                        this.coBookedRooms[i].roomName = data.data.roomName;
                        console.log(this.coBookedRooms[i].roomName)
                    }).catch(error => console.error(error));
                }).catch(error => console.error(error));
            }
        }).catch(error => console.error(error));
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