# Uses Python SpeechRecognizer API to record a 2 second audio slice                                                                               
                                                                                                      
import speech_recognition as sr  
import pyaudio

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# Speech recognizer credits go to the authors at 
# https://pypi.python.org/pypi/SpeechRecognition/

r = sr.Recognizer()
m = sr.Microphone()
m.SAMPLE_RATE = 48000
with m as source:
    # set's threshold to background noise level
    r.adjust_for_ambient_noise(source)
    while True:
        print('Speak:')
        audio = r.record(source, 2)
        try:
            print("You said " + r.recognize_google(audio))   
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))