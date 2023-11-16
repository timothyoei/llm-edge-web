const mongoose = require("mongoose")
mongoose.connect('mongodb+srv://llmedgesd1:nc3*mo29vDBjh*b#u7eS@cluster0.yqzuhfy.mongodb.net/?retryWrites=true&w=majority')  

.then(()=>{
    console.log("mongodb connected")
})
.catch(()=> {
    console.log('failed')
})

const newSchema = new mongoose.Schema({
    email:{
        type:String,
        required:true
    },
    password:{
        type:String,
        required:true
    },
    user:{
        type:String,
        required:true
    }
})

const collection = mongoose.model("collection",newSchema)

module.exports = collection