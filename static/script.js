async function sendMessage() {
    const input = document.getElementById("input");
    const msg = input.value;

    if (!msg) return;

    const messages = document.getElementById("messages");

    // Show user message
    messages.innerHTML += `<div class="message user">${msg}</div>`;

    input.value = "";

    // Loading
    messages.innerHTML += `<div class="message bot" id="loading" style="color: #a3a3a3; font-style: italic;">Assistant is thinking...</div>`;

    const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: msg})
    });

    const data = await res.json();

    // Remove loading
    document.getElementById("loading").remove();

    // Show response
    messages.innerHTML += `<div class="message bot">${data.response.replace(/\n/g, "<br>")}</div>`;

    messages.scrollTop = messages.scrollHeight;
}