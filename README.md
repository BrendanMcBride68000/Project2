# Project2
The program functions as a client-server application, communicating data from a Raspberry Pi (client) to a host machine (server).

The server program runs on a host machine (PC or PI) and creates a GUI
to display the received data from the Raspberry Pi.

The client program runs on a Raspberry Pi only and collects various system data
such as temperature, memory usage, CPU voltage, CPU frequency,
and GPU frequency using vcgencmd commands.
