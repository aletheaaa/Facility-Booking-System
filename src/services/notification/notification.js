const amqp = require('amqplib');
const nodemailer = require('nodemailer')

const queueName = 'notification';
const exchangeName = 'fbs';
const routingKey = 'email.notifications'; // the routing key to use when publishing messages
var subject_title = 'confirmation';
//HOW TO RUN
//Run the command line: "docker-compose up --build"

//json variables: bookerAddress, coBookerAddress,roomName, cost, bookingID, startTime, endTime, type
//ESDFBSproj is the mail name to send emails
function toSend(details,subject,mailnames,message){ //function to send emails in a round robin fashion due to domains having spam protection after sending multiple mails
  const mailAccounts = [
    {
      service: 'hotmail',
      auth: {
        email: 'ESDFBSproj@outlook.com',
        password: 'ESD1235-6789FBS',
    }},
    {
      service: 'protonmail',
      auth: {
        email: 'ESDFBSproj@proton.me',
        password: 'ESD1235-6789FBS',
    }},
    {
      service: 'tutanota',
      auth: {
        email: 'ESDFBSproj@tutanota.com',
        password: 'ESD1235-6789FBS',
    }},
  ];
  
  // Index of the current mail account to use
  let currentIndex = 0;
  
  // Define the nodemailer transporter outside of the sendMail function
  const transporter = nodemailer.createTransport({
    service: mailAccounts[currentIndex].service,
    auth: {
      user: mailAccounts[currentIndex].auth.email,
      pass: mailAccounts[currentIndex].auth.password,
    },
  });
  
  // Define a function to try sending the email with a different mail account
  function tryNextMailAccount(error, info, mailOptions) {
    if (error) {
      console.log(`Failed to send email with ${mailAccounts[currentIndex].auth.email}: ${error.message}`);
      currentIndex = (currentIndex + 1) % mailAccounts.length;
      console.log(`Trying next mail account: ${mailAccounts[currentIndex].auth.email}`);
      transporter.options.service = mailAccounts[currentIndex].service;
      transporter.options.auth.user = mailAccounts[currentIndex].auth.email;
      transporter.options.auth.pass = mailAccounts[currentIndex].auth.password;
      transporter.sendMail(mailOptions, (err, info) => tryNextMailAccount(err, info, mailOptions));
    } else {
      console.log(`Email sent with ${mailAccounts[currentIndex].auth.email}: ${info.response}`);
      console.log(`Recipients: ${mailnames}`);
      console.log(`Message content: ${message}`);
    }
  }
  
  const mailOptions = {
    from: 'ESDFBSproj@outlook.com',
    to: mailnames,
    subject: `Facility booking for ID:${details.bookingID} ${subject}`,
    text: message,
  };
  
  transporter.sendMail(mailOptions, (error, info) => tryNextMailAccount(error, info, mailOptions));
} 

function mailer(details) {
    var mailnames = [];
    var message = ``

    //to extract the date
    const startDate = new Date(details.startTime);
    const endDate = new Date(details.endTime);
    
    const formattedStartDate = `${startDate.getDate()}/${startDate.getMonth() + 1}/${startDate.getFullYear()}`;
    const formattedEndDate = `${endDate.getDate()}/${endDate.getMonth() + 1}/${endDate.getFullYear()}`;
    
    const date = `${formattedStartDate} - ${formattedEndDate}`;

    //to extract the time
    const start = new Date(details.startTime);
    const end = new Date(details.startTime);

    const formattedStartTime = start.toLocaleTimeString([], {hour: 'numeric', minute: 'numeric', hour12: true});
    const formattedEndTime = end.toLocaleTimeString([], {hour: 'numeric', minute: 'numeric', hour12: true});

    const time = `${formattedStartTime} - ${formattedEndTime}`;

    //check if there is a cobooker
    if (details.coBookerAddress.length > 0){
      mailnames = details.coBookerAddress.concat(details.bookerAddress)
    }
    else{
      mailnames = details.bookerAddress
    }

    //if it is a cancellation
    if (details.type == "cancel"){
      subject_title = "cancellation"
      var message = `This is to inform that there is cancellation of a booking on ${date} for ${details.roomName} at ${time}. 
Any credits deducted for the booking will be refunded shortly` 
      toSend(details,subject_title,mailnames,message)
    }

    //if it is to update cobooker status
    else if(details.type == "update"){
        mailnames = details.bookerAddress
        subject_title = `[Acceptance] Facility booking for ID:${details.bookingID}`
        message = `This is to inform you that ${details.coBookerAddress} has accepted the request for:

BookingID: ${details.bookingID}
Date: ${date} 
Roomname: ${details.roomName}
Date: ${time}

This link provides the booking information:
fbs.com`

        //send to original booker
        toSend(details,subject_title,mailnames,message)
        
        // set variables for cooboker confirmation
        mailnames = details.coBookerAddress
        subject_title = "(cobooker update)"
        message = `This is to inform you that you have accepted a booking (${details.bookingID})

BookingID: ${details.bookingID}
Date: ${date} 
Roomname: ${details.roomName}
Date: ${time}

This link provides the booking information:
fbs.com`

        toSend(details,subject_title,mailnames,message)
    }
        

    //for confirmation
    else{

      //if cobooker indicated
      if (details.coBookerAddress.length > 0) {
        mailnames = details.coBookerAddress
        subject_title = `[CoBooker request] for bookingID ${details.bookingID}`
        message = `This is to inform you that ${details.bookerAddress} has indicated you as a cobooker for:

Booking details:
BookingID: ${details.bookingID}
Date: ${date} 
Roomname: ${details.roomName}
Date: ${time}

Please use this link to accept the booking:
fbs.com`

        toSend(details,subject_title,mailnames,message)
      }
      //mail to primary booker
      subject_title = `Confirmation for bookingID: ${details.bookingID}`
      var message = `This is to inform you that your booking on ${date} for ${details.roomName} at ${time} has been approved.

Please use this link to see the booking information:
fbs.com`

        toSend(details,subject_title,details.bookerAddress,message)
    }
}

async function listen() {
  try {
    const connection = await amqp.connect('amqp://esd-rabbit');
    const channel = await connection.createChannel();

    await channel.assertExchange(exchangeName, 'direct', { durable: true });
    await channel.assertQueue(queueName, { durable: true });
    await channel.bindQueue(queueName, exchangeName, routingKey);
    console.log('Waiting for messages...');

    channel.consume(queueName, (message) => {
        if (message !== null) {
          console.log(message)
          const content = message.content.toString();
          // try {
            const jsonMessage = JSON.parse(content);
            console.log(jsonMessage)
            //console.log(`Received message: ${jsonMessage}`);
            mailer(jsonMessage)
          // } catch (error) {
          //   console.error(`Error: received non-JSON message: ${content}`);
          // }
          channel.ack(message);
        }
      });
  } catch (err) {
    console.error(err);
  }
}

//To create the exchange and queue if it does not exists
async function setup() {
  try {
    const connection = await amqp.connect('amqp://esd-rabbit');
    const channel = await connection.createChannel();

    await channel.assertExchange(exchangeName, 'direct', { durable: true });
    await channel.assertQueue(queueName, { durable: true });
    await channel.bindQueue(queueName, exchangeName, routingKey);
    console.log('Exchange and queue created.');
  } catch (err) {
    console.error(err);
  }
}

setup();
listen();