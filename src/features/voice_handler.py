import speech_recognition as sr
import pyttsx3

# Text-to-Speech Engine

try:
    engine = pyttsx3.init()
except Exception as e:
    print("Warning: Could not initialize pyttsx3 speech engine. Voice output will be disabled.")
    print(f"Error: {e}")
    engine = None

def speak(text):
    """
    Makes A.C.E. speak the given text out loud.
    """
    print(f"\nACE: {text}")

    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error during speech synthesis: {e}")
    else:
        # if engine fails, display a note
        print("Voice out is disabled.")

# The Ears
recognizer = sr.Recognizer()

def listen_for_command():
    """
    Listens for a voice command from the microphone and converts it to text.
    """

    # User system's default microphone
    with sr.Microphone() as source:
        # This function listens for a moment.
        # Improves accuracy
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        # We call our own 'speak' function
        speak("At your service, Boss! What can I do for you?")
        try:
            # Main Listening command. Stops after 5 sec of silence & 10secs of recording
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")

            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")

            return text.lower()
        except sr.WaitTimeoutError:
            # Happens when nothing is said
            speak("I didn't hear. Please repeat")
            return None
        except sr.UnknownValueError:
            # Happens when speech is not recognized
            speak("Sorry Boss, I didn't understand that.")
            return None
        except sr.RequestError as e:
            # Happens when problem with Network or API
            speak(f"Sorry Boss, I couldn't connect to service, {e}")
            return None
