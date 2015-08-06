import pyaudio
import wave
import sys

BUFFER_SIZE = 1024

# Opening audio file as binary data
wf = wave.open(sys.argv[1], 'rb')

# Instantiate PyAudio
p = pyaudio.PyAudio()

file_sw = wf.getsampwidth()

stream = p.open(format=p.get_format_from_width(file_sw),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(BUFFER_SIZE)

while data != '':
    stream.write(data)
    data = wf.readframes(BUFFER_SIZE)

stream.stop_stream()
stream.close()

p.terminate()