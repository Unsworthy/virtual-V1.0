from flask import Flask, request, jsonify
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os

app = Flask(__name__)

MASTER = "Maxx"

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning " + MASTER)
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon " + MASTER)
    else:
        speak("Good Evening " + MASTER)

@app.route('/process_query', methods=['POST'])
def process_query():
    data = request.get_json()
    query = data['query']

    if query:
        if "wikipedia" in query.lower():
            speak("searching wikipedia....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak(results)
            return jsonify({'message': results})
        elif "open youtube" in query.lower():
            url = "https://youtube.com"
            webbrowser.open(url)
            return jsonify({'message': "Opening YouTube"})
        elif "open google" in query.lower():
            url = "https://google.com"
            webbrowser.open(url)
            return jsonify({'message': "Opening Google"})
        elif "play music" in query.lower():
            music_dir = "D:\\musik"  # Replace with your music directory path
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                return jsonify({'message': "Playing music"})
            else:
                speak("No music files found.")
                return jsonify({'message': "No music files found."})
        elif "the time" in query.lower():
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            return jsonify({'message': f"The time is {strTime}"})
        else:
            speak("I'm not sure how to help with that.")
            return jsonify({'message': "I'm not sure how to help with that."})
    else:
        speak("I didn't catch that. Please try again.")
        return jsonify({'message': "I didn't catch that. Please try again."})

if __name__ == '__main__':
    wishMe()
    app.run(debug=True)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
from flask import send_from_directory

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')
