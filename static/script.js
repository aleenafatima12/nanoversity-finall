function showDescription(courseId) {
    fetch(`/course/${courseId}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('popup-title').innerText = data.title;
        document.getElementById('popup-description').innerText = data.description;
        document.getElementById('popup-modal').style.display = 'block';
    });
}

function closeModal() {
    document.getElementById('popup-modal').style.display = 'none';
}
document.getElementById("chatbot-toggle").addEventListener("click", function () {
    const container = document.getElementById("chatbot-container");
    container.style.display = (container.style.display === "block") ? "none" : "block";
});

document.getElementById("chatbot-input").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        const input = e.target.value;
        const messages = document.getElementById("chatbot-messages");
        messages.innerHTML += `<div class="user-msg">${input}</div>`;
        fetch("/chatbot", {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: input})
        })
        .then(res => res.json())
        .then(data => {
            messages.innerHTML += `<div class="bot-msg">${data.response}</div>`;
            e.target.value = "";
            messages.scrollTop = messages.scrollHeight;
        });
    }
});
