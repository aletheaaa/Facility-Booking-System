<template>
 <div class="container">
        <h1 class="display-1 text-light font-weight-bold">All Upcoming Bookings</h1>
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
 </div>

</template>

<script>
export default {
    name: 'Admin',
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
        // getCurrentUserEmail()
        // .then(userEmail => {
        //     console.log(userEmail);
        //     if (userEmail) {
        //         return fetch(`http://localhost:5002/payment/getAccountID/${userEmail}`)
        //     }
        //     else{
        //         router.push('/')
        //         throw new Error('User email not found');
        //     }
        // })
        // .then(response => response.json())
        // .then(data => {
        //     this.userID = data.data.accountID;
        //     console.log(this.userID)
        //     return fetch('http://localhost:5001/bookinglog/getByaccountID/' + this.userID);
        // })
        // .then(response => response.json())
        // .then(data => {
        //     this.bookedRooms = data.data.bookinglogs;
        //     console.log(this.bookedRooms)
        //     // for each room in the list of bookedRooms, we will get the relevant information using the bookingID to call getbybookingID
        //     // to get the bookingDate, startTime, endTime, and roomStatus
        //     for (let i = 0; i < this.bookedRooms.length; i++) {
        //         console.log(this.bookedRooms[i].bookingID)
        //         fetch('http://localhost:5001/bookinglog/getBybookingID/' + this.bookedRooms[i].bookingID)
        //         .then(response => response.json())
        //         .then(data => {
        //             // console.log(data.data)
        //             Object.assign(this.bookedRooms[i], data.data)
        //             // console.log(this.bookedRooms[i])
        //             this.bookedRooms[i].bookingDate = this.bookedRooms[i].startTime.slice(0,16);
        //             this.bookedRooms[i].startTime = this.bookedRooms[i].startTime.slice(-11,-3);
        //             this.bookedRooms[i].endTime = this.bookedRooms[i].endTime.slice(-11,-3);
        //             const allAccepted = this.bookedRooms[i].coBooker.every(coBooker => coBooker.acceptStatus === 'True');
        //             this.bookedRooms[i].roomStatus = allAccepted ? 'Confirmed' : 'Unconfirmed';
        //             fetch('http://localhost:8080/rooms/' + this.bookedRooms[i].roomId)
        //             .then(response => response.json())
        //             .then(data => {
        //                 this.bookedRooms[i].roomName = data.data.roomName;
        //                 console.log(this.bookedRooms[i].roomName)
        //             }).catch(error => console.error(error));
        //         }).catch(error => console.error(error));
        //     }
        // }).catch(error => console.error(error));
        fetch("http://localhost:5001/bookinglog/getTaken", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
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
        
    },
    
    
    methods: {
        cancelBooking(bookingID) {
            console.log(bookingID)
            fetch('http://localhost:5001/bookinglog/delete/' + bookingID, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.status === 'success') {
                    alert('Booking cancelled successfully');
                    window.location.reload();
                }
                else {
                    alert('Booking cancellation failed');
                }
            })
            .catch(error => console.error(error));
        }
        },
}
</script>