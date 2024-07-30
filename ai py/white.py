import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import requests
from bs4 import BeautifulSoup

print("Memulai White")

MASTER = "Maxx"
LANGUAGE = "en"  # Default language is English

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)

# fungsi berbicara
def speak(text):
    engine.say(text)
    engine.runAndWait()

# sapa kepada user
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if LANGUAGE == "en":
        if hour >= 0 and hour < 12:
            speak("Good Morning " + MASTER)
        elif hour >= 12 and hour < 18:
            speak("Good Afternoon " + MASTER)
        else:
            speak("Good Evening " + MASTER)
    else:
        if hour >= 0 and hour < 12:
            speak("Selamat Pagi " + MASTER)
        elif hour >= 12 and hour < 18:
            speak("Selamat Siang " + MASTER)
        else:
            speak("Selamat Malam " + MASTER)

# mengambil suara user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Mendengarkan..." if LANGUAGE == "id" else "Listening...")
        r.adjust_for_ambient_noise(source)  # Sesuaikan dengan kebisingan sekitar
        audio = r.listen(source)

        try:
            print("Mengenali..." if LANGUAGE == "id" else "Recognizing...")
            query = r.recognize_google(audio, language="id-ID" if LANGUAGE == "id" else "en-US")
            print(f"User mengatakan: {query}\n" if LANGUAGE == "id" else f"User said: {query}\n")
            return query
        except sr.UnknownValueError:
            print("Maaf, saya tidak mengerti itu. Bisakah Anda mengulanginya?" if LANGUAGE == "id" else "Sorry, I did not understand that. Could you please repeat?")
            speak("Maaf, saya tidak mengerti itu. Bisakah Anda mengulanginya?" if LANGUAGE == "id" else "Sorry, I did not understand that. Could you please repeat?")
            return None
        except sr.RequestError:
            print("Maaf, layanan suara saya sedang down" if LANGUAGE == "id" else "Sorry, my speech service is down")
            speak("Maaf, layanan suara saya sedang down" if LANGUAGE == "id" else "Sorry, my speech service is down")
            return None

def search_google(question):
    try:
        query = question.replace(" ", "+")
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Get the first result from Google
        answer = soup.find("div", class_="BNeawe").text
        return answer
    except Exception as e:
        print(f"Error searching Google: {e}")
        speak("Maaf, terjadi kesalahan dalam mencari jawaban di Google." if LANGUAGE == "id" else "Sorry, there was an error searching for an answer on Google.")
        return None

# script penyapaan
speak("Halo, nama saya White, apa yang bisa saya bantu?" if LANGUAGE == "id" else "Hello, my name is White, how can I help you?")
wishMe()

while True:
    query = takeCommand()
    
    if query:
        if "indo pride" in query.lower():
            LANGUAGE = "id"
            speak("Bahasa telah diubah ke Indonesia.")
            continue
        elif "change language to english" in query.lower():
            LANGUAGE = "en"
            speak("Language has been changed to English.")
            continue
        
        if "wikipedia" in query.lower():
            speak("mencari di wikipedia...." if LANGUAGE == "id" else "searching wikipedia....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2, auto_suggest=False)
            print(results)
            speak(results)
        elif "buka youtube" in query.lower() or "open youtube" in query.lower():
            url = "https://youtube.com"
            webbrowser.open(url)
        elif "buka google" in query.lower() or "open google" in query.lower():
            url = "https://google.com"
            webbrowser.open(url)
        elif "buka spotify" in query.lower() or "open spotify" in query.lower():
            url = "https://spotify.com"
            webbrowser.open(url)
        elif "putar musik" in query.lower() or "play music" in query.lower():
            music_dir = "D:\\musik"  # Ganti dengan path direktori musik Anda
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("Tidak ada file musik yang ditemukan." if LANGUAGE == "id" else "No music files found.")
        elif "jam berapa" in query.lower() or "the time" in query.lower():
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sekarang jam {strTime}" if LANGUAGE == "id" else f"Sir, the time is {strTime}")
        elif "question" in query.lower():
            answer = search_google(query)
            if answer:
                speak(answer)
            else:
                speak("Saya tidak yakin bagaimana membantu dengan itu. Silakan coba lagi." if LANGUAGE == "id" else "I'm not sure how to help with that. Please try again.")
    else:
        continue

    break
