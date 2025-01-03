import numpy as np
import matplotlib.pyplot as plt
import cleese_stim as cleese
from cleese_stim.engines import PhaseVocoder
import csv

n = 0
num = ["num"]
p1int = ["p1"]
p2int = ["p2"]
p3int = ["p3"]
p4int = ["p4"]
p1 = ["p1"]
p2 = ["p2"]
p3 = ["p3"]
p4 = ["p4"]
for n in range(1400):
    input_file = "./norm_stim_bonjour_homme.wav"
    config_file = "./config/90centsrandom_pitch_profile.toml"

    wave_in, sr, _ = PhaseVocoder.wav_read(input_file)
    wave_out, bpf_out = cleese.process_data(PhaseVocoder, wave_in, config_file, sample_rate=sr)
    bpf_1int = int(bpf_out[0,1])
    p1int.append(bpf_1int)
    bpf_2int = int(bpf_out[1,1])
    p2int.append(bpf_2int)    
    bpf_3int = int(bpf_out[2,1])
    p3int.append(bpf_3int)
    bpf_4int = int(bpf_out[3,1])
    p4int.append(bpf_4int)
    bpf_1 = bpf_out[0,1]
    p1.append(bpf_1)
    bpf_2 = bpf_out[1,1]
    p2.append(bpf_2)
    bpf_3 = bpf_out[2,1]
    p3.append(bpf_3)
    bpf_4 = bpf_out[3,1]
    p4.append(bpf_4)

    n += 1
    num.append(n)
    output_file = "./1400x90cents/Bjr90cents"+str(n)+"_p1at"+str(bpf_1int)+"_p2at"+str(bpf_2int)+"_p3at"+str(bpf_3int)+"_p4at"+str(bpf_4int)+".wav"
    PhaseVocoder.wav_write(wave_out, output_file, sr)
rows = zip(num, p1int, p2int, p3int, p4int)
rowz = zip(num, p1, p2, p3, p4)
with open("./1400x90cents/1400x90intversion.csv", "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
with open("./1400x90cents/1400x90floatversion.csv", "w") as f:
    writer = csv.writer(f)
    for row in rowz:
        writer.writerow(row)