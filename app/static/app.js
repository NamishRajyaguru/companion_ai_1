const landing = document.getElementById("landing");
const chat = document.getElementById("chat");
const startBtn = document.getElementById("startBtn");

const chatWindow = document.getElementById("chatWindow");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

const emptyState = document.getElementById("emptyState");

const emptyMessages = [
  "What’s new today?",
  "Send a message to start the conversation.",
  "Companion AI is listening 🐾",
];

function showEmptyState() {
  if (chatWindow.children.length === 1) {
    const msg =
      emptyMessages[Math.floor(Math.random() * emptyMessages.length)];
    emptyState.textContent = msg;
    emptyState.style.display = "flex";
  }
}

function hideEmptyState() {
  emptyState.style.display = "none";
}

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    if (window.innerWidth > 768) { // desktop only
      e.preventDefault();
      sendBtn.click();
    }
  }
});

async function loadHistory() {
  const res = await fetch("/history");
  const data = await res.json();

  data.messages.forEach(m => {
    addMessage(
      m.content,
      m.role === "assistant" ? "bot" : "user"
    );
  });
}

startBtn.onclick = () => {
  landing.classList.add("hidden");

  chat.classList.remove("hidden");
  loadHistory();
  // wait one frame so CSS transition can trigger
  requestAnimationFrame(() => {
    chat.classList.add("active");
  });
  showEmptyState();
};


function addMessage(text, sender) {
  const row = document.createElement("div");
  row.className = `message-row ${sender}`;

  const avatar = document.createElement("img");
  avatar.className = "avatar";
  avatar.src =
    sender === "bot"
      ? "/static/assets/bot-logo.png"
      : "/static/assets/user.png";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  hideEmptyState();

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatWindow.appendChild(row);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

sendBtn.onclick = async () => {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  showTyping();

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  });

  const data = await res.json();

  hideTyping();
  addMessage(data.reply, "bot");
};

let typingRow = null;

function showTyping() {
  if (typingRow) return;

  typingRow = document.createElement("div");
  typingRow.className = "message-row bot";

  const avatar = document.createElement("img");
  avatar.className = "avatar";
  avatar.src = "/static/assets/bot-logo.png";

  const bubble = document.createElement("div");
  bubble.className = "bubble typing";

  bubble.innerHTML = `
    <span class="dot"></span>
    <span class="dot"></span>
    <span class="dot"></span>
  `;

  typingRow.appendChild(avatar);
  typingRow.appendChild(bubble);
  chatWindow.appendChild(typingRow);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function hideTyping() {
  if (typingRow) {
    typingRow.remove();
    typingRow = null;
  }
}
