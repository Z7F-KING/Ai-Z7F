let deepMode = false;

document.getElementById("deep").onclick = () => {
  deepMode = !deepMode;
  alert("تفكير عميق: " + (deepMode ? "مفعل" : "مغلق"));
};

async function send() {
  const input = document.getElementById("input");
  const msg = input.value;
  const model = document.getElementById("model").value;

  addMessage("🧑 " + msg);

  input.value = "";

  const response = await fetch("/api/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      message: msg,
      model: model,
      deep: deepMode
    })
  });

  const data = await response.json();
  addMessage("🤖 " + data.reply);
}

function addMessage(text) {
  const div = document.createElement("div");
  div.innerText = text;
  document.getElementById("messages").appendChild(div);
}
