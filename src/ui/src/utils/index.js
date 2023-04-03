import { getAuth, signInWithEmailAndPassword, GoogleAuthProvider, onAuthStateChanged, signOut } from 'firebase/auth'
import { initializeApp } from 'firebase/app';
import router from '../router/index.js';

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyAs7yJzR2gIxF49JzXQVkVKdw3v_DvzO-s",
    authDomain: "wantest-9f6bf.firebaseapp.com",
    databaseURL: "https://wantest-9f6bf-default-rtdb.firebaseio.com",
    projectId: "wantest-9f6bf",
    storageBucket: "wantest-9f6bf.appspot.com",
    messagingSenderId: "76006540168",
    appId: "1:76006540168:web:fb66edf97a4623b652b03d",
    measurementId: "G-SDMVB049GX"
};


// Initialize Firebase
const app = initializeApp(firebaseConfig);

export const getCurrentUserEmail = () => {
    return new Promise((resolve, reject) => {
        const auth = getAuth();
        const unsubscribe = auth.onAuthStateChanged((user) => {
            if (user) {
                resolve(user.email);
            } else {
                resolve(null);
            }
            unsubscribe();
        });
    });
};

// const auth = getAuth();
export const isLoggedIn = () => {
    onAuthStateChanged(getAuth(), (currentUser) => {
        if (currentUser != null) {
            router.push('/main')
            console.log("Logged in user: " + currentUser)
            return true
        } else {
            router.push('/')
            return false
        }
    })
}

// signing the user out 
export const signout = () => {
    signOut(getAuth())
    .then(() => {
        console.log('Signed Out');
        router.push('/')
    })
    .catch(e => {
        console.error('Sign Out Error', e);
    });
};


export const login = () => {
    console.log("Handling signin")
    var email = document.getElementById('email').value
    var password = document.getElementById('password').value;
    if (email.length < 4) {
        alert('Please enter an email address.');
        return;
    }
    if (password.length < 4) {
        alert('Please enter a password.');
        return;
    }
    // Create user with email and pass.
    signInWithEmailAndPassword(getAuth(), email, password).then(() => {
        console.log("Successfully signed in")
        router.push('/main')
    })
    
    .catch(function (error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        if (errorCode === "auth/wrong-password") {
            alert("Incorrect password!");
        }
        else if (errorCode === "auth/user-not-found") {
            alert("User not found! Please enter a valid email address");
        }
        else {
            alert(errorMessage);
        }
        console.log(error);
    });
}