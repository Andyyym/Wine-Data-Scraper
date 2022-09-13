const PORT = process.env.PORT || 8000;
const express = require('express');

const Wine = require('./Data/RedWine.json');
const WoolWorths = require('./Data/Woolworths.json');
const PicknPay = require('./Data/PicknPay.json');
const Makro = require('./Data/Makro.json');

const app = express()


app.get('/',(req,res) =>{
    res.json('welcome to wine api')
})

app.get('/store/', (req,res) => {
    res.json(Wine)
})

app.get('/store/woolworths', (req,res) => {
    res.json(WoolWorths)
})

app.get('/store/picknpay', (req,res) => {
    res.json(PicknPay)
})

app.get('/store/makro', (req,res) => {
    res.json(Makro)
})

app.listen(PORT, () => console.log(`server is running on PORT ${PORT}`))