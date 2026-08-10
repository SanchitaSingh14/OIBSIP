import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser


# Initialize speech engine
engine = pyttsx3.init()

# Initialize speech recognizer
recognizer = sr.Recognizer()


# Function to speak
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# Function to listen
def listen():
    with sr.Microphone() as source:
        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text.lower()

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand you.")
        return ""

    except sr.RequestError:
        print("Could not connect to the speech recognition service.")
        return ""

# Start the assistant
speak("Hello! I am your voice assistant. How can I help you?")


while True:

    command = listen()

    if "hello" in command:
        speak("Hello! Nice to meet you. How can I help you?")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The current time is " + current_time)

    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        speak("Today's date is " + current_date)

    elif command.startswith("search"):
        search_query = command.replace("search", "", 1).strip()

        if search_query:
            speak("Searching for " + search_query)

            webbrowser.open(
                "https://www.google.com/search?q="
                + search_query.replace(" ", "+")
            )

        else:
            speak("Please tell me what you want me to search for.")

    elif "exit" in command or "quit" in command or "goodbye" in command:
        speak("Goodbye! Have a great day.")
        break

    elif command:
        speak("Sorry, I don't know that command yet.")

    else:
        speak("Sorry, I didn't understand. Please repeat.")