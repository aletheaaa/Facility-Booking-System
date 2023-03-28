<template>
    <!-- <nav>
        <button @click="signout()">
            Sign Out
        </button>
    </nav> -->
    <div class="booking-cta" v-show="!displayRooms">
        <h1 class="display-1 text-light font-weight-bold">SMU <br>Facilities Booking System</h1>
    </div>
    <div id="app">
        <div id="booking" class="container" v-show="!displayRooms">
            <div class="booking-form w-100 p-5 bg-light">
                <div class="form-group">
                    <span class="form-label">Room Location</span>
                    <select class="form-control" id="location" v-model="roomlocation" required>
                        <option value="soa">SOA</option>
                        <option value="sob">SOB</option>
                        <option value="scis">SCIS</option>
                        <option value="soe">SOE</option>
                        <option value="soss">SOSS</option>
                    </select>
                    <span class="select-arrow"></span>
                </div>
                <div class="form-group">
                    <span class="form-label">Room Type</span>
                    <select class="form-control" id="roomtype" v-model="roomtype" required>
                        <option value="seminar">Seminar Room</option>
                        <option value="Group Study Room">Group Study Room</option>
                        <option value="classroom">Classroom</option>
                    </select>
                    <span class="select-arrow"></span>
                </div>
                <div class="form-group">
                    <span class="form-label">Date</span>
                    <input class="form-control" type="date" id="date" v-model="date" required>
                </div>
                <div class="row">
                    <div class="col-sm-6">
                        <div class="form-group">
                            <span class="form-label">Start Time</span>
                            <select name="time" id="time" class="form-control" v-model="starttime">
                                <option value="0800">0800</option>
                                <option value="0830">0830</option>
                                <option value="0900">0900</option>
                                <option value="0930">0930</option>
                                <option value="1000">1000</option>
                                <option value="1030">1030</option>
                                <option value="1100">1100</option>
                                <option value="1130">1130</option>
                                <option value="1200">1200</option>
                                <option value="1230">1230</option>
                                <option value="1300">1300</option>
                                <option value="1330">1330</option>
                                <option value="1400">1400</option>
                                <option value="1430">1430</option>
                                <option value="1500">1500</option>
                                <option value="1530">1530</option>
                                <option value="1600">1600</option>
                                <option value="1630">1630</option>
                                <option value="1700">1700</option>
                                <option value="1730">1730</option>
                                <option value="1800">1800</option>
                                <option value="1830">1830</option>
                                <option value="1900">1900</option>
                                <option value="1930">1930</option>
                                <option value="2000">2000</option>
                                <option value="2030">2030</option>
                                <option value="2100">2100</option>
                                <option value="2130">2130</option>
                                <option value="2200">2200</option>
                            </select>
                            <span class="select-arrow"></span>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="form-group">
                            <span class="form-label">Duration</span>
                            <select class="form-control" id="duration" v-model="duration" required>
                                <option>1</option>
                                <option>2</option>
                                <option>3</option>
                            </select>
                            <span class="select-arrow"></span>
                        </div>
                    </div>
                </div>
                <div class="form-btn">
                    <button class="btn btn-primary btn-lg" @click="findRooms()">Find rooms</button>
                </div>
            </div>
            
            
        </div>
        
        <div id="rooms" class="section" v-show="displayRooms">
            <table class="table table-striped" v-if="rooms">
                <thead>
                    <tr>
                        <th scope="col">Room ID</th>
                        <th scope="col">Room Name</th>
                        <th scope="col">Room Type</th>
                        <th scope="col">Room Location</th>
                        <th scope="col">Room Status</th>
                        <th scope="col">Room Booking</th>
                        <th scope="col">Book Room</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="room in rooms">
                        <th scope="row">{{room.room_id}}</th>
                        <td>{{room.room_name}}</td>
                        <td>{{room.room_type}}</td>
                        <td>{{room.room_location}}</td>
                        <td>{{room.room_status}}</td>
                        <td>{{room.room_booking}}</td>
                        <td><button class="submit-btn btn-primary" @click="bookRoom()">Book Room</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import { signout } from '../utils'
export default {
    name: 'Main',
    data() {
        return {
            roomlocation: '',
            roomtype: '',
            date: '',
            starttime: '',
            duration: '',
            rooms: [],
            displayRooms: false,
            get_rooms : "http://localhost:8080/rooms"
        }
    },
    methods: {
        findRooms() {
            this.displayRooms = true;
            console.log(this.roomlocation);
            console.log(this.roomtype);
            console.log(this.date);
            console.log(this.starttime);
            console.log(this.duration);
            //fetch rooms 
            // fetch(`${get_rooms}?location=${this.roomlocation}&type=${this.roomtype}&date=${this.date}&starttime=${this.starttime}&duration=${this.duration}}`,
            fetch(this.get_rooms)
            .then(response => response.json())
            .then(data => {
                this.rooms = data;
                console.log(this.rooms);
                
            })
            .catch(error => {
                // Errors when calling the service; such as network error, 
                // service offline, etc
                console.log(this.message + error);
                
            });
        },
        bookRoom() {
            console.log("book room");
        },
        signout
        
    },
}
</script>