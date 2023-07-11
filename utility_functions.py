import numpy as np
# These three functions are based upon this very useful webpage:
# https://newt.phys.unsw.edu.au/jw/notes.html
def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)

NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()
def note_name(n): return NOTE_NAMES[n % 12] + str(n/12 - 1)