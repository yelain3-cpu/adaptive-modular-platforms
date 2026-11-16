import scriptcontext as sc
import serial

def read_serial_data():
    """Read only the most recent data from the serial port."""
    if "serial_connection" in sc.sticky and sc.sticky["serial_connection"] and sc.sticky["serial_connection"].is_open:
        try:
            # Check if there is data waiting in the buffer
            while sc.sticky["serial_connection"].in_waiting > 0:
                # Continuously read and discard older data
                latest_data = sc.sticky["serial_connection"].readline().decode('utf-8').strip()
            
            # If data was found, return the most recent message
            return latest_data if 'latest_data' in locals() else None
        except Exception as e:
            print(f"Error reading from serial port: {e}")
            return None
    else:
        print("Serial port is not open.")
        return None

# Output variable
output_data = None

# Read data if the toggle is active
if read:
    output_data = read_serial_data()

# Assign output to Grasshopper variable
a = output_data
