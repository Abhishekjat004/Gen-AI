// static/script.js
document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const sendButton = document.getElementById("send-button");

    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = (userInput.scrollHeight) + 'px';
    });

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage("user", message);
        userInput.value = "";
        userInput.style.height = 'auto'; // Reset height
        sendButton.disabled = true;

        let botMessageEl = createBotMessageElement();

        try {
            const res = await fetch("/Chatting", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message }),
            });

            if (!res.ok) {
                throw new Error(`Server error: ${res.statusText}`);
            }

            const data = await res.json();

            botMessageEl.innerHTML = DOMPurify.sanitize(marked.parse(data.response));
            addCopyButtons(botMessageEl);

        } catch (err) {
            botMessageEl.innerHTML = `<p style="color: #ff5555;">❌ Error: Failed to connect to backend. Please check the console.</p><p>${err.message}</p>`;
            console.error(err);
        }

        finally {
            sendButton.disabled = false;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    });

    function appendMessage(sender, text) {
        const messageEl = document.createElement("div");
        messageEl.classList.add("chat-message", sender);

        // For user messages, we just set the text content directly
        const contentDiv = document.createElement("div");
        contentDiv.textContent = text;
        messageEl.appendChild(contentDiv);

        chatBox.appendChild(messageEl);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function createBotMessageElement() {
        const messageEl = document.createElement("div");
        messageEl.classList.add("chat-message", "bot");

        const senderEl = document.createElement("div");
        senderEl.classList.add("sender");
        senderEl.textContent = "AI Assistant";

        const contentEl = document.createElement("div");
        contentEl.classList.add("message-content");
        contentEl.innerHTML = '<p>Thinking...</p>';

        messageEl.appendChild(senderEl);
        messageEl.appendChild(contentEl);
        chatBox.appendChild(messageEl);
        chatBox.scrollTop = chatBox.scrollHeight;

        // We return the content element to be updated by the stream
        return contentEl;
    }

    function addCopyButtons(container) {
        const pres = container.querySelectorAll("pre");
        pres.forEach(pre => {
            const button = document.createElement("button");
            button.className = "copy-btn";
            button.textContent = "Copy";
            pre.appendChild(button);

            button.addEventListener("click", () => {
                const code = pre.querySelector("code").innerText;
                navigator.clipboard.writeText(code).then(() => {
                    button.textContent = "Copied!";
                    button.classList.add("copied");
                    setTimeout(() => {
                        button.textContent = "Copy";
                        button.classList.remove("copied");
                    }, 2000);
                });
            });
        });
    }
});
