/* ================================
   Agora Assistant Embedded Widget
   Advanced Widget Script with Actions
================================ */

(function () {
    const widgetHTML = `
        <button class="agora-widget-button" id="agoraWidgetToggle" aria-label="Open Agora Assistant">
            💬
        </button>

        <div class="agora-widget" id="agoraWidget">
            <div class="agora-widget-header">
                <div class="agora-widget-title">
                    <strong>Agora Assistant</strong>
                    <span>College support chatbot</span>
                </div>

                <div class="agora-widget-status">
                    <span class="agora-status-dot"></span>
                    Online
                </div>
            </div>

            <div class="agora-widget-body" id="agoraWidgetMessages">
                <div class="agora-message bot">
                    Hello! I’m Agora Assistant. I can help you with services, documents, appointments, departments, and portal navigation.
                </div>

                <div class="agora-quick-actions">
                    <button data-question="What services are available?">Services</button>
                    <button data-question="How can I book an appointment?">Appointments</button>
                    <button data-question="What documents can I search?">Documents</button>
                    <button data-question="What departments are available?">Departments</button>
                </div>

                <div class="agora-typing" id="agoraTyping">
                    Agora Assistant is typing<span>...</span>
                </div>
            </div>

            <div class="agora-widget-footer">
                <div class="agora-input-row">
                    <input
                        type="text"
                        id="agoraWidgetInput"
                        placeholder="Ask about this website..."
                        autocomplete="off"
                    >

                    <button id="agoraWidgetSend" aria-label="Send message">
                        ➤
                    </button>
                </div>

                <div class="agora-footer-note">
                    Powered by Agora Assistant
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML("beforeend", widgetHTML);

    const toggleButton = document.getElementById("agoraWidgetToggle");
    const widget = document.getElementById("agoraWidget");
    const messages = document.getElementById("agoraWidgetMessages");
    const input = document.getElementById("agoraWidgetInput");
    const sendButton = document.getElementById("agoraWidgetSend");
    const typing = document.getElementById("agoraTyping");

    function escapeHTML(text) {
        return String(text)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
    }

    function scrollToBottom() {
        messages.scrollTop = messages.scrollHeight;
    }

    function getActionLinks(source, answer, question) {
        const text = `${source} ${answer} ${question}`.toLowerCase();
        const actions = [];

        if (
            text.includes("appointment") ||
            text.includes("advisor") ||
            text.includes("book")
        ) {
            actions.push({
                label: "Open Appointment Page",
                url: "/appointments"
            });

            actions.push({
                label: "View Services Section",
                url: "#services"
            });
        }

        if (
            text.includes("document") ||
            text.includes("course") ||
            text.includes("form") ||
            text.includes("guide")
        ) {
            actions.push({
                label: "Open Document Section",
                url: "#documents"
            });

            actions.push({
                label: "Open Full Documents Page",
                url: "/documents"
            });
        }

        if (
            text.includes("department") ||
            text.includes("computer science") ||
            text.includes("business") ||
            text.includes("design") ||
            text.includes("marketing")
        ) {
            actions.push({
                label: "Open Departments Section",
                url: "#departments"
            });
        }

        if (
            text.includes("service") ||
            text.includes("support") ||
            text.includes("student affairs") ||
            text.includes("registrar")
        ) {
            actions.push({
                label: "Open Services Section",
                url: "#services"
            });
        }

        if (
            text.includes("history") ||
            text.includes("conversation")
        ) {
            actions.push({
                label: "Open Conversation History",
                url: "/history"
            });
        }

        if (
            text.includes("dashboard") ||
            text.includes("profile") ||
            text.includes("portal")
        ) {
            actions.push({
                label: "Go to Portal Home",
                url: "#home"
            });
        }

        const uniqueActions = [];
        const seen = new Set();

        actions.forEach(action => {
            const key = `${action.label}-${action.url}`;

            if (!seen.has(key)) {
                seen.add(key);
                uniqueActions.push(action);
            }
        });

        return uniqueActions.slice(0, 3);
    }

    function handleActionClick(url) {
        if (url.startsWith("#")) {
            const target = document.querySelector(url);

            if (target) {
                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }

            return;
        }

        window.location.href = url;
    }

    function addMessage(text, sender, source = null, actions = []) {
        const message = document.createElement("div");
        message.className = `agora-message ${sender}`;

        let content = escapeHTML(text);

        if (source) {
            content += `<small><strong>Source:</strong> ${escapeHTML(source)}</small>`;
        }

        if (actions.length > 0) {
            content += `<div class="agora-action-list">`;

            actions.forEach(action => {
                content += `
                    <button class="agora-action-link" data-url="${escapeHTML(action.url)}">
                        ${escapeHTML(action.label)}
                    </button>
                `;
            });

            content += `</div>`;
        }

        message.innerHTML = content;

        messages.insertBefore(message, typing);
        scrollToBottom();

        const actionButtons = message.querySelectorAll(".agora-action-link");

        actionButtons.forEach(button => {
            button.addEventListener("click", function () {
                handleActionClick(this.dataset.url);
            });
        });
    }

    function setLoading(isLoading) {
        typing.style.display = isLoading ? "block" : "none";
        sendButton.disabled = isLoading;
        input.disabled = isLoading;
        scrollToBottom();
    }

    async function sendMessage(customQuestion = null) {
        const question = customQuestion || input.value.trim();

        if (!question) {
            return;
        }

        addMessage(question, "user");

        input.value = "";
        setLoading(true);

        try {
            const response = await fetch("/api/widget/message", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: question,
                    source: "embedded_widget"
                })
            });

            const data = await response.json();

            if (!response.ok || data.error) {
                addMessage(
                    data.error || "Sorry, I could not process your message.",
                    "bot",
                    "Widget Error"
                );
            } else {
                const answer = data.answer || "I could not find a response.";
                const source = data.source || "Agora Assistant";
                const actions = getActionLinks(source, answer, question);

                addMessage(
                    answer,
                    "bot",
                    source,
                    actions
                );
            }
        } catch (error) {
            addMessage(
                "Connection error. Please make sure the chatbot server is running.",
                "bot",
                "Connection Error"
            );
        }

        setLoading(false);
        input.focus();
    }

    toggleButton.addEventListener("click", function () {
        if (widget.style.display === "flex") {
            widget.style.display = "none";
        } else {
            widget.style.display = "flex";
            input.focus();
            scrollToBottom();
        }
    });

    sendButton.addEventListener("click", function () {
        sendMessage();
    });

    input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });

    document.querySelectorAll(".agora-quick-actions button").forEach(button => {
        button.addEventListener("click", function () {
            sendMessage(this.dataset.question);
        });
    });
})();