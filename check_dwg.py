import struct

input_file = r"C:\Users\陈定平\.openclaw\media\outbound\330f91c8-9488-474e-ab6f-a4f309eeabf2.dwg"

with open(input_file, 'rb') as f:
    data = f.read(100)
    print(f"First 100 bytes (hex): {data.hex()}")
    # DWG header starts with "AC"
    if data[0:2] == b'AC':
        print("DWG file signature found")
        version = data[2:6]
        print(f"Version bytes: {version}")
    else:
        print("Not a standard DWG file?")
        
    # Try to read as ASCII
    print(f"ASCII: {data[:50]!r}")