const PORT = process.env.PORT || 8000;
const express = require('express');

const Wine = require('./Data/WineData.json');

const app = express()


app.get('/',(req,res) =>{
    res.json('welcome to wine api')
})

app.get('/redwine', (req,res) => {
    res.json(Wine)
})


app.listen(PORT, () => console.log(`server is running on PORT ${PORT}`))