import sys
import argparse
import random
import pandas as pd
from datetime import datetime
import numpy as np

def tsgenerate_motifs(num_motifs=1, motif_duration=50, motif_y_max=15, num_motif_repetition=5):
    
    time_series_duration_in_days = (num_motifs * motif_duration * num_motif_repetition * 10) % (24 * 60 * 60) + 1 
    
    date_range = pd.date_range(start='01/01/2020', periods=time_series_duration_in_days, freq='S')
    df = pd.DataFrame(date_range, columns=['time'])
    
    motifs = []
    for i in range(0, num_motifs):
        motif = []
        for j in range(0, motif_duration):
            motif.append(random.randint(0, motif_y_max))
        motifs.append(motif)
    
    non_motif_len = len(date_range) - (num_motifs * motif_duration * num_motif_repetition)
    non_motif = np.random.randint(0,25,size=non_motif_len)
    avg_delta_between_motifs = non_motif_len/(num_motifs * num_motif_repetition)
    
    data = []
    for i in range(0, num_motifs * num_motif_repetition):
        for j in range(0, random.randint(0, int(avg_delta_between_motifs))):
            data.append(random.randint(0,motif_y_max))
        data = data + motifs[i%len(motifs)]
    
    for i in range(0, len(date_range)-len(data)):
        data.append(random.randint(0,motif_y_max))
            
    df['data'] = data
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    return df

