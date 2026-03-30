<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body { background:#0f172a; color:white; font-family:Arial; }
#chat { height:75vh; overflow-y:auto; padding:10px; }
.msg { margin:10px; padding:10px; border-radius:10px; }
.user { background:#38bdf8; color:black; text-align:right; }
.ai { background:#1e293b; }

#inputBox {
  position:fixed;
  bottom:0;
  width:100%;
  display:flex;
  gap:5px;
}

input { flex:1; padding:15px; }
button { padding:15px; }

#fileInput { display:none; }
</style>
</head>

<body>

<div id="chat"></div>

<div id="inputBox">
<input id="msg" placeholder="Напиши..." />
<button onclick="send()">➤</button>
<button onclick="uploadClick()">📎</button>
<input type="file" id="fileInput" onchange="uploadFile()" />
</div>

<script>

async function send() {
  let input = document.getElementById("msg");
  let text = input.value.trim();

  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  try {
    let res = await fetch("/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ text: text })
    });

    let data = await res.json();

    console.log(data); // 🔥 покажет ответ в консоли

    addMessage(data.answer ? data.answer : JSON.stringify(data), "ai");

  } catch (err) {
    addMessage("Ошибка соединения", "ai");
  }
}

function addMessage(text, type) {
  let div = document.createElement("div");
  div.className = "msg " + type;
  div.innerText = text;

  let chat = document.getElementById("chat");
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function uploadClick() {
  document.getElementById("fileInput").click();
}

async function uploadFile() {
  let file = document.getElementById("fileInput").files[0];

  let formData = new FormData();
  formData.append("file", file);

  let res = await fetch("/upload", {
    method: "POST",
    body: formData
  });

  let data = await res.json();

  addMessage(data.status || "Файл загружен", "ai");
}

</script>

</body>
</html>
