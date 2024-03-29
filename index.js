// server.js
const express = require('express');
// Define Express App
const app = express();
const PORT = process.env.PORT || 80;

// Serve Static Assets
app.use(express.static('public'));
app.use(express.static('images'));

app.use(express.static('public'));
app.listen(PORT, () => {
    console.log(`Server connected at: ${PORT}`);
});