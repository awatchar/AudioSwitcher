
# Audio Input Device Monitor

This is a Python-based GUI application to monitor audio input devices. It lists available audio input devices, allows you to select one, and displays a live volume level graph. If the volume exceeds a specified threshold, it triggers a keyboard event.

## Features

- Lists available audio input devices.
- Allows the user to select an audio input device.
- Displays a live volume level graph using Matplotlib.
- Triggers a keyboard event when the volume exceeds a specified threshold.
- Displays status messages in a terminal-like text box.

## Requirements

- Python 3.x
- Tkinter
- PyAudio
- NumPy
- Matplotlib
- Keyboard

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/audio-monitor.git
   cd audio-monitor
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

   **Requirements File (`requirements.txt`)**:
   ```plaintext
   pyaudio
   numpy
   matplotlib
   keyboard
   ```

## Usage

1. **Run the application**:
   ```bash
   python audio_monitor.py
   ```

2. **Select an audio input device** from the dropdown list.

3. **Enter a threshold value** in the provided entry box.

4. **Click "Confirm Selection"** to start monitoring the selected audio input device.

5. **Observe the volume level graph** and status messages in the application window.

## Code Overview

### Main Components

- `list_audio_devices()`: Lists available audio input devices.
- `update_selected_device()`: Updates the selected device and starts the audio stream.
- `start_audio_stream()`: Starts the audio stream using PyAudio.
- `update_volume_level()`: Reads audio data, updates the volume level graph, and triggers keyboard events based on the volume threshold.

### GUI Layout

- A dropdown list to select the audio input device.
- A button to confirm the selection.
- A text box to display status messages.
- An entry box to input the volume threshold value.
- A Matplotlib figure to display the live volume level graph.

### Example Code Snippet

```python
# Create the main window
root = tk.Tk()
root.title("Select Audio Input Device")
root.resizable(False, False)  # Disable window resizing

# List of audio devices
audio_devices = list_audio_devices()

# Input device
input_device_label = ttk.Label(root, text="Select Input Device:")
input_device_label.grid(row=0, column=0, padx=10, pady=10)
input_device = ttk.Combobox(root, values=audio_devices)
input_device.grid(row=0, column=1, padx=10, pady=10)

# Button to confirm selection
confirm_button = ttk.Button(root, text="Confirm Selection", command=update_selected_device)
confirm_button.grid(row=1, column=0, columnspan=2, pady=20)

# Text box for status display with terminal-like style
status_box_label = ttk.Label(root, text="Program Status:")
status_box_label.grid(row=2, column=0, padx=10, pady=10)
status_box = tk.Text(root, height=10, width=50, bg='black', fg='white', insertbackground='white')
status_box.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Text box for threshold value
threshold_label = ttk.Label(root, text="Enter Threshold Value:")
threshold_label.grid(row=4, column=0, padx=10, pady=10)
threshold_entry = ttk.Entry(root)
threshold_entry.grid(row=4, column=1, padx=10, pady=10)
threshold_entry.insert(0, "0.1")  # Set a default threshold value

# Matplotlib figure for bar graph
fig, ax = plt.subplots()
bars = ax.bar(['Input Device'], [0], color=['blue'])
bar = bars[0]
ax.set_ylim(0, 50)  # Adjust the Y-axis as needed

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Initialize variables
stream = None
p = None
device_index = None
last_state = None  # To keep track of the previous state

# Run the application
root.mainloop()
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
