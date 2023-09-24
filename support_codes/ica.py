import time
import numpy as np
from pprint import pprint

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams
from brainflow.data_filter import DataFilter


def main():
    board_id = BoardIds.GANGLION_NATIVE_BOARD
    eeg_channels = BoardShim.get_eeg_channels(board_id)
    pprint(BoardShim.get_board_descr(board_id))

    params = BrainFlowInputParams()
    board = BoardShim(board_id, params)
    # board.prepare_session()
    # board.start_stream()
    # time.sleep(10)
    data = DataFilter.read_file('C:\\Users\\akash\\PycharmProjects\\Brainflow-bci\\think_data\\test_60_1694967344.csv')
    # data = board.get_board_data(500)
    print(len(data))
    print(data)
    # board.stop_stream()
    # board.release_session()
    print(eeg_channels)

    channel_to_use = eeg_channels[3]
    data = data[channel_to_use, :500]
    print(len(data))
    # provide 5 chunks of data for components selection
    data = data.reshape(5, 100)
    data = np.ascontiguousarray(data)
    w, k, a, s = DataFilter.perform_ica(data, 2)
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(s[0, :])
    axs[0].set_title('Unmixed signal 1')
    axs[1].plot(s[1, :])
    axs[1].set_title('Unmixed signal 2')
    plt.savefig('unmixed_signal.png')


if __name__ == "__main__":
    main()
