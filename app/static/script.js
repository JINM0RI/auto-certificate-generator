// ---------- AUTO UPLOAD: SHEET ----------
document.getElementById("sheetFile").addEventListener("change", async () => {
    const file = document.getElementById("sheetFile").files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/upload-sheet", {
        method: "POST",
        body: formData
    });

    const data = await res.json();
    alert(`Sheet uploaded. Participants: ${data.count}`);
});


// ---------- AUTO UPLOAD: TEMPLATE ----------
document.getElementById("templateFile").addEventListener("change", async () => {
    const file = document.getElementById("templateFile").files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/upload-template", {
        method: "POST",
        body: formData
    });

    const data = await res.json();
    alert("Template uploaded");

    // Enable position editor button once template exists
    document.getElementById("openEditorBtn").disabled = false;
});


// ---------- OPEN POSITION EDITOR ----------
function openPositionEditor() {
    window.open(
        "/static/position_control.html?v=" + Date.now(),
        "_blank",
        "width=1100,height=800"
    );
}


// ---------- GENERATE CERTIFICATES ----------
async function generateCertificates() {
    const templateInput = document.getElementById("templateFile");
    if (!templateInput.files.length) {
        alert("Upload a template first");
        return;
    }

    const templateName = templateInput.files[0].name;

    await fetch(`/generate-certificates?template_name=${templateName}`, {
        method: "POST"
    });

    alert("Certificates generated");
}


// ---------- SEND EMAILS ----------

async function sendEmails() {
    const subject = document.getElementById("subject").value;
    const body = document.getElementById("body").value;

    const res = await fetch("/send-emails", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ subject, body })
    });

    const data = await res.json();

    if (!res.ok) {
        alert("Email sending failed: " + data.error);
        return;
    }

    
    await fetch("/reset", {
        method: "POST"
    });

    alert("Emails sent & system reset");

    // Optional UI cleanup
    document.getElementById("sheetFile").value = "";
    document.getElementById("templateFile").value = "";
    document.getElementById("subject").value = "";
    document.getElementById("body").value = "";
}

