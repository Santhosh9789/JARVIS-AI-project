import speech_recognition as sr

def listen_for_command():
    """
    Listens for a voice command from the user and transcribes it to text.

    Returns:
        str: The transcribed text if successful, None otherwise.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

if __name__ == '__main__':
    command = listen_for_command()
    if command:
        print(f"You said: {command}")
