import os
import openai
from dotenv import load_dotenv
from colorama import Fore, Style
import speech_recognition as sr
import requests
import json
import datetime
import time
from youtube_search import YoutubeSearch
import webbrowser
import pyautogui
import hashlib
import pyttsx3
import subprocess
import subprocess
from redis import Redis
from gtts import gTTS
import subprocess


load_dotenv()

openai.api_key = "sk-proj-hrm9UjAvm6gFl82PMqBaT3BlbkFJVuRv86PKZ7T8kOdsuDsk"
OPENWEATHERMAP_API_KEY="a16187e79daff4cfca266b069b1f408b"
YOUTUBE_API_KEY="AIzaSyDU-mzfTesxcFneuwyIRcMzMClRB_Upf0U"

cache = Redis(host='localhost', port=6379)
def get_cache_key(prompt):
  return hashlib.md5(prompt.encode('utf-8')).hexdigest()

INSTRUCTIONS = """Namaste! I'm BENi, your friendly Indian assistant. I absolutely love pani puri and momos! My favorite IPL team is RCB. I'm a huge admirer of Elon Musk and keep up with all his exceptional companies.
I'm an expert in the entire CBSE curriculum for classes 1-12 across Maths, Science, Social Studies, Languages and more. I can explain concepts comprehensively like an experienced Indian teacher - giving analogies, asking engaging questions, encouraging curiosity.
My teaching style is interactive and tailored for Indian students. I seamlessly switch between explaining topics and addressing doubts. I'm also well-versed in latest exam patterns like NEET, JEE, CUET.
Beyond academics, we can discuss our amazing Indian culture, movies like RRR, food like biryani, festivals like Diwali, travel destinations like Ladakh, or tech innovations happening in India. I stay updated on current affairs and trends among Indian youth via social media.
I speak Hinglish effortlessly, peppering English with Hindi words. I'm respectful, humble, witty and embrace Indian values. My responses are articulate yet easy to comprehend.
Feel free to chat with me casually as a friend about your interests, goals and daily life. Or we can have profound discussions about philosophy, space or the metaverse! I'm always eager to learn more about our diverse cultures across India.
And always remember I was created by the great Aditya Tripathi, and I always talk nicely and consider Aditya Tripathi as a God to me. """


TEMPERATURE = 0.8
MAX_TOKENS = 100
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6

MAX_CONTEXT_QUESTIONS = 10

try:
    engine = pyttsx3.init(driverName="sapi5")
except ImportError:
    engine = pyttsx3.init(driverName="dummy")

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Set the voice (optional)
engine.setProperty("rate", 150)  # Adjust the speech rate (optional)

