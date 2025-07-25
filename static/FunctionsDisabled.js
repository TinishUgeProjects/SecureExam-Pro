// JavaScript code to disable shortcuts during exam

// Function to disable shortcuts
function disableShortcuts(event) {
    // Disable right-click
    if (event.button === 2) {
        showWarning("Right-click is disabled during the exam.");
        return false;
    }
    // Disable copy shortcut
    else if (event.key.toLowerCase() === "c" && event.ctrlKey) {
        showWarning("Copy shortcut is disabled during the exam.");
        return false;
    }
    // Disable paste shortcut
    else if (event.key.toLowerCase() === "v" && event.ctrlKey) {
        showWarning("Paste shortcut is disabled during the exam.");
        return false;
    }
}

// Function to show warning message
function showWarning(message) {
    alert(message);
}

// Function to start exam
function startExam() {
    // Add event listeners to disable shortcuts
    document.addEventListener("contextmenu", disableShortcuts); // Disable right-click
    document.addEventListener("keydown", disableShortcuts); // Disable copy and paste shortcuts

    // Enable end exam button
    enableEndExamButton();
}

// Function to end exam
function endExam() {
    // Remove event listeners to enable shortcuts
    document.removeEventListener("contextmenu", disableShortcuts);
    document.removeEventListener("keydown", disableShortcuts);

    // Disable end exam button
    disableEndExamButton();
}

// Function to enable end exam button
function enableEndExamButton() {
    var endButton = document.getElementById("end-exam-button");
    if (endButton) {
        endButton.disabled = false;
    }
}

// Function to disable end exam button
function disableEndExamButton() {
    var endButton = document.getElementById("end-exam-button");
    if (endButton) {
        endButton.disabled = true;
    }
}

// Function to handle focus out event
function handleFocusOut(event) {
    showWarning("Switching to another window or tab during the exam is not allowed. This warning will only appear once. Further attempts will terminate the exam.");
    setTimeout(endExam, 1000); // Automatically terminate the exam after 1 second
}
