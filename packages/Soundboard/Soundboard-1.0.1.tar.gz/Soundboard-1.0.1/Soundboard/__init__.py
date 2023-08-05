import math
import wave
import struct
import os

A = 440
C = int(A*math.pow(2,-9/12)) #0
C1 = int(A*math.pow(2,-8/12)) #1
D = int(A*math.pow(2,-7/12)) #2
D1 = int(A*math.pow(2,-6/12)) #3
E = int(A*math.pow(2,-5/12)) #4
F = int(A*math.pow(2,-4/12)) #5
F1 = int(A*math.pow(2,-3/12)) #6
G = int(A*math.pow(2,-2/12)) #7
G1 = int(A*math.pow(2,-1/12)) #8
A = int(A*math.pow(2,0/12)) #9
A1 = int(A*math.pow(2,1/12)) #10
B = int(A*math.pow(2,2/12)) #11
SAMPLERATE = 44100

def render(frequency,amplitude,duration,filename):
    arr = []
    for i in range(len(arr1)):
        try:
            arr.append([frequency[i],amplitude[i]*0.4,duration[i]])
        except IndexError:
            print("Please ensure that all the notes are complete with all 3 inputs (frequency, duration, and Amplitude)")
    build(arr)
    compile(filename)


def filesize(name):
    with open(name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def build(arr):
    percent = -1
    ticks = 0
    file = open("Build.txt","w")
    phase = 0;
    lastf = arr[0][0];
    lasta = 0;
    for i in range(len(arr)):
        s = arr[i][1]
        a = arr[i][2]/100*32767
        freq = arr[i][0]
        if percent < math.floor(ticks/len(arr)*100):
            percent = math.floor(ticks/len(arr)*100)
            print("Building: " + str(percent) + "%")
        for j in range(int(SAMPLERATE*s)+10000):
            if(int(math.sin(freq*(j+phase)*2*math.pi/SAMPLERATE)*a)==int(math.sin(lastf*(j+phase)*2*math.pi/SAMPLERATE)*lasta)):
                phase += j-SAMPLERATE*s
                break;
        for j in range(int(SAMPLERATE*s)):
            lasta += (a-lasta)*0.1
            file.write(str(int(math.sin(freq*(j+phase)*2*math.pi/SAMPLERATE)*lasta))+"\n")
        ticks += 1;
        lastf = freq;
    return

def compile(file_name):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")
    build = open("Build.txt","r")

    # wav params
    nchannels = 1
    sample_rate = SAMPLERATE
    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = filesize("Build.txt")
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    ticks = 0
    percent = -1
    string = ""
    for i in range(nframes):
        string = build.readline()[:-2]
        if string == "":
            string = "0"
        elif string == "-":
            string = "0"
        wav_file.writeframes(struct.pack('h',int(string)))
        ticks+=1
        if percent < math.floor(ticks/nframes*100):
           percent = math.floor(ticks/nframes*100)
           print("Compiling: " + str(percent) + "%")


    wav_file.close()
    build.close()
    os.remove("Build.txt")

    return
