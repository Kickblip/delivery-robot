import time
import struct
import serial

# Define the serial port for the connection
ser = serial.Serial(
    port='/dev/serial0',
    baudrate=57600, # Pixhawk 6C default baud rate / Telem 1 port (?)
    timeout=0.1
)

# Define the message to send to the Pixhawk 6C
message = struct.pack('<iiii', 0, 0, 21196, 3)

# Send the message to the Pixhawk 6C
ser.write(message)

# Wait for a response from the Pixhawk 6C
response = ser.read(100)

# Print the response from the Pixhawk 6C
print(response)

# Close the serial connection
ser.close()








"""
The parameters in the struct.pack function specify the format of the binary data being 
sent to the Pixhawk 6C. The format string, '<iiii', is used to specify the structure of the data.

The first character, '<', specifies the byte order of the data. '<' means "little endian", 
which is the byte order used by most personal computers.

The following characters, 'iiii', specify the type and size of each item of data in the structure. 
Each 'i' character represents a signed integer (4 bytes) in the structure.

In this case, the struct.pack function is being used to send 4 integers (0, 0, 21196, 3) to the Pixhawk 6C. 
The first two integers (0 and 0) are placeholders, and the last two integers (21196 and 3) correspond 
to the command ID and confirmation value for a "vehicle_command" message in the MAVLink protocol, respectively. 
This message is used to request the Pixhawk 6C to stop all motor activity.
"""
