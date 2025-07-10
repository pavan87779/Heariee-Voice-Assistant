import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import threading
import os
import sys

# GUI setup
root = tk.Tk()
root.title("🎧 Heariee - Voice Assistant")
root.geometry("650x650")
root.resizable(False, False)

output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=75, height=18, font=("Segoe UI", 10))
output_box.pack(pady=10)

status_label = tk.Label(root, text="Press 'Start Listening' to begin.", fg="blue", font=("Segoe UI", 10, "italic"))
status_label.pack()


# Speak and display
def talk(text):
    output_box.insert(tk.END, f"\n🎧 Heariee: {text}\n")
    output_box.see(tk.END)
    try:
        local_engine = pyttsx3.init('sapi5')  # Fresh engine each time
        local_engine.setProperty('rate', 170)
        voices = local_engine.getProperty('voices')
        local_engine.setProperty('voice', voices[1].id)
        local_engine.say(text)
        local_engine.runAndWait()
    except Exception as e:
        output_box.insert(tk.END, f"\n🔇 Voice Error: {e}\n")


# Listen via mic
def take_command():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            status_label.config(text="🎙️ Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
        command = listener.recognize_google(voice)
        command = command.lower().strip()
        output_box.insert(tk.END, f"\n🗣️ You: {command}")
        return command
    except sr.UnknownValueError:
        talk("Sorry, I didn’t catch that.")
    except sr.RequestError:
        talk("Network issue with Google service.")
    except OSError:
        talk("Microphone not found.")
    return ""


# Main assistant logic
def run_heariee():
    command = take_command()
    status_label.config(text="Processing...")

    if "play" in command:
        song = command.replace("play", "").strip()
        response = f"Playing {song} on YouTube 🎶"
        talk(response)
        pywhatkit.playonyt(song)

    elif "time" in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"It’s {current_time} ⏰")

    elif "pawan babu" in command or "tell about me" in command:
        info = (
            "Pavan Babu is a BTech Computer Science Engineering graduate, seeking entry-level roles in IT 💻. "
            "He is a quick learner with an adaptive nature, able to thrive in any domain with the right training."
        )
        talk(info)
    elif "who is" in command:
        person = command.replace("who is", "").strip()
        try:
            results = wikipedia.search(person)
            if results:
                page_title = results[0]
                summary = wikipedia.summary(page_title, sentences=1, auto_suggest=False, redirect=True)
                talk(summary)
            else:
                talk("I couldn't find any information about that person.")
        except wikipedia.exceptions.DisambiguationError as e:
            talk(f"There are multiple results for {person}. Try saying: who is {e.options[0]}")
        except wikipedia.exceptions.PageError:
            talk("Sorry, I couldn't find a page for that.")
        except Exception as e:
            talk(f"Wikipedia search failed: {e}")






    elif "joke" in command:
        joke = pyjokes.get_joke()
        talk(joke)

    elif "open chrome" in command:
        chrome_path = "C://Program Files//Google//Chrome//Application//chrome.exe"
        if os.path.exists(chrome_path):
            talk("Opening Chrome 🚀")
            os.startfile(chrome_path)
        else:
            talk("Chrome is not installed or path not found 😬")

    elif "open code" in command or "open vs code" in command:
        talk("Opening VS Code 💻")
        os.system("code")

    elif "exit" in command or "stop" in command or "close" in command:
        talk("Okay bro, see you later 👋")
        root.quit()
        sys.exit()

    elif command != "":
        talk("I heard you, but I don’t understand that yet 😅")

    status_label.config(text="Press 'Start Listening' to begin.")


# Use threading to prevent GUI freeze
def threaded_listen():
    thread = threading.Thread(target=run_heariee)
    thread.start()


# Buttons
start_button = tk.Button(root, text="🎤 Start Listening", command=threaded_listen, font=("Segoe UI", 12, "bold"), width=20)
start_button.pack(pady=10)

exit_button = tk.Button(root, text="❌ Exit", command=root.quit, font=("Segoe UI", 12), width=20)
exit_button.pack(pady=5)

# Greet
talk("Yo! I'm Heariee – your personal voice assistant 💡")

# Run app
root.mainloop()
