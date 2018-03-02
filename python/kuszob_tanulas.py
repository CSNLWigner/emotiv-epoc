## kuszob tanulas
import pickle
import numpy as np
import sys

CHANNELS = ['T7','T8']

file_input = sys.argv[1]
adat = pickle.load(open(file_input,'rb'))
bounds = pickle.load(open('CALIBRATION_BOUNDS.pkl','rb'))

ablak_meret = 4
atlagok = []
atlagok_1 = []
maximum = 0

for ch in CHANNELS:
    MAX = bounds['max'][ch]
    MIN = bounds['min'][ch]
    adat[ch] = (adat[ch]-(MAX+MIN)/2)/(MAX-MIN)

for i in range(1,len(adat[CHANNELS[0]])-ablak_meret):
    ablak = np.zeros((len(CHANNELS), ablak_meret))
    for j, ch in enumerate(CHANNELS):
        ablak[j,:] = adat[ch][i:(i+ablak_meret)]
    atlagok.append(np.mean(ablak))
    if (adat['input'][i] == 1):
        atlagok_1.append(maximum)
        maximum = np.mean(ablak)
    elif maximum < np.mean(ablak):
        maximum = np.mean(ablak)

kuszob = min(atlagok_1)


pickle.dump(kuszob, open('vivi_szemoldok_kuszob.pkl','wb'))
print(kuszob)