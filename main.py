import tkinter as tk
from tkinter import ttk
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import keyboard

# Function to list audio devices
def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    devices = []
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            devices.append(device_info.get('name'))
    p.terminate()
    return devices

# Function to update the selected device
def update_selected_device():
    selected_device = input_device.get()
    status_text = f"Selected Audio Input Device: {selected_device}\n"
    status_box.insert(tk.END, status_text)
    status_box.see(tk.END)
    start_audio_stream()

# Function to start the audio stream
def start_audio_stream():
    global stream, p, device_index
    
    device_index = audio_devices.index(input_device.get())

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, input_device_index=device_index, frames_per_buffer=1024)

    update_volume_level()

# Function to update volume level
def update_volume_level():
    global stream, last_state, threshold_entry

    try:
        data = np.frombuffer(stream.read(10240, exception_on_overflow=False), dtype=np.int16)
        volume = np.linalg.norm(data) / len(data)
        bar.set_height(volume)
        
        # Get the threshold value
        threshold = float(threshold_entry.get())
        
        # Check if volume is above or below the threshold and if the state has changed
        current_state = volume > threshold
        if current_state != last_state:
            if current_state:
                status_box.insert(tk.END, "Volume above threshold.\n")
                keyboard.press_and_release('F4')
            else:
                status_box.insert(tk.END, "Volume below threshold.\n")
                keyboard.press_and_release('F4')
            status_box.see(tk.END)
            last_state = current_state
    except IOError as e:
        print(f"Error reading from stream: {e}")
        bar.set_height(0)

    canvas.draw()
    root.after(100, update_volume_level)

# Create the main window
root = tk.Tk()
root.title("AudioSwitcher by E25FGL")
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
