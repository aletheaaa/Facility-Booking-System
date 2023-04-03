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
                    <h3>Add a Co-Booker:</h3>
                    <!-- TODO: add text input field -->
                    <p>Co-Booker email: </p>
                    <input type="email" name="" id="">
                </div>
                <button class="btn btn-lg btn-danger mt-3">
                    <!-- TODO: add makeBooking functionality -->
                    Confirm Booking
                </button>
            </div>
        </div>
        
    </div>
</template>
<script>
export default {
    name: 'BookRoom',
    data() {
        return {
            bookingInfo: [],
            date: '',
            startTime: '',
            endTime: '',
        };
    },
    mounted() {
        this.bookingInfo = JSON.parse(this.$route.query.bookingInfo);
        this.date = this.$route.query.date;
        this.startTime = this.$route.query.startTime;
        this.endTime = this.$route.query.endTime;
    },
    methods: {},
};
</script>