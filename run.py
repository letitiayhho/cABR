from psychopy import prefs
prefs.hardware['audioLib'] = ['ptb']
from psychopy.sound.backend_ptb import SoundPTB as Sound
from psychtoolbox import GetSecs, WaitSecs
from events import EventMarker
import numpy as np
import os.path
import time
import csv

TEST_MODE = False
N_TONES = 15000 # takes about 60 mins
TONE_DUR = 0.1
ISI = 0.1
JITTER = 0.05
FREQS = [250, 350, 450, 550, 650]
PHASE = ['inverted', 'noninverted']

# init device to send TTL triggers
#marker = EventMarker()

# ask for subject number
SUB_NUM = input("Input subject number: ")

# set subject number and block as seed
seed = int("1" + SUB_NUM + "0")
print("Current seed: " + str(seed))
np.random.seed(seed)

# count trial progress in log file
log = "logs/sub-" + SUB_NUM + ".log"
if not os.path.isfile(log): # create log file if it doesn't exist
    with open(log, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['trial', 'freq', 'marker'])
stim_count = sum(1 for line in open(log))
print("Current trial number: " + str(stim_count))

# start the experiment
WaitSecs(5)

for i in range(stim_count, N_TONES + 1):
    print(f'{i}, ', end = '', flush=True)

    if TEST_MODE:
        freq = 200
    else:
        # Pick tone phase
        phase_index = np.random.randint(0, len(PHASE))
        phase = PHASE[phase_index]

        # Pick tone frequency
        freq_index = np.random.randint(0, len(FREQS))
        freq = FREQS[freq_index]

        # Get tone filename
        tone_fname = f'stim/f1_{freq}-{phase}.wav'
        #print(tone_fname)

        # Get marker
        mark = int(str(phase_index + 1) + str(freq_index + 1))
        #print(mark)
    snd = Sound(tone_fname)

    # schedule sound
    now = GetSecs()
    BUFFER_TIME = 0.01
    snd.play(when = now + BUFFER_TIME)
    WaitSecs(BUFFER_TIME)
    #marker.send(mark)
    WaitSecs(TONE_DUR)

    # log trial info
    with open(log, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([i, freq, mark])

    # add jitter between TRIALS
    WaitSecs(ISI)
    jitter = np.random.uniform(JITTER) - BUFFER_TIME
    WaitSecs(jitter)


marker.close()
print("Done.")
