import openai
import pyttsx3
import speech_recognition as sr

# Initialize the OpenAI API with your API key
openai.api_key = "YOUR_OPENAI_KEY"

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the voice rate and volume
#engine.setProperty('rate', 150)
#engine.setProperty('volume', 0.5)

# Initialize the speech recognizer
r = sr.Recognizer()

# Define a function to get user input from the microphone
def get_input():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""

# Define a function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define a function to generate a response using the OpenAI API
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Define the main function that runs the chatbot
def main():
    speak("Hello, how can I help you?")
    while True:
        user_input = get_input().lower()
        if "exit" in user_input or "stop" in user_input:
            speak("Goodbye!")
            break
        else:
            prompt = "User: " + user_input + "\nBot:"
            response = generate_response(prompt)
            speak(response)

if __name__ == '__main__':
    main()
