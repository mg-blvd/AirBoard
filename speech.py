import speech_recognition as sr

class VoiceRecord():
    def __init__(self):
        self.r = sr.Recognizer()


    def send_text(self):
        with sr.Microphone() as source:
            print ("Speak Now");
            self.audio = self.r.listen(source)
            print("Processing")
                
        try:
            return self.r.recognize_google(self.audio)
        except:
            pass;

