from RealtimeTTS import TextToAudioStream, GTTSEngine

engine = GTTSEngine(voice="en")  # تهيئة محرك الصوت

stream = TextToAudioStream(engine)

def speak_response(response_text):
    stream.feed(response_text)
    stream.play()

def stop_speaking():
    try:
        stream.stop()  # محاولة إيقاف الصوت الحالي
    except AttributeError:
        print("Stop method not supported by RealtimeTTS stream")