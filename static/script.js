function sendEvent(eventType, x = null, y = null, targetId = "") {
    fetch("/log", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            session_id: SESSION_ID,
            actor_type: ACTOR_TYPE,
            bot_type: BOT_TYPE,
            event_type: eventType,
            target_id: targetId,
            x: x,
            y: y,
            viewport_width: window.innerWidth,
            viewport_height: window.innerHeight,
            timestamp: Date.now()
        })
    });
}

function targetNameFor(element) {
    if (!element) {
        return "";
    }
    return element.dataset.targetId || element.id || element.name || element.tagName.toLowerCase();
}

sendEvent("page_screen_change", null, null, PAGE_NAME);

document.addEventListener("click", function (event) {
    sendEvent("click", event.clientX, event.clientY, targetNameFor(event.target));
});

let lastMove = 0;
document.addEventListener("mousemove", function (event) {
    const now = Date.now();
    if (now - lastMove > 200) {
        sendEvent("mousemove", event.clientX, event.clientY, targetNameFor(event.target));
        lastMove = now;
    }
});

document.addEventListener("scroll", function () {
    sendEvent("scroll", window.scrollY, null, PAGE_NAME);
});

document.addEventListener("keydown", function (event) {
    sendEvent("keydown", null, null, event.target ? targetNameFor(event.target) : event.key);
});

window.addEventListener("focus", function () {
    sendEvent("focus_change", null, null, "window_focus");
});

window.addEventListener("blur", function () {
    sendEvent("focus_change", null, null, "window_blur");
});

document.querySelectorAll("form[data-track-form]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        sendEvent("page_screen_change", null, null, form.dataset.trackForm + "_submit");
        const button = form.querySelector("button[type='submit'], button");
        if (button) {
            button.textContent = "Submitted";
        }
    });
});
