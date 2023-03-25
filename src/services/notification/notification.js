const amqp = require('amqplib');
const nodemailer = require('nodemailer')

const queueName = 'notification';
const exchangeName = 'fbs';
const routingKey = 'email.notifications'; // the routing key to use when publishing messages


function mailer(details) {
    const link = 'https://fbs.intranet.smu.edu.sg/home'
    var cobooker_text = ``

    if (details.cobooker != null) {
        cobooker_text = `You have indicated a cobooker when booking, ${details.cobooker} please click on the following link to accept the booking:
${link}`
    };

    var message = `This is to inform you that your booking on ${details.date} for ${details.room} at ${details.time} has been approved. 
${cobooker_text}
Click this link for more information:
${link}`

    var transporter = nodemailer.createTransport({
        service: 'hotmail',
        auth: {
          user: 'ESDFBSproj@outlook.com',
          pass: 'ESD1235-6789FBS'
        }
      });
    var mailnames = [
        details.name,
        details.cobooker
    ]
      
    var mailOptions = {
    from: "ESDFBSproj@outlook.com",
    to: mailnames,
    subject: `Facility booking for ID:${details.bookingid} confirmed`,
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
