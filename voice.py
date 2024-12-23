import pyttsx3
import speech_recognition as sr
import random
import sys

engine = pyttsx3.init()
def set_language(language):
    if language == "ru":
        voices = engine.getProperty('voices')
        for voice in voices:
            if "ru" in voice.languages:
                engine.setProperty('voice', voice.id)
                break
        return "ru-RU"
    elif language == "en":
        voices = engine.getProperty('voices')
        for voice in voices:
            if "en" in voice.languages:
                engine.setProperty('voice', voice.id)
                break
        return "en-US"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech(recognizer, microphone, language):
    with microphone as source:
        print("Слушаю...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "Ошибка подключения к сервису распознавания речи."
def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    language = set_language("ru")

    speak("Здравствуйте! Я ваш голосовой помощник. Чем могу помочь?")

    while True:
        user_input = recognize_speech(recognizer, microphone, language)
        if not user_input:
            speak("Извините, я не расслышал. Повторите, пожалуйста.")
            continue

        print(f"Вы сказали: {user_input}")

        if ("привет" in user_input.lower() and language == "ru-RU") or ("hello" in user_input.lower() and language == "en-US"):
            speak("Привет! Чем я могу помочь?" if language == "ru-RU" else "Hello! How can I assist you?")

        elif ("пока" in user_input.lower() and language == "ru-RU") or ("goodbye" in user_input.lower() and language == "en-US"):
            speak("До свидания! Хорошего дня!" if language == "ru-RU" else "Goodbye! Have a great day!")
            sys.exit()

        elif ("подбрось монетку" in user_input.lower() and language == "ru-RU") or ("flip a coin" in user_input.lower() and language == "en-US"):
            result = random.choice(["орёл", "решка"] if language == "ru-RU" else ["heads", "tails"])
            speak(f"Выпало: {result}." if language == "ru-RU" else f"It's {result}.")

        elif ("измени язык" in user_input.lower() and language == "ru-RU") or ("change language" in user_input.lower() and language == "en-US"):
            speak("На какой язык вы хотите переключиться? Скажите 'английский' или 'русский'." if language == "ru-RU" else "Which language would you like to switch to? Say 'English' or 'Russian'.")
            lang_choice = recognize_speech(recognizer, microphone, language)
            if "английский" in lang_choice.lower() or "english" in lang_choice.lower():
                language = set_language("en")
                speak("Язык изменён на английский." if language == "ru-RU" else "Language switched to English.")
            elif "русский" in lang_choice.lower() or "russian" in lang_choice.lower():
                language = set_language("ru")
                speak("Язык изменён на русский." if language == "ru-RU" else "Language switched to Russian.")
            else:
                speak("Язык не распознан. Попробуйте снова." if language == "ru-RU" else "Language not recognized. Please try again.")

        else:
            speak("Я не понял эту команду. Попробуйте ещё раз." if language == "ru-RU" else "I didn't understand that command. Please try again.")

if __name__ == "__main__":
    main()
