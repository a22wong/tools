import pyaudio
import wave
import sys

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS_LIMIT = 120
WAVE_OUTPUT_FILENAME = "stream.wav"
OUTPUT_DIRECTORY_PATH = "stream/"

def main():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording...")

    frames = []

    try:
        wf = wave.open(OUTPUT_DIRECTORY_PATH+WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        if RECORD_SECONDS_LIMIT > 0:
            # for limited recording
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS_LIMIT)):
                data = stream.read(CHUNK)
                # frames.append(data)
                wf.writeframes(data)
        else:
            # for endless recording
            while True:
                data = stream.read(CHUNK)
                # frames.append(data)
                wf.writeframes(data)
    except KeyboardInterrupt:
        print("\n* terminating early")

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # wf = wave.open(OUTPUT_DIRECTORY_PATH+WAVE_OUTPUT_FILENAME, 'wb')
    # wf.setnchannels(CHANNELS)
    # wf.setsampwidth(p.get_sample_size(FORMAT))
    # wf.setframerate(RATE)
    # wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == '__main__':
    try:
        WAVE_OUTPUT_FILENAME = sys.argv[1]+".wav"
    except:
        print("* no output filename provided")
        print("* using default: %s" % WAVE_OUTPUT_FILENAME)

    try:
        RECORD_SECONDS_LIMIT = int(sys.argv[2])
        if RECORD_SECONDS_LIMIT == 0:
            print("* endless recording")
        else:
            print("* recording limited to "+str(RECORD_SECONDS_LIMIT)+" seconds")
    except:
        print("* recording limited to default "+str(RECORD_SECONDS_LIMIT)+" seconds")


    main()
