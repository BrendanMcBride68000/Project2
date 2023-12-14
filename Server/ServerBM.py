'''

TPRG 2131 Fall 2023 Project 2
Dec 14, 2023
Brendan McBride


ServerBM.py

The server program runs on a host machine and creates a GUI
to display the received data from the Raspberry Pi.

'''

import socket
import json
import PySimpleGUI as sg

def create_gui():
    # Function to create the GUI layout
    layout = [
        [sg.Text('Received Pi Information')],
        [sg.Text('Temperature: '), sg.Text('', size=(15, 1), key='-TEMPERATURE-')],
        [sg.Text('Memory Usage: '), sg.Text('', size=(15, 1), key='-MEMORY_USAGE-')],
        [sg.Text('CPU Voltage: '), sg.Text('', size=(15, 1), key='-CPU_VOLTAGE-')],
        [sg.Text('CPU Frequency: '), sg.Text('', size=(15, 1), key='-CPU_FREQUENCY-')],
        [sg.Text('GPU Frequency: '), sg.Text('', size=(15, 1), key='-GPU_FREQUENCY-')],
        [sg.Text('Iteration Count: '), sg.Text('', size=(15, 1), key='-ITERATION-')],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Server Status', layout)
    return window

def receive_data():
    # Function to receive data from the client
    s = socket.socket()
    host = '0.0.0.0'  
    port = 5006

    s.bind((host, port))
    s.listen(5)

    window = create_gui()
    connected = False

    while True:
        c, addr = s.accept()  # Accept the incoming connection
        print('Got connection from', addr)
        
        received_data = c.recv(1024).decode('utf-8')  # Receive data from client
        if received_data:
            data_dict = json.loads(received_data)
            event, _ = window.read(timeout=100)  # Read events from GUI
            window.refresh()  # Refresh the window to update changes
            window['-TEMPERATURE-'].update(data_dict.get('Temperature', ''))
            window['-MEMORY_USAGE-'].update(data_dict.get('MemoryUsage', ''))
            window['-CPU_VOLTAGE-'].update(data_dict.get('CPUVoltage', ''))
            window['-CPU_FREQUENCY-'].update(data_dict.get('CPUFrequency', ''))
            window['-GPU_FREQUENCY-'].update(data_dict.get('GPUFrequency', ''))
            window['-ITERATION-'].update(data_dict.get('Iteration', ''))  # Update iteration count
            
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

    window.close()
    s.close()

if __name__ == '__main__':
    receive_data()

