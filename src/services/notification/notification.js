const amqp = require('amqplib');
const nodemailer = require('nodemailer')

const queueName = 'notification';
const exchangeName = 'fbs';
const routingKey = 'email.notifications'; // the routing key to use when publishing messages
var subject_title = 'confirmation';

//bookerID, coBookerID, bookerAddress, coBookerAddress,roomName, cost, bookingID, date, time, type

function mailer(details) {
    //const link = "fbs.com/?accountID="

    //if it is a cancellation
    if (details.type == "cancel"){
      subject_title = "cancellation"
      var message = `This is to confirm the cancellation of your booking on ${details.date} for ${details.roomName} at ${details.time}. 
Please wait while the credits are being refunded` 
    }

    //for confirmation
    else{
      var cobooker_text = ``

      if (details.coBookerID != null) {
        cobooker_text = `Additionally, as you have indicated a cobooker when booking, please note credits are only deducted evenly after cobooker accepts the request
`
    };

      var message = `This is to inform you that your booking on ${details.date} for ${details.roomName} at ${details.time} has been approved.

${cobooker_text}

Please use this link to see the booking information:
fbs.com`
    }

    //nodemailer transporter
    var transporter = nodemailer.createTransport({
        service: 'hotmail',
        auth: {
          user: 'ESDFBSproj@outlook.com',
          pass: 'ESD1235-6789FBS'
        }
      });
    var mailnames = [
        details.bookerAddress,
        details.coBookerAddress
    ]
      
    var mailOptions = {
    from: "ESDFBSproj@outlook.com",
    to: mailnames,
    subject: `Facility booking for ID:${details.bookingID} ${subject_title}`,
    text: message
    };
    
    transporter.sendMail(mailOptions, function(error, info){
    if (error) {
        console.log(error);
    } else {
        console.log('Email sent: ' + info.response);
        console.log('Message content: '+ message)
    }
    });
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
          const content = message.content.toString();
          try {
            const jsonMessage = JSON.parse(content);
            console.log(jsonMessage)
            //console.log(`Received message: ${jsonMessage}`);
            mailer(jsonMessage)
          } catch (error) {
            console.error(`Error: received non-JSON message: ${content}`);
          }
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