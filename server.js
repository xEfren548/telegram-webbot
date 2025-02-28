const express = require("express");
const bodyParser = require("body-parser");
const moment = require("moment");
const momentTz = require("moment-timezone");

require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 4005;

// Middleware para parsear el cuerpo de las solicitudes JSON
app.use(bodyParser.json());
app.use(express.static("public"));

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/public/index.html");
})

app.get("/contenido", (req, res) => {
    res.sendFile(__dirname + "/public/contenidoDiario.html");
});

let messages = [];

app.post("/webhook", (req, res) => {
    const { message, date } = req.body;

    messages.push({ text: message, date: date }); // Almacenar el mensaje
    console.log(`Mensaje recibido (${date}): ${message}`);

    res.status(200).send("Mensaje recibido");
});

app.get("/messages", (req, res) => {
    // const today = new Date().toISOString().split("T")[0]; // Obtener la fecha actual (YYYY-MM-DD)
    const today = momentTz().tz("America/Mexico_City").format("YYYY-MM-DD");
    // const todayMessages = messages.filter(msg => msg.date === today); // Filtrar mensajes del día actual

    const todayMessages = messages.filter(msg => {
        const messageDate = msg.date.split(" ")[0]; // Extraer la parte de la fecha (YYYY-MM-DD)
        return messageDate === today;
    });

    res.json(todayMessages); // Enviar los mensajes almacenados
});

// Iniciar el servidor
app.listen(PORT, () => {
    console.log(`Servidor Node.js escuchando en http://localhost:${PORT}`);
});