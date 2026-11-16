import scriptcontext as sc

def send_serial_data(message):
    """Send a string message to the serial port, with robust error handling."""
    if "serial_connection" in sc.sticky and sc.sticky["serial_connection"] and sc.sticky["serial_connection"].is_open:
        try:
            # Write the message to the serial port
            # '\n' is crucial as it will let Arduino know the end of message
            sc.sticky["serial_connection"].write((message +'\n').encode('utf-8'))
            print(f"Sent: {message}")
            return True  # Successfully sent
        except Exception as e:
            print(f"Error sending to serial port: {e}")
            return False
    else:
        print("Serial port is not open.")
        return False

# Output variable
success = False

# Send data if the toggle is active
if Send and Pin_Values:
    success = send_serial_data(Pin_Values)

# Assign output to Grasshopper variable
a = success
