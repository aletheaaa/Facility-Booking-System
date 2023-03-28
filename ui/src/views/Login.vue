<template>
    <div class="booking-cta">
        <h1 class="display-1 text-light font-weight-bold">SMU <br>Facilities Booking System</h1>
    </div>
    <div id="app">
        <div class="login container bg-light p-5">
            <h1 class="h1 mb-4">Login</h1>
            <form @submit.prevent="login">
                <div class="form-group">
                    <p for="email">Email</p>
                    <input
                    class="form-control"
                    type="text"
                    id="email"
                    v-model="email"
                    placeholder="Enter your email"
                    />
                    
                </div>
                <br />
                <div class="form-group">
                    <p for="password">Password</p>
                    <input
                    class="form-control"
                    type="password"
                    id="password"
                    v-model="password"
                    placeholder="Enter your password"
                    />
                </div>
                <br />
                <button type="submit" class="btn-lg btn-primary">Login</button>
            </form>
        </div>
    </div>
        
    </template>
    
    <script>
    import { login } from '../utils'
    export default {
        name: 'Login',
        data() {
            return {
                email: '',
                password: '',
            }
        },
        methods: {
            login
        },
    }
</script>