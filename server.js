import express from "express";
import fetch from "node-fetch";

const app = express();
app.use(express.json());
app.use(express.static("public"));

const API_KEY = "PUT_YOUR_KEY_HERE";

app.post("/api/chat", async (req, res) => {
  const { message, model, deep } = req.body;

  const systemPrompt = deep
    ? "أجب بشكل عميق وتحليل مفصل"
    : "أجب بشكل مختصر";

  const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: model,
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: message }
      ]
    })
  });

  const data = await response.json();

  res.json({
    reply: data.choices[0].message.content
  });
});

app.listen(3000, () => console.log("Server running"));
