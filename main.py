import voice_invoke.snowboydecoder as snowboydecoder
import sys
import signal
import app_main
import voice_control_car.record_original as record_original
import voice_control_car.speaker_recognition.modeltraining as modeltraining
interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

usage_time = 0
usage_time_file = 'usage_times.txt'
with open(usage_time_file, 'r') as f:
    lines = f.readlines()
    first_line = lines[0]
    usage_time = first_line
    print usage_time
    print type(usage_time)

if usage_time == '1\n':
    record_original.record('ztt', 10)
    modeltraining.training('ztt', 10)
    print "master's acoustic model has been trained"
    usage_time = '2'
    with open(usage_time_file, 'w') as f:
        f.write(usage_time)

elif usage_time == '2':
    model = sys.argv[1]

    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.8)
    print('Listening... Press Ctrl+C to exit')

    # main loop
    detector.start(detected_callback=app_main.main,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)
    detector.terminate()
