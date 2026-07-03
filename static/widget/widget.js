/* ================================
   Agora Assistant Embedded Widget
   Updated Widget Script with:
   - Backend action_label/action_url support
   - Dynamic action buttons from chatbot API
   - Safe fallback action detection
   - Visible close button
   - Fixed service/section links
   - Accessibility label updates
   - Chatbot reopen after navigation
================================ */

(function () {
    const WIDGET_REOPEN_KEY = "agoraWidgetReopenAfterNavigation";

    const widgetHTML = `
        <button
            class="agora-widget-button"
            id="agoraWidgetToggle"
            aria-label="Open Agora Assistant"
            aria-expanded="false"
            aria-controls="agoraWidget"
        >
            💬
        </button>

        <div
            class="agora-widget"
            id="agoraWidget"
            role="dialog"
            aria-hidden="true"
            aria-labelledby="agoraWidgetTitle"
        >
            <div class="agora-widget-header">
                <div class="agora-widget-title">
                    <strong id="agoraWidgetTitle">Agora Assistant</strong>
                    <span>College support chatbot</span>
                </div>

                <div class="agora-widget-header-actions">
                    <div class="agora-widget-status">
                        <span class="agora-status-dot"></span>
                        Online
                    </div>

                    <button
                        type="button"
                        class="agora-widget-close"
                        id="agoraWidgetClose"
                        aria-label="Close Agora Assistant"
                    >
                        ×
                    </button>
                </div>
            </div>

            <div class="agora-widget-body" id="agoraWidgetMessages">
                <div class="agora-message bot">
                    Hello! I’m Agora Assistant. I can help you with services, documents, appointments, departments, and portal navigation.
                </div>

                <div class="agora-quick-actions" id="agoraInitialQuickActions">
                    <button data-question="What services are available?">Services</button>
                    <button data-question="How can I book an appointment?">Appointments</button>
                    <button data-question="Show my appointments">My Appointments</button>
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
    const closeButton = document.getElementById("agoraWidgetClose");
    const widget = document.getElementById("agoraWidget");
    const messages = document.getElementById("agoraWidgetMessages");
    const input = document.getElementById("agoraWidgetInput");
    const sendButton = document.getElementById("agoraWidgetSend");
    const typing = document.getElementById("agoraTyping");
    const initialQuickActions = document.getElementById("agoraInitialQuickActions");

    function escapeHTML(text) {
        return String(text || "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");
    }

    function formatMessageText(text) {
        return escapeHTML(text).replace(/\n/g, "<br>");
    }

    function scrollToBottom() {
        messages.scrollTop = messages.scrollHeight;
    }

    function openWidget(focusInput = true) {
        widget.style.display = "flex";
        widget.classList.add("is-open");
        widget.setAttribute("aria-hidden", "false");

        toggleButton.setAttribute("aria-label", "Close Agora Assistant");
        toggleButton.setAttribute("aria-expanded", "true");
        toggleButton.textContent = "×";

        if (focusInput) {
            setTimeout(function () {
                input.focus();
            }, 100);
        }

        scrollToBottom();
    }

    function closeWidget() {
        widget.style.display = "none";
        widget.classList.remove("is-open");
        widget.setAttribute("aria-hidden", "true");

        toggleButton.setAttribute("aria-label", "Open Agora Assistant");
        toggleButton.setAttribute("aria-expanded", "false");
        toggleButton.textContent = "💬";
    }

    function toggleWidget() {
        if (widget.style.display === "flex") {
            closeWidget();
        } else {
            openWidget(true);
        }
    }

    function removeInitialQuickActions() {
        if (initialQuickActions) {
            initialQuickActions.remove();
        }
    }

    function isSafeActionUrl(url) {
        if (!url) {
            return false;
        }

        const cleanedUrl = String(url).trim();

        return (
            cleanedUrl.startsWith("/") ||
            cleanedUrl.startsWith("https://") ||
            cleanedUrl.startsWith("http://")
        );
    }

    function normalizeAction(label, url) {
        if (!label || !url) {
            return null;
        }

        const cleanLabel = String(label).trim();
        const cleanUrl = String(url).trim();

        if (!cleanLabel || !cleanUrl) {
            return null;
        }

        if (!isSafeActionUrl(cleanUrl)) {
            return null;
        }

        return {
            label: cleanLabel,
            url: cleanUrl
        };
    }

    function addUniqueAction(actions, seen, label, url) {
        const action = normalizeAction(label, url);

        if (!action) {
            return;
        }

        const key = `${action.label}-${action.url}`;

        if (!seen.has(key)) {
            seen.add(key);
            actions.push(action);
        }
    }

    function getFallbackActionLinks(source, answer, question) {
        const primaryText = `${question || ""} ${source || ""}`.toLowerCase();
        const secondaryText = `${answer || ""}`.toLowerCase();

        const actions = [];
        const seen = new Set();

        const hasAppointmentIntent =
            primaryText.includes("appointment") ||
            primaryText.includes("advisor") ||
            primaryText.includes("book") ||
            primaryText.includes("schedule meeting") ||
            primaryText.includes("meeting") ||
            primaryText.includes("counsellor") ||
            primaryText.includes("counselor");

        const hasDocumentIntent =
            primaryText.includes("document") ||
            primaryText.includes("pdf") ||
            primaryText.includes("form") ||
            primaryText.includes("guide") ||
            primaryText.includes("course") ||
            primaryText.includes("policy") ||
            primaryText.includes("registration");

        const hasDepartmentIntent =
            primaryText.includes("department") ||
            primaryText.includes("computer science") ||
            primaryText.includes("business") ||
            primaryText.includes("design") ||
            primaryText.includes("marketing") ||
            primaryText.includes("program");

        const hasServiceIntent =
            primaryText.includes("service") ||
            primaryText.includes("support") ||
            primaryText.includes("student affairs") ||
            primaryText.includes("registrar") ||
            primaryText.includes("help desk") ||
            primaryText.includes("library");

        const hasHistoryIntent =
            primaryText.includes("history") ||
            primaryText.includes("conversation") ||
            primaryText.includes("previous chat");

        const hasDashboardIntent =
            primaryText.includes("dashboard");

        const hasPortalIntent =
            primaryText.includes("portal") ||
            primaryText.includes("home") ||
            primaryText.includes("website");

        if (hasAppointmentIntent) {
            addUniqueAction(actions, seen, "Open Appointment Page", "/appointments");
        }

        if (hasDocumentIntent) {
            addUniqueAction(actions, seen, "Open Document Center", "/documents");
            addUniqueAction(actions, seen, "View Documents Section", "/demo-site#documents");
        }

        if (hasDepartmentIntent) {
            addUniqueAction(actions, seen, "View Departments Section", "/demo-site#departments");
        }

        if (hasServiceIntent) {
            addUniqueAction(actions, seen, "View Services Section", "/demo-site#services");
        }

        if (hasHistoryIntent) {
            addUniqueAction(actions, seen, "Open Conversation History", "/history");
        }

        if (hasDashboardIntent) {
            addUniqueAction(actions, seen, "Open Dashboard", "/dashboard");
        }

        if (hasPortalIntent) {
            addUniqueAction(actions, seen, "Go to Portal Home", "/demo-site");
        }

        /*
          Secondary check:
          Only use answer text if no direct intent was detected from question/source.
          This prevents the chatbot from showing the same options every time.
        */
        if (actions.length === 0) {
            if (
                secondaryText.includes("appointment") ||
                secondaryText.includes("advisor") ||
                secondaryText.includes("book")
            ) {
                addUniqueAction(actions, seen, "Open Appointment Page", "/appointments");
            } else if (
                secondaryText.includes("document") ||
                secondaryText.includes("pdf") ||
                secondaryText.includes("form") ||
                secondaryText.includes("guide")
            ) {
                addUniqueAction(actions, seen, "Open Document Center", "/documents");
            } else if (
                secondaryText.includes("department")
            ) {
                addUniqueAction(actions, seen, "View Departments Section", "/demo-site#departments");
            } else if (
                secondaryText.includes("service") ||
                secondaryText.includes("support")
            ) {
                addUniqueAction(actions, seen, "View Services Section", "/demo-site#services");
            } else if (
                secondaryText.includes("history") ||
                secondaryText.includes("conversation")
            ) {
                addUniqueAction(actions, seen, "Open Conversation History", "/history");
            }
        }

        return actions;
    }

    function buildActionsFromResponse(data, question) {
        const actions = [];
        const seen = new Set();

        /*
          Main update:
          Use backend-provided action first.
          This action comes from chatbot_service.py and MongoDB website content records.
        */
        addUniqueAction(
            actions,
            seen,
            data.action_label || "",
            data.action_url || ""
        );

        /*
          Fallback:
          If backend action is missing or if text strongly indicates another useful page,
          add safe backup actions.
        */
        const fallbackActions = getFallbackActionLinks(
            data.source || "",
            data.answer || "",
            question || ""
        );

        fallbackActions.forEach(action => {
            addUniqueAction(
                actions,
                seen,
                action.label,
                action.url
            );
        });

        /*
          Last fallback for unclear/general questions.
        */
        if (actions.length === 0) {
            addUniqueAction(actions, seen, "Go to Portal Home", "/demo-site");
            addUniqueAction(actions, seen, "Search Documents", "/documents");
        }

        return actions.slice(0, 3);
    }

    function scrollToSection(hash) {
        const target = document.querySelector(hash);

        if (target) {
            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

            return true;
        }

        return false;
    }

    function handleActionClick(url) {
        if (!isSafeActionUrl(url)) {
            return;
        }

        /*
          Keep chatbot open after page navigation.
          This fixes the issue where the chatbot collapses after clicking an action.
        */
        sessionStorage.setItem(WIDGET_REOPEN_KEY, "true");

        const cleanedUrl = String(url).trim();

        if (cleanedUrl.startsWith("#")) {
            scrollToSection(cleanedUrl);
            openWidget(false);
            return;
        }

        if (cleanedUrl.startsWith("http://") || cleanedUrl.startsWith("https://")) {
            window.open(cleanedUrl, "_blank", "noopener,noreferrer");
            return;
        }

        const targetUrl = new URL(cleanedUrl, window.location.origin);
        const currentPath = window.location.pathname;
        const samePath = targetUrl.pathname === currentPath;

        if (samePath && targetUrl.hash) {
            scrollToSection(targetUrl.hash);
            openWidget(false);
            return;
        }

        window.location.href = targetUrl.pathname + targetUrl.hash;
    }

    function addMessage(text, sender, source = null, actions = []) {
        const message = document.createElement("div");
        message.className = `agora-message ${sender}`;

        let content = `<div class="agora-message-text">${formatMessageText(text)}</div>`;

        if (source) {
            content += `
                <small class="agora-message-source">
                    <strong>Source:</strong> ${escapeHTML(source)}
                </small>
            `;
        }

        if (actions.length > 0) {
            content += `<div class="agora-action-list">`;

            actions.forEach(action => {
                content += `
                    <button
                        type="button"
                        class="agora-action-link"
                        data-url="${escapeHTML(action.url)}"
                    >
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

        removeInitialQuickActions();

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
                    message: question,
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
                const actions = buildActionsFromResponse(data, question);

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

    function reopenWidgetIfNeeded() {
        const shouldReopen = sessionStorage.getItem(WIDGET_REOPEN_KEY);

        if (shouldReopen === "true") {
            sessionStorage.removeItem(WIDGET_REOPEN_KEY);

            setTimeout(function () {
                openWidget(false);
            }, 300);
        }
    }

    toggleButton.addEventListener("click", toggleWidget);

    closeButton.addEventListener("click", function () {
        closeWidget();
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

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && widget.style.display === "flex") {
            closeWidget();
        }
    });

    closeWidget();
    reopenWidgetIfNeeded();
})();