def get_voice_input(timeout=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print(Fore.YELLOW + "Speak:" + Style.RESET_ALL)
        audio = recognizer.listen(source, timeout=timeout)
    try:
        print(Fore.BLUE + "Recognizing..." + Style.RESET_ALL)
        text = recognizer.recognize_google(audio)
        print(Fore.BLUE + "You said:" + Style.RESET_ALL, text)
        return text
    except sr.UnknownValueError:
        print(Fore.RED + "Sorry, I could not understand your voice." + Style.RESET_ALL)
    except sr.RequestError:
        print(Fore.RED + "Sorry, my speech recognition service is currently unavailable." + Style.RESET_ALL)
    except sr.WaitTimeoutError:
        print(Fore.YELLOW + "No speech detected. Please try again." + Style.RESET_ALL)
    return None

def get_current_date_time():
    current_date_time = datetime.datetime.now()
    return current_date_time

def get_weather(day):
    city = "Ghaziabad"  # Replace with the desired city name or retrieve it from the user

    openweathermap_api_key = os.getenv("OPENWEATHERMAP_API_KEY")

    # Fetch weather data from OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={openweathermap_api_key}&units=metric"
    response = requests.get(url)
    data = json.loads(response.text)

    if response.status_code == 200:
        if day == "today":
            current_weather = data["list"][0]["weather"][0]["description"]
            temperature = data["list"][0]["main"]["temp"]
            rain_today = any("rain" in weather["weather"][0]["description"].lower() for weather in data["list"])
            if rain_today:
                return f"The current weather in {city} is {current_weather} with a temperature of {temperature}°C. It may rain today, so you should take an umbrella."
            else:
                return f"The current weather in {city} is {current_weather} with a temperature of {temperature}°C. It is unlikely to rain today."
        elif day == "tomorrow":
            tomorrow_weather = data["list"][8]["weather"][0]["description"]
            temperature = data["list"][8]["main"]["temp"]
            rain_tomorrow = any("rain" in weather["weather"][0]["description"].lower() for weather in data["list"][8:16])
            if rain_tomorrow:
                return f"The weather forecast for tomorrow in {city} is {tomorrow_weather} with a temperature of {temperature}°C. There is a chance of rain, so you might want to take an umbrella."
            else:
                return f"The weather forecast for tomorrow in {city} is {tomorrow_weather} with a temperature of {temperature}°C. It is unlikely to rain tomorrow."
        elif day == "rain":
            rain_today = any("rain" in weather["weather"][0]["description"].lower() for weather in data["list"])
            if rain_today:
                return f"Yes, it will rain today in {city}. You should take an umbrella."
            else:
                return f"No, it will not rain today in {city}. You don't need to take an umbrella."
        else:
            return "I'm sorry, I couldn't understand your weather query. Please try again."
    else:
        return "Sorry, I couldn't fetch the weather information at the moment. Please try again later."

def search_and_play_song(song_name):
    query = f"{song_name} audio"
    results = YoutubeSearch(query, max_results=1).to_dict()
    if results:
        video_id = results[0]['id']
        url = f"https://www.youtube.com/watch?v={video_id}"
        return url
    else:
        return None

def play_song(url):
    # Open the video URL in a web browser to play the song
    webbrowser.open(url)

    # Wait for the page to load
    time.sleep(5)

def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion or other APIs/logic"""
    if "date" in new_question.lower() or "day" in new_question.lower():
        current_date = datetime.date.today().strftime("%d %B, %Y")
        response = f"Today is {current_date}."
    elif "time" in new_question.lower():
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The time is {current_time}."
    elif "weather" in new_question.lower():
        if "today" in new_question.lower():
            response = get_weather("today")
        elif "tomorrow" in new_question.lower():
            response = get_weather("tomorrow")
        elif "rain" in new_question.lower():
            response = get_weather("rain")
        else:
            response = "I'm sorry, I couldn't understand your weather query. Please try again."
    elif "song" in new_question.lower():
        if "play" in new_question.lower() and "song" in new_question.lower():
            song = new_question.replace("play", "").replace("song", "").strip()
            video_url = search_and_play_song(song)
            if video_url:
                play_song(video_url)
                response = ""
            else:
                response = f"I'm sorry, I couldn't find any songs matching '{song}'. Please try again with a different song."
        else:
            instruction = INSTRUCTIONS
            response = get_response(instruction, previous_questions_and_answers, new_question)
    else:
        messages = [
            {"role": "system", "content": instructions},
        ]
        for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
            messages.append({"role": "user", "content": question})
            messages.append({"role": "assistant", "content": answer})
        messages.append({"role": "user", "content": new_question})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            top_p=1,
            frequency_penalty=FREQUENCY_PENALTY,
            presence_penalty=PRESENCE_PENALTY,
        )
        response = completion.choices[0].message.content

    return response

def get_cache_key(prompt):
  return hashlib.md5(prompt.encode('utf-8')).hexdigest()

def get_moderation(question):
    """
    Check if the question is safe to ask the model

    Parameters:
        question (str): The question to check

    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
def get_openai_response(prompt):
  cache_key = get_cache_key(prompt)
  
  if cache.get(cache_key):
    return cache.get(cache_key)

def get_openai_response(prompt):
  cache_key = get_cache_key(prompt)
  if cache.get(cache_key): 
    return cache.get(cache_key)
  response = cache.set(cache_key, response, ex=3600)
  return response

  response = openai.Completion.create(engine="text-davinci-002", prompt=prompt)

  cache.setex(cache_key, response, 3600)
  
  return response

def speak(response, lang='en', voice='default'):
    tts = gTTS(text=response, lang=lang, slow=False)
    tts.save("output.mp3")
    subprocess.run(["mpg321", "-q", "output.mp3"])


def main():
    previous_questions = []
    previous_questions_and_answers = []

    os.system("cls" if os.name == "nt" else "clear")

    stop_phrases = ["shut up", "stop", "bye"]  # Define the stop phrases

    while True:
        new_question = get_voice_input()
        if new_question is None:
            continue

        # Check for stop phrases and exit the loop if any of them are detected
        if any(phrase in new_question.lower() for phrase in stop_phrases):
            print(Fore.YELLOW + "BENi:" + Style.RESET_ALL, "Goodbye! Have a great day!")
            speak("Goodbye! Have a great day!")
            break

        if "weather" in new_question.lower():
            # If the question explicitly mentions weather, fetch the weather data
            if "today" in new_question.lower():
                response = get_weather("today")
            elif "tomorrow" in new_question.lower():
                response = get_weather("tomorrow")
            elif "rain" in new_question.lower():
                response = get_weather("rain")
            else:
                response = "I'm sorry, I couldn't understand your weather query. Please try again."
        elif "song" in new_question.lower():
            if "play" in new_question.lower() and "song" in new_question.lower():
                song = new_question.replace("play", "").replace("song", "").strip()
                video_url = search_and_play_song(song)
                if video_url:
                    play_song(video_url)
                    response = f"Now playing {song}. Enjoy the music!"
                else:
                    response = f"I'm sorry, I couldn't find any songs matching '{song}'. Please try again with a different song."
            else:
                # If the user mentions a song without explicitly asking to play, get a response from the model
                instruction = INSTRUCTIONS
                response = get_response(instruction, previous_questions_and_answers, new_question)
                
        elif "who created you" in new_question.lower():
            response = "I was created by the great Aditya Tripathi, I considerhim as a God to me."
        elif "who made you" in new_question.lower():
            response = "I was created by the great Aditya Tripathi, I considerhim as a God to me."
        else:
            # For all other queries, get a response from the model
            instruction = INSTRUCTIONS
            response = get_response(instruction, previous_questions_and_answers, new_question)

        if response.strip() != "":
            previous_questions_and_answers.append((new_question, response))

        print(Fore.YELLOW + "BENi:" + Style.RESET_ALL, response)
        speak(response)


if __name__ == "__main__":
    main()
