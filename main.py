import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import pyjokes
import pywhatkit as kit
import wikipedia

recongnizer= sr.Recognizer()
engine= pyttsx3.init()
newsapi= "6711732980614c7ebab24c76e37c4a80"
weatherapi= "2e4a563af129ea2edd3f5e8327fdce4c"
city_name= "Bhopal"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif "open chatgpt" in c.lower():
        webbrowser.open("https://chatgpt.com")

    elif "open whatsapp" in c.lower():
        webbrowser.open("https://whatsapp.com")

    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")

    elif c.lower().startswith("play"):
        parts = c.lower().split(" ", 1)  # Split into two parts: the command and the video name
        if len(parts) > 1:
            video_name = parts[1].strip()  # Get the video name name and remove extra spaces
            kit.playonyt(video_name) # Use pywhatkit to play the video on YouTube

    elif "news" in c.lower():
        r= requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apikey={newsapi}")
        if r.status_code==200:
            data= r.json() # Parse the JSON reponse

            articles= data.get('articles',[]) # Extract the artcles

            if articles:
                speak("Here are the top headlines:")
                
                # Speak the top 5 headlines
                for i, article in enumerate(articles[:5], start=1):  # Limit to 5 headlines
                    title = article.get('title', 'No Title Available')
                    speak(f"Headline {i}: {title}")
            else:
                speak("Sorry, I couldn't find any news articles at the moment.")
        else:
            speak("Sorry, there was an issue fetching the news. Please try again later.")
            

    elif "joke" in c.lower():
        joke= pyjokes.get_joke()  # Fetch a random joke
        print(joke)
        speak(joke)

    elif "weather" in c.lower():
        try:
        # Replace 'your_api_key_here' with your actual OpenWeatherMap API key
            api_key = "2e4a563af129ea2edd3f5e8327fdce4c"
            base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
            
            # Make the API request
            response = requests.get(base_url)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract weather details
                city = data.get("name", "Unknown Location")
                temperature = data["main"]["temp"]
                weather_desc = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                
                # Prepare the weather report
                weather_report = (
                    f"The weather in {city} is currently {weather_desc} with a temperature of {temperature}°C. "
                    f"The humidity is {humidity}% and the wind speed is {wind_speed} meters per second."
                )
            
                # Announce the weather
                print(weather_report)
                speak(weather_report)
            else:
                speak("Sorry, I couldn't fetch the weather information. Please try again later.")
                print(f"Error: {response.status_code} - {response.reason}")
        except Exception as e:
            speak("An error occurred while fetching the weather information.")
            print(f"Error: {e}")

        
    else:
        topic= c.lower()
        try:
            # Fetch a brief summary (2 sentences by default)
            summary = wikipedia.summary(topic, sentences=2)
                
            # Print and speak the summary
            print(f"Summary of {topic}:\n{summary}")
            speak(summary)
        except wikipedia.DisambiguationError as e:
                print(f"Multiple results found for '{topic}': {e.options}")
                speak(f"Multiple results found for '{topic}'. Please be more specific.")
        except wikipedia.PageError:
            print(f"No page found for '{topic}'.")
            speak(f"Sorry, I couldn't find any information about '{topic}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
            speak("An error occurred while fetching the information.")



if __name__== "__main__":
    speak("Intializing jarvis...")
    while True:
        # Listen for the wake word "Jarvis"
        # Obtain audio from the microphone
        r= sr.Recognizer()

        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio= r.listen(source,timeout=2,phrase_time_limit=1)

            word= r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Activated...")
                    audio= r.listen(source)
                    command= r.recognize_google(audio)

                    processCommand(command)



        except Exception as e:
            print("Error; {0}".format(e))