const express = require('express');
const fs = require('fs');
const app = express();
const cors = require('cors');
const port = 3000;

// Helper function to read the wine data from the JSON file
function getWineData() {
    const data = fs.readFileSync('./Data/WineData.json');
    return JSON.parse(data);
}

app.use(cors());

// Route to get all wines
app.get('/api/wines', (req, res) => {
    const wines = getWineData();
    res.json(wines);
});

// Route to get wines by store
app.get('/api/wines/:store', (req, res) => {
   const store = req.params.store.toLowerCase();
   const wines = getWineData();
   const filteredWines = wines.filter(wine => wine.Store.toLowerCase() === store);
   res.json(filteredWines);
});

app.listen(port, () => {
    console.log(`Wine API listening at http://localhost:${port}`);
});
