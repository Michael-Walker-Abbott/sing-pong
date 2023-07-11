import miniaudio
from constants import MSECS_PER_BUFFER, SAMPLES_PER_SEC

def make_audio_capture_device():
    devices = miniaudio.Devices()
    print("Available recording devices:")
    captures = devices.get_captures()
    for d in enumerate(captures):
        num = d[0]
        name = d[1]['name']
        print(f'{num} = {name}')   
    print("Available input devices:")
    selection = int(input("Enter the number of the input device: "))
    input_device = captures[selection]
    capture = miniaudio.CaptureDevice(
        buffersize_msec=MSECS_PER_BUFFER,
        sample_rate=SAMPLES_PER_SEC,
        device_id=input_device["id"],
        nchannels=1
    )
    return capture
    