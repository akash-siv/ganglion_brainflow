import time

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter


def main():
    BoardShim.enable_dev_board_logger()

    # use synthetic board for demo
    params = BrainFlowInputParams()
    board_id = BoardIds.GANGLION_NATIVE_BOARD.value
    sampling_rate = BoardShim.get_sampling_rate(board_id)
    board = BoardShim(board_id, params)
    # board.prepare_session()
    # board.start_stream()
    # BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    # time.sleep(10)
    data = DataFilter.read_file('C:\\Users\\akash\\PycharmProjects\\Brainflow-bci\\think_data\\test_60_1694967344.csv')
    # board.stop_stream()
    # board.release_session()

    eeg_channels = BoardShim.get_eeg_channels(board_id)
    bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate, True)
    print("avg band powers : %s" % str(bands[0]))
    print("stddev band powers : %s" % str(bands[1]))


if __name__ == "__main__":
    main()
