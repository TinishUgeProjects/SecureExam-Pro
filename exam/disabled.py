import tkinter as tk


def disable_shortcuts(event):
    # Disable right-click
    if event.num == 3:
        show_warning("Right-click is disabled during the exam.")
        return "break"
    # Disable copy shortcut
    elif event.keysym.lower() == "c" and event.state == 4:  # Control key
        show_warning("Copy shortcut is disabled during the exam.")
        return "break"
    # Disable paste shortcut
    elif event.keysym.lower() == "v" and event.state == 4:  # Control key
        show_warning("Paste shortcut is disabled during the exam.")
        return "break"


def start_exam():
    # Disable right-click and copy-paste shortcuts
    root.bind("<Button-3>", disable_shortcuts)  # Disable right-click
    root.bind("<Control-c>", disable_shortcuts)  # Disable copy shortcut
    root.bind("<Control-v>", disable_shortcuts)  # Disable paste shortcut
    # Enable end exam button
    end_button.config(state=tk.NORMAL)


def end_exam():
    # Enable right-click and copy-paste shortcuts
    root.unbind("<Button-3>")
    root.unbind("<Control-c>")
    root.unbind("<Control-v>")
    # Disable end exam button
    end_button.config(state=tk.DISABLED)


def show_warning(message):
    warning_window = tk.Toplevel(root)
    warning_window.title("Warning")
    warning_label = tk.Label(warning_window, text=message)
    warning_label.pack()
    ok_button = tk.Button(warning_window, text="OK", command=warning_window.destroy)
    ok_button.pack()


def enable_end_exam_button():
    # Enable end exam button
    end_button.config(state=tk.NORMAL)


def handle_focus_out(event):
    show_warning(
        "Switching to another window or tab during the exam is not allowed. This warning will only appear once. Further attempts will terminate the exam.")
    root.after(1000, end_exam)  # Automatically terminate the exam after 1 second


# Create GUI window
root = tk.Tk()
root.title("Proctored Quiz")

# Button to start exam
start_button = tk.Button(root, text="Start Exam", command=start_exam)
start_button.pack()

# Button to end exam
end_button = tk.Button(root, text="End Exam", command=end_exam, state=tk.DISABLED)
end_button.pack()

# Bind focus out event
root.bind("<FocusOut>", handle_focus_out)

# Run GUI
root.mainloop()
