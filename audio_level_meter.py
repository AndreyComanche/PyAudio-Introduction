import sys
import pyaudio
import math
import struct
import time

# Instantiate PyAudio
p = pyaudio.PyAudio()

# Define callback
def callback(in_data, frame_count, time_info, status):
    floatLevels = []
    for _i in range(1024):
        floatLevels.append(struct.unpack('<h', in_data[_i:_i + 2])[0])
    avgChunk = sum(floatLevels)/len(floatLevels)
    print_audio_level(avgChunk, time_info['current_time'])
    return (in_data, pyaudio.paContinue)


time_difference = [0, 0]
def print_audio_level(in_data, callback_time):
    time_difference [1] = callback_time
    if time_difference [1] - time_difference [0] > 0.1:
    	time_difference [0] = time_difference [1]
        level = get_level_dB(in_data)
        sys.stdout.write('Audio level' + str(level) + '\r')
        sys.stdout.flush()

def get_level_dB(sample_value):
    MAX_SAMPLE_VALUE = 32768
    try:
        level = (20 * math.log10(float(abs(sample_value)) / MAX_SAMPLE_VALUE))
    except ValueError:
        level = - 96.32
    return int(level)

# Open stream using callback
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=48000,
                frames_per_buffer=1024,
                input=True,
                output=True,
                stream_callback=callback)

# Start the stream
#stream.start_stream()

# Close the stream after 10 seconds
time.sleep(10)
stream.close()