# requirements: pyserial
# requirements: pyserial
# requirements: pyserial
import serial
import scriptcontext as sc

Open = Open
Port = Port

baud_rate = Baud
# port_name = 'COM' + str(Port)
port_name = '/dev/cu.usbserial-120'

def open_serial_port(port_name, baud_rate):
    """Open and return a serial port connection."""
    if "serial_connection" not in sc.sticky or sc.sticky["serial_connection"] is None:
        try:
            sc.sticky["serial_connection"] = serial.Serial(port_name, baud_rate, timeout=1)
            print(f"Serial port {port_name} opened successfully.")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            sc.sticky["serial_connection"] = None
    else:
        print("Serial port is already open.")

def close_serial_port():
    """Close the serial port."""
    if "serial_connection" in sc.sticky and sc.sticky["serial_connection"]:
        try:
            sc.sticky["serial_connection"].close()
            print("Serial port closed.")
        except serial.SerialException as e:
            print(f"Error closing serial port: {e}")
        sc.sticky["serial_connection"] = None

# Open or close the serial port based on the input
if Open:
    open_serial_port(port_name, baud_rate)
else:
    close_serial_port()

# Output the status of the serial port
a = sc.sticky["serial_connection"].is_open if "serial_connection" in sc.sticky and sc.sticky["serial_connection"] else False
