import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import soundfile as sf
import os
from pydub import AudioSegment
from math import ceil

os.chdir(r'C:\Users\Igor\Desktop\OTTranscription')

dlina = int(input('Введите точную длину аудио В СЕКУНДАХ: '))

adio = AudioSegment.from_file("1.wav", format="wav")
k = 0
ftext = ''

for i in range(ceil(dlina / 60)):
    start_time = k
    end_time = min(60 * (i+1), dlina)
    # Срез аудио
    part1 = adio[start_time*1000:end_time*1000]

    # Сохранение части
    partn = f"part_{i+1}.wav"
    part1.export(partn, format="wav")
    k += 60

    # А теперь важная часть: используем speech_recognition, чтобы загрузить запись на распознание
    recognizer = sr.Recognizer()
    with sr.AudioFile(partn) as source:
        audio = recognizer.record(source)
        
        # Отправляем аудиофайл в Google Speech Recognition API, чтобы получить распознанный текст.
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print(f"{i+1}) {text}")
            ftext += text + ''
        
        #Осталось обработать возможные ошибки    
        except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
            print("Не удалось распознать речь.")
        except sr.RequestError as e:             # - если нет интернета или API недоступен
            print(f"Ошибка сервиса: {e}")
            
if ftext:
    print('Тест:', ftext)
    lang = input("Введите код языка для перевода (например, 'en' — английский, 'es' — испанский): ")
    translator = Translator()
    translated = translator.translate(ftext, dest=lang)
    print("🌍 Перевод:", translated.text)
