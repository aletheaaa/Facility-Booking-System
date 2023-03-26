const amqp = require('amqplib');

const exchangeName = 'fbs';
const routingKey = 'email.notifications';
//{ bookerID, coBookerID, bookerAddress, coBookerAddress,roomName, cost, bookingID, date, time, type}
const message = {
    "bookerAddress":"joeltan.2021@scis.smu.edu.sg",
    "coBookerAddress":"alethea.toh.2021@scis.smu.edu.sg",
    "bookerID":1,
    "coBookerID":2,
    "type":"create",
    "bookingID":"57639218",
    "time":"1100 - 1200",
    "roomName":"SOE/SCIS2 Seminar Rm 3-3",
    "date":"15/03/23"
};

//To publish messages to the queue
async function publishMessage() {
  try {
    const connection = await amqp.connect('amqp://localhost');
    const channel = await connection.createChannel();
    await channel.assertExchange(exchangeName, 'direct', { durable: true });
    const messageString = JSON.stringify(message);
    channel.publish(exchangeName, routingKey, Buffer.from(messageString));
    console.log(`Message sent to exchange ${exchangeName} with routing key ${routingKey}`);
    console.log(typeof(messageString)+"//"+messageString)
    await channel.close();
    await connection.close();
  } catch (error) {
    console.error(error);
  }
}

publishMessage();
