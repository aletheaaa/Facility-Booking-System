<template>
    <div class="booking-cta">
        <h1 class="display-1 text-light font-weight-bold">SMU <br>Facilities Booking System</h1>
    </div>
    <div class="container">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th scope="col">Room ID</th>
                    <th scope="col">Room Name</th>
                    <th scope="col">Room Status</th>
                    <th scope="col">Booking Date</th>
                </tr>
            </thead>
            
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
export default {
    name: 'Account',
    data() {
        return {

        }
    },
    methods: {
        confirmBooking() {
            // alert("Booking Confirmed!")
        }
    },
}
</script>