const inputField = document.getElementById("input");
const chat = document.getElementById("chat");

inputField.addEventListener("keydown", function (event) {
  if (event.key === "Enter" && !event.shiftKey) { 
    event.preventDefault(); 
    send(); 
  }
});

function keepLoaderAtEnd(loader) {
  if (loader.parentNode) loader.remove();
  chat.appendChild(loader);
  chat.scrollTop = chat.scrollHeight;
}

async function send() {
  const input = inputField.value.trim();
  if (!input) return;

  const userMessage = document.createElement("div");
  userMessage.innerHTML = `🧑 <span class="user">You:</span> ${input}\n\n`;
  chat.appendChild(userMessage);
  inputField.value = "";
  chat.scrollTop = chat.scrollHeight;

  const loader = document.createElement("div");
  loader.className = "loader";
  loader.innerHTML = "⏳ AI is typing...";
  keepLoaderAtEnd(loader);

  const aiStream = document.createElement("div");
  aiStream.className = "ai";
  aiStream.innerHTML = `🤖 <span class='ai'>AI:</span><br>`;
  chat.appendChild(aiStream);
  keepLoaderAtEnd(loader);

  try {
    const response = await fetch("http://127.0.0.1:8000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idea: input })
    });

    if (!response.ok) { 
      loader.innerHTML = `⚠️ Server error: ${response.status}`; 
      return; 
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let aiContent = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      chunk.split("\n").forEach(line => {
        if (line.startsWith("data:")) {
          let data = line.replace("data:", "").trim();
          if (data === "[DONE]") {
            displayAI(aiContent, aiStream);
            loader.remove();
          } else {
            data = data
              .replace(/\[market\]/i, "<b>Market Analysis:</b>\n")
              .replace(/\[technical\]/i, "<b>Technical Feasibility:</b>\n")
              .replace(/\[business\]/i, "<b>Business Strategy:</b>\n")
              .replace(/\[recommendation\]/i, "<b>Recommendation:</b>\n");
            aiContent += data + "\n\n";
            aiStream.innerHTML = `🤖 <span class='ai'>AI:</span><br>` + aiContent;
            keepLoaderAtEnd(loader);
          }
        }
      });
    }

  } catch (error) {
    loader.innerHTML = `⚠️ Error: ${error.message}`;
    keepLoaderAtEnd(loader);
  }
}

function clearChat() {
  chat.innerHTML = "";
  inputField.value = "";
}

function displayAI(fullText, aiStream) {
  const sections = fullText.split(/<b>(.*?)<\/b>/).filter(s => s.trim() !== "");
  let html = "";
  for (let i = 0; i < sections.length; i += 2) {
    const title = sections[i].trim();
    const content = sections[i + 1] ? sections[i + 1].trim() : "";

    if (content.length > 200) {
      const truncated = content.slice(0, 200);
      html += `<b>${title}</b>\n${truncated} <span class="show-more" data-full="${encodeURIComponent(content)}">...</span>\n\n`;
    } else {
      html += `<b>${title}</b>\n${content}\n\n`;
    }
  }

  aiStream.innerHTML = `🤖 <span class='ai'>AI:</span><br>` + html;

  aiStream.querySelectorAll(".show-more").forEach(el => {
    el.addEventListener("click", () => {
      const fullContent = decodeURIComponent(el.getAttribute("data-full"));
      const points = fullContent.split(/[\n\.;]+/).filter(p => p.trim() !== "");
      const html = `<ul>${points.map(p => `<li>${p.trim()}</li>`).join("")}</ul>`;
      document.getElementById("modal-content").innerHTML = html;
      document.getElementById("modal").style.display = "flex";
    });
  });
}

document.getElementById("modal-close").addEventListener("click", () => {
  document.getElementById("modal").style.display = "none";
});
