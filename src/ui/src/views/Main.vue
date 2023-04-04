<template>
    <!-- <nav>
        <button @click="signout()">
            Sign Out
        </button>
    </nav> -->
    <div class="booking-cta">
        <h1 class="display-1 text-light font-weight-bold">SMU <br>Facilities Booking System</h1>
    </div>
    <div id="app">
        <div id="booking" class="container" v-show="!displayRooms">
            <div class="booking-form w-100 p-5 bg-light">
                <div class="form-group">
                    <span class="form-label">Room Location</span>
                    <select class="form-control" id="location" v-model="roomlocation" >
                        <option value="School of Accountancy">SOA</option>
                        <option value="School of Business">SOB</option>
                        <option value="School of Computing and Information Systems">SCIS</option>
                        <option value="School of Economics">SOE</option>
                        <option value="School of Social Sciences">SOSS</option>
                    </select>
                    <span class="select-arrow"></span>
                </div>
                <div class="form-group">
                    <span class="form-label">Room Type</span>
                    <select class="form-control" id="roomtype" v-model="roomtype" required>
                        <option value="Seminar Room">Seminar Room</option>
                        <option value="Group Study Room">Group Study Room</option>
                        <option value="Classroom">Classroom</option>
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
                            <select name="time" id="starttime" class="form-control" v-model="starttime">
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
                            <span class="form-label">End Time</span>
                            <select name="time" id="endtime" class="form-control" v-model="endtime">
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
                </div>
                <div class="form-btn">
                    <button class="btn btn-primary btn-lg" @click="findRooms()">Find rooms</button>
                </div>
            </div>
            
            
        </div>
        
        <div id="rooms" class="section" v-show="displayRooms">
            <table class="table table-hover table-light" v-if="rooms">
                <thead>
                    <tr>
                        <th scope="col">Room ID</th>
                        <th scope="col">Room Name</th>
                        <th scope="col">Room Type</th>
                        <th scope="col">Book Room</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="room in rooms">
                        <th scope="row">{{room.roomId}}</th>
                        <td>{{room.roomName}}</td>
                        <td>{{room.roomType}}</td>
                        <td><button class="submit-btn btn-primary" @click="bookRoom(room.roomId)">Book Room</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import router from '../router'
export default {
    name: 'Main',
    data() {
        return {
            roomlocation: '',
            roomtype: '',
            date: '',
            starttime: '',
            endtime: '',
            rooms: [],
            takenRooms: [],
            displayRooms: false,
            get_rooms : "http://localhost:5004/accessTakenBooking",
            get_all_rooms: "http://localhost:8080/rooms",
            allRooms: [],
        }
    },
    mounted() {
        fetch(this.get_all_rooms)
        .then(response => response.json()) // Parse response body as JSON
        .then(response => {
            console.log(response.data)
            this.allRooms = response.data
        })
        .catch(err => {
            console.log(`Error getting documents`, err);
        });
    },
    methods: {  
        findRooms() {
            this.displayRooms = true;
            // console.log(this.roomlocation);
            // console.log(this.roomtype);
            // console.log(this.date);
            // console.log(this.starttime);
            // console.log(this.duration);
            var roomlocarray = [];
            var roomtypearray = [];
            roomtypearray.push(this.roomtype);
            roomlocarray.push(this.roomlocation);
            // this.rooms = this.getAllRooms();
            var bodydata = {
                "roomType": roomtypearray,
                "location": roomlocarray,
                "dateChosen": this.date,
            }
            fetch(this.get_rooms, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(bodydata)
            })
            .then(response => response.json()) // Parse response body as JSON
            .then(data => {
                if (data.data.data.length == 0) {
                    this.rooms = this.allRooms;
                    return;
                }
                this.takenRooms = data.data.data;
                console.log(data.data.data)
                const takenIDs = this.takenRooms.map(booking => booking.bookingID);
                for (var i = 0; i < this.allRooms.length; i++) {
                    var currentRoom = this.allRooms[i];
                    console.log(currentRoom);
                    var currentRoomID = this.allRooms[i].roomId;
                    console.log(currentRoomID)
                    if (!takenIDs.includes(currentRoomID)) {
                        this.rooms.push(currentRoom);
                    }
                }
                console.log(this.rooms);
                
            })
            .catch(error => console.error(error))
            this.rooms = this.allRooms;
            return;
        }, // Do something with the data
        
        bookRoom(roomId) {
            console.log("book room");
            console.log(roomId);
            console.log(this.rooms[roomId]);
            router.push({ 
                path: '/book', 
                query: { bookingInfo: JSON.stringify(this.rooms[roomId]),
                    date: this.date,
                    starttime: this.starttime,
                    endtime: this.endtime } 
                })
                
            }
            
        },
    }
</script>