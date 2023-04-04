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
                            Email : {{ allEmails[booker] }}
                        </li>
                    </ol>
                    <p v-show="this.cobooker.length == 0">
                        No co-bookers
                    </p>
                    <p>Enter new email:
                        <!-- <input type="email" name="" id="newBooker" style="margin-right: 10px">  -->
                        <!-- <button class="btn btn-primary" @click="addCoBooker">Add</button>-->
                        <select name="time" id="starttime" class="form-control" v-model="cobooker" multiple>
                            <option v-for="(email, ID) in allEmails" :value="ID">{{ email }}</option>
                        </select>
                        <span class="select-arrow"></span>
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
import { getCurrentUserEmail } from '../utils'
export default {
    name: 'BookRoom',
    data() {
        return {
            bookingInfo: JSON.parse(this.$route.query.bookingInfo),
            date: this.$route.query.date,
            startTime: this.$route.query.starttime,
            endTime: this.$route.query.endtime,
            bookingLogs: "http://localhost:5100/makeBooking",
            accountInfo: "http://localhost:5002/payment/getAccountID/",
            cobooker: [],
            allEmails: [],
            userID: 0,
            userEmail: '',
        };
    },
    
    mounted() {
        // this.bookingInfo = JSON.parse(this.$route.query.bookingInfo);
        console.log(this.bookingInfo);
        
        
        fetch('http://localhost:5002/payment/getAllAccounts')
        .then(response => response.json())
        .then(data => {
            this.allEmails = data.data.accounts.reduce((acc, curr) => {
                acc[curr.accountID] = curr.email;
                return acc;
            }, {});
            console.log(this.allEmails)
        })
        .catch(error => {
            console.error('Error fetching email list:', error);
        });
        
        
        getCurrentUserEmail()
        .then(userEmail => {
            this.userEmail = userEmail;
            console.log(userEmail);
            if (userEmail) {
                return fetch(`http://localhost:5002/payment/getAccountID/${userEmail}`)
            }
            else{
                router.push('/')
                throw new Error('User email not found');
            }
        })
        .then(response => response.json())
        .then(data => {
            this.userID = data.data.accountID;
            // console.log("user"+this.userID)
        }).catch(error => {
            console.error('Error fetching account ID:', error);
        });
        
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
                "accountID": this.userID,
                
                "accountEmail": this.userEmail,
                
                "startTime": `${this.date} ${this.startTime.slice(0, 2)}:${this.startTime.slice(2)}:00`,
                
                "endTime": `${this.date} ${this.endTime.slice(0, 2)}:${this.endTime.slice(2)}:00`,
                
                // "price": this.getPrice(), // get price from rooms service[cost]
                "price": this.getPrice(),
                
                // "roomID": this.bookingInfo.roomId,
                "roomID": this.bookingInfo.roomId,
                
                "roomName": [this.bookingInfo.roomName],
                
                "location": [this.bookingInfo.location],
                
                "coBookerIDs": [this.cobooker],
                
                "coBookerEmails": [this.cobooker.map(id => this.allEmails[id])],
            }
            console.log(newBooking);
            // fetch(this.bookingLogs, {
                //     method: 'POST',
                //     headers: {
                    //         'Content-Type': 'application/json'
                    //     },
                    //     body: JSON.stringify(newBooking)
                    // })
                    // .then(response => response.json()) 
                    // .then(data => {
                        //     console.log(data)
                        // }) 
                        // .catch(error => console.error(error));
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
                        const cost = this.bookingInfo.cost;
                        // this function needs to take in startTime and endTime and find the duration in hours and multiply by cost
                        const startTime = this.startTime;
                        const endTime = this.endTime;

                        const [startHour, startMinute] = startTime.match(/.{1,2}/g);
                        const [endHour, endMinute] = endTime.match(/.{1,2}/g);
                        
                        const startDate = new Date(0, 0, 0, startHour, startMinute);
                        const endDate = new Date(0, 0, 0, endHour, endMinute);
                        
                        const timeDiff = endDate.getTime() - startDate.getTime();
                        const hoursDiff = timeDiff / (1000 * 60 * 60);
                        // console.log(hoursDiff * cost)
                        return hoursDiff * cost;
                        
                    }
                    
                }
            }
        </script>