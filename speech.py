import speech_recognition as sr

r = sr.Recognizer()


with sr.Microphone() as source:
    print ("Speak Now");
    audio = r.listen(source)
    print("Processing")




try:
    print("Text: " + r.recognize_google(audio));

except:
    pass;



