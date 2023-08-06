import csv
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams


def record_data_to_csv(filename, duration):
    # Create a BrainFlow instance for the OpenBCI Ganglion board
    board_id = brainflow.board_shim.BoardIds.GANGLION_NATIVE_BOARD.value
    params = BrainFlowInputParams()
    board = BoardShim(board_id, params)

    # Set the sampling rate to 200 Hz (maximum supported by Ganglion)
    board.prepare_session()
    board.config_board("sampling_rate", 200)

    # Connect to the board
    board.connect()

    # Start streaming
    board.start_stream()

    # Initialize an empty list to store the data
    data = []

    try:
        # Read EEG data for the specified duration (in seconds)
        while board.get_board_data_count() < duration * board.get_sampling_rate():
            # Get the latest chunk of data
            data_chunk = board.get_board_data()

            # Append the chunk to the data list
            data.extend(data_chunk)

        # Stop streaming and disconnect
        board.stop_stream()
        board.disconnect()

        # Write the data to a CSV file
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

        print("Data saved to:", filename)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    # Specify the filename for the CSV file
    csv_filename = "eeg_data.csv"

    # Specify the duration for data recording (in seconds)
    recording_duration = 10  # for example, record data for 10 seconds

    # Call the function to start recording and storing data in the CSV file
    record_data_to_csv(csv_filename, recording_duration)
