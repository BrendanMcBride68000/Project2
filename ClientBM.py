'''

TPRG 2131 Fall 2023 Project 2
Dec 14, 2023
Brendan McBride


ClientBM.py

The client program runs on a Raspberry Pi only and collects various system data
such as temperature, memory usage, CPU voltage, CPU frequency,
and GPU frequency using vcgencmd commands.

'''

import socket
import time
import json
import os
import PySimpleGUI as sg
import sys

def pi_temperature():
    # Function to retrieve core temperature from Pi
    t = os.popen('vcgencmd measure_temp').readline()
    return float(t.strip()[5:-3])  # Extract temperature as a float value with one decimal place

def pi_memory_usage():
    # Function to retrieve memory usage of the ARM processor
    m = os.popen('vcgencmd get_mem arm').readline()
    return float(m.split('=')[1].split('M')[0])  # Extract memory usage as a float value with one decimal place

def pi_cpu_voltage():
    # Function to retrieve CPU voltage from Pi
    cpuv = os.popen('vcgencmd measure_volts').readline()
    return float(cpuv.strip()[5:-2])  # Extract CPU voltage as a float value with one decimal place

def pi_cpu_frequency():
    # Function to retrieve CPU frequency from Pi
    cpuf = os.popen('vcgencmd measure_clock arm').readline()
    return float(cpuf.strip()[14:]) / 1e1  # Extract CPU frequency as a float value with one decimal place

def pi_gpu_frequency():
    # Function to retrieve GPU frequency from Pi
    gpuf = os.popen('vcgencmd measure_clock core').readline()
    return float(gpuf.strip()[14:]) / 1e1  # Extract GPU frequency as a float value with one decimal place

def collect_data(iteration):
    # Collect data including iteration count and Pi vcgencmd data
    temperature = pi_temperature()
    memory_usage = pi_memory_usage()
    cpu_voltage = pi_cpu_voltage()
    cpu_frequency = pi_cpu_frequency()
    gpu_frequency = pi_gpu_frequency()

    data = {
        "Iteration": iteration,
        "Temperature": temperature,
        "MemoryUsage": memory_usage,
        "CPUVoltage": cpu_voltage,
        "CPUFrequency": cpu_frequency,
        "GPUFrequency": gpu_frequency
    }
    return data

def send_data(data):
    # The socket that sends the data to the server
    s = socket.socket()
    host = '10.102.13.161'  
    port = 5006

    try:
        s.connect((host, port))
        s.send(bytes(json.dumps(data), 'utf-8'))
        

        s.close()
    except socket.error as e:
        print("Error: Unable to connect to the server.")
        s.close()

def create_gui():
    layout = [
        [sg.Text('Connection Status:')],
        [sg.Text('', font=('Arial', 20), key='-LED-', size=(2, 1))],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Client Status', layout)
    return window

def main():
    if sys.platform != 'linux':
        print("This script can only run on a Raspberry Pi. Get lost!")
        sys.exit()

    iterations = 50
    window = create_gui()

    for i in range(1, iterations + 2):
        event, _ = window.read(timeout=100)
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

        if i % 2 == 0:
            window['-LED-'].update('⏺')  # Unicode On LED
        else:
            window['-LED-'].update('⚪')  # Unicode Off LED

        data = collect_data(i)
        send_data(data)
        time.sleep(2)  # Wait for 2 seconds before next iteration

    window.close()
    print("Goodbye")

if __name__ == '__main__':
    main()
