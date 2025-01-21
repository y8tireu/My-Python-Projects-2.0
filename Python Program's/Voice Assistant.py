import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

try:
    with sr.Microphone() as mic:
        engine.say("How can I help you?")
        engine.runAndWait()
        audio = recognizer.listen(mic)
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        engine.say(f"You said {text}")
        engine.runAndWait()
except Exception as e:
    print("Could not process audio:", e)
