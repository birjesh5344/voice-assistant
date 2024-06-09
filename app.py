import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import smtplib
import requests
import nltk
from nltk.tokenize import word_tokenize
from flask import Flask, render_template

# Download necessary NLTK data1
nltk.download('punkt')

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

app = Flask(__name__)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""

def interpret_command(command):
    tokens = word_tokenize(command)
    if "email" in tokens:
        send_email()
    elif "weather" in tokens:
        get_weather()
    elif "time" in command:
        tell_time()
    elif "date" in command:
        tell_date()
    elif "search for" in command:
        search_web(command)
    else:
        custom_command(command)

def tell_time():
    current_time = datetime.datetime.now().strftime("%H:%M")
    speak(f"The current time is {current_time}")

def tell_date():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today's date is {current_date}")

def search_web(command):
    search_query = command.replace("search for", "")
    url = f"https://www.google.com/search?q={search_query}"
    webbrowser.open(url)
    speak(f"Searching for {search_query}")

def send_email():
    # Configure your email server and credentials
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("youremail@gmail.com", "yourpassword")
    message = "This is a test email from your voice assistant."
    server.sendmail("youremail@gmail.com", "recipientemail@gmail.com", message)
    server.quit()
    speak("Email has been sent.")

def get_weather():
    api_key = "your_openweathermap_api_key"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "your_city"
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        speak(f"The temperature is {temperature - 273.15:.2f} degrees Celsius.")
    else:
        speak("City not found.")

user_commands = {
    "open google": "webbrowser.open('http://www.google.com')",
    "play music": "webbrowser.open('http://www.spotify.com')"
}

def custom_command(command):
    if command in user_commands:
        exec(user_commands[command])
        speak(f"Executing {command}")
    else:
        speak("Command not found.")

@app.route('/')
def index():
    return render_template('index.html')

def main():
    while True:
        command = listen()
        if command:
            interpret_command(command)

if __name__ == "__main__":
    from threading import Thread
    Thread(target=main).start()
    app.run(debug=True)
