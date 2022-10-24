// server.js
const express = require('express');
// Define Express App
const app = express();
const PORT = process.env.PORT || 80;
const { spawn } = require('child_process');

// Serve Static Assets
app.use(express.static('public'));
app.use(express.static('images'));

const bat = spawn('cmd.exe', ['/c','run.bat']);

app.use(express.static('public'));
app.listen(PORT, () => {
    console.log('Server connected at:', PORT);
});