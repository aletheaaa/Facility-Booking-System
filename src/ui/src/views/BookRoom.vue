<template>
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
                        <!-- todo: get this info from prev page as well -->
                        <li>Date: {{ bookingInfo.date }}</li>
                        <li>Start time: {{ bookingInfo.startTime }}</li>
                        <li>End time: {{ bookingInfo.endTime }}</li>
                    </ul>
                </div>
                <div class="container">
                    <h3>Add a Co-Booker:</h3>
                    <!-- todo: add text input field -->
                    <p>Co-Booker email: </p>
                    <input type="email" name="" id="">
                </div>
                <button class="btn btn-lg btn-danger mt-3">
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
        };
    },
    mounted() {
        this.bookingInfo = JSON.parse(this.$route.query.bookingInfo);
    },
    methods: {},
};
</script>