import time
from pprint import pprint

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, AggOperations, WaveletTypes, NoiseEstimationLevelTypes, \
    WaveletExtensionTypes, ThresholdTypes, WaveletDenoisingTypes

folder_name = 'think_data'
def main():
    BoardShim.enable_dev_board_logger()



    # read data from csv
    # params = BrainFlowInputParams()
    board_id = BoardIds.GANGLION_NATIVE_BOARD.value
    pprint(BoardShim.get_board_descr(board_id))
    # board = BoardShim(board_id, params)
    # board.prepare_session()
    # board.start_stream()
    # BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    # time.sleep(10)
    # data = board.get_current_board_data(500)
    data = DataFilter.read_file('C:\\Users\\akash\\PycharmProjects\\Brainflow-bci\\think_data\\test_60_1694967344.csv')
    # board.stop_stream()
    # board.release_session()

    # Board details
    exg_channel = BoardShim.get_exg_channels(board_id)
    sampling_rate = BoardShim.get_sampling_rate(board_id)
    print(f"No of EEG Channels : {exg_channel}\n"
          f"Sampling Rate : {sampling_rate}")

    # demo how to convert it to pandas DF and plot data
    eeg_channels = BoardShim.get_eeg_channels(board_id)
    df = pd.DataFrame(np.transpose(data))
    plt.figure()
    df[eeg_channels].plot(subplots=True)
    plt.savefig('before_processing.png')

    # demo for denoising, apply different methods to different channels for demo
    for count, channel in enumerate(eeg_channels):
        # first of all you can try simple moving median or moving average with different window size
        if count == 0:
            DataFilter.perform_rolling_filter(data[channel], 3, AggOperations.MEAN.value)
        elif count == 1:
            DataFilter.perform_rolling_filter(data[channel], 3, AggOperations.MEDIAN.value)
        # if methods above dont work for your signal you can try wavelet based denoising
        # feel free to try different parameters
        else:
            DataFilter.perform_wavelet_denoising(data[channel], WaveletTypes.BIOR3_9, 3,
                                                 WaveletDenoisingTypes.SURESHRINK, ThresholdTypes.HARD,
                                                 WaveletExtensionTypes.SYMMETRIC, NoiseEstimationLevelTypes.FIRST_LEVEL)

    df = pd.DataFrame(np.transpose(data))
    plt.figure()
    df[eeg_channels].plot(subplots=True)
    plt.savefig('after_processing.png')


if __name__ == "__main__":
    main()
