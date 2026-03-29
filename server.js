import express from "express";
import cors from "cors";
import fetch from "node-fetch";

const app = express();
app.use(cors());
app.use(express.json());

const API_KEY = "YOUR_OPENAI_API_KEY"; // حط مفتاح OpenAI هنا

app.post("/chat", async (req,res)=>{
    const userMessage = req.body.message;
    const response = await fetch("https://api.openai.com/v1/chat/completions",{
        method:"POST",
        headers:{
            "Authorization": `Bearer ${API_KEY}`,
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            model:"gpt-4o-mini",
            messages:[{role:"user", content:userMessage}]
        })
    });
    const data = await response.json();
    res.json({reply: data.choices[0].message.content});
});

app.listen(3000,()=>console.log("Server running on port 3000"));
