import pyttsx3

def speak(text: str):
    """
    Uses text-to-speech to say the given text.
    Falls back to printing if TTS fails at any stage.

    Args:
        text (str): The text to be spoken.
    """
    try:
        engine = pyttsx3.init()
        if engine is None: # Check if initialization returned None
            raise RuntimeError("pyttsx3.init() returned None")

        # Attempt to set properties that might help in restricted environments
        # This is speculative and might not have an effect.
        engine.setProperty('driverName', 'dummy') # Try dummy driver if available

        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")
        print(f"Fallback TTS (saying): {text}")

if __name__ == '__main__':
    print("Testing voice output...")
    speak("Hello, this is a test of the text to speech system.")
    speak("If you hear this, it is working.")
    speak("Testing with an empty string.")
    speak("")
    speak("Another test after potential errors.")
    print("Test complete.")
