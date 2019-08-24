import numpy as np


# Hardware Information
SAMPLING_RATE = 20

# Threshold Parameters
PEAK_THRESHOLD = 3
IE_THRESHOLD   = 1.5
IS_THRESHOLD   = 0.8

PEAK_RECOVER_T   = 2.5 # peak recover time in seconds
IE_RANGE_T       = 1
IS_RANGE_T       = -1.2

WINDOW_RANGE = (-2.2, 1)
MINIMUM_VALLEY_RANGE = 0.5

PEAK_DURATION_THRESHOLD = 1.8

ARI_INTERVAL = 0.35

FFI_INTERVAL = 0.2
FFT_THRESHOLD = 0.8


def hello():
    print("hello")

# feature extraction in "God View"
def feature_extraction(vector):
    pt_i = None
    len = vector.shape[0]
    indexes = np.argwhere(vector > PEAK_THRESHOLD).reshape(-1)
    print(indexes)
    # find the peak
    for i in range(indexes.shape[0]):
        if (indexes[i] + PEAK_RECOVER_T * SAMPLING_RATE) < len:  # not
            if i == indexes.shape[0] - 1:  # come to the last one
                    pt_i = indexes[i]
            elif indexes[i+1] - indexes[i] >= PEAK_RECOVER_T * SAMPLING_RATE:
                pt_i = indexes[i]
        elif i == indexes.shape[0] - 1:
            pt_i = indexes[i]

    print(pt_i)

    if pt_i is None:
        return None

    # find impact start
    is_i = pt_i
    is_search_range = int(pt_i+IS_RANGE_T*SAMPLING_RATE) if pt_i+IS_RANGE_T*SAMPLING_RATE >0 else 0
    for i in range(is_search_range, pt_i):
        if vector[i] < IS_THRESHOLD:
            for j in range(i+1, pt_i):
                if vector[j] > IE_THRESHOLD:
                    is_i = j
                    break
            break
    print(is_i)

    # find impact end
    ie_i = int(pt_i + IE_RANGE_T * SAMPLING_RATE)
    for i in range(int(pt_i + IE_RANGE_T * SAMPLING_RATE), pt_i, -1):
        if vector[i] >= IE_THRESHOLD:
            ie_i = i
            break
    print(ie_i)

    # find ammv
    ammv = AMMV(vector[is_i:ie_i+2])

    # find impact duration
    idi = (ie_i - is_i) / float(SAMPLING_RATE)

    # find maximum peak
    mpi = np.max(vector[is_i:ie_i+1])

    # find minimum valley
    mvi = np.min(vector[int(is_i-MINIMUM_VALLEY_RANGE*SAMPLING_RATE):ie_i+1])
    print(mvi)

    # find peak duration index
    ps_i = pt_i   # peak start
    while vector[ps_i] > PEAK_DURATION_THRESHOLD:
        ps_i = ps_i - 1
    pe_i = pt_i   # peak end
    while vector[pe_i] > PEAK_DURATION_THRESHOLD:
        pe_i = pe_i + 1
    pdi = (pe_i - ps_i) / float(SAMPLING_RATE)
    print(pdi)

    # find activity ratio index
    center = int((ie_i + is_i) / 2.0)
    interval = vector[int(center-ARI_INTERVAL*SAMPLING_RATE) : int(center+ARI_INTERVAL*SAMPLING_RATE)]
    print(interval)
    ari = 1 - float(np.argwhere(np.logical_and(interval >= 0.85, interval <= 1.3)).reshape(-1).shape[0]) / interval.shape[0]
    print("ari: " + str(ari))

    # find FFI
    ffi_i = pt_i - FFI_INTERVAL * SAMPLING_RATE
    for i in range(ffi_i, pt_i):
        if vector[i] < FFT_THRESHOLD:
            ffi_i = i
            break
    interval = vector



def AMMV(window):
    ammv = 0
    for i in range(window.shape[0]-1):
        ammv = ammv + abs(window[i]-window[i+1])
    ammv = ammv / (window.shape[0])
    print(ammv)
    return ammv


if __name__ == "__main__":
    import pandas as pd
    import numpy as np

    index = 53
    sorted_data = pd.read_csv("data.txt", sep=" ", header=None).values
    print(sorted_data[index, :])
    feature_extraction(sorted_data[index, :])

