import sys
import argparse
import random
import pandas as pd
from datetime import datetime
import numpy as np

from tspf_stomp.stomp import TSPFStomp
from tspf_util.generate import tsgenerate_motifs

def main():
    """Scripted techniques for pattern finding in event data."""
    
    # Have a parent parser for all approaches
    #main_args_parser = argparse.ArgumentParser(add_help=False)
    #main_args_parser.add_argument('technique', choices=['haar', 'stomp'], default='stomp')
    
    # Include our child parsers.
    stomp = TSPFStomp()
    ts = tsgenerate_motifs()
    mp.identify_motifs(ts)

if __name__ == "__main__":
    main()



 