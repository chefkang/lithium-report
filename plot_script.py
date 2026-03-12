import sys
import os
import win32com.client

input_file = r"C:\Users\陈定平\.openclaw\media\outbound\330f91c8-9488-474e-ab6f-a4f309eeabf2.dwg"
output_file = r"C:\Users\陈定平\.openclaw\media\outbound\converted.pdf"

# Create a script file
scr_content = f"""FILEDIA 0
OPEN "{input_file}"
-PLOT
Y
Model
DWG To PDF.pc3
A4
Millimeters
Landscape
No
Extents
Fit
Center
Yes
1:1
0.00,0.00
Yes
No
No
No
{output_file}
Yes
Y
CLOSE
Y
FILEDIA 1
"""

scr_path = r"C:\Users\陈定平\.openclaw\workspace\plot.scr"
with open(scr_path, 'w') as f:
    f.write(scr_content)

print(f"Script created at {scr_path}")

try:
    acad = win32com.client.Dispatch("AutoCAD.Application")
    print("AutoCAD started")
    acad.Visible = True
    
    # Run the script
    acad.ActiveDocument.SendCommand("SCRIPT ")
    acad.ActiveDocument.SendCommand(scr_path + "\n")
    
    # Wait for script to complete
    import time
    time.sleep(10)
    
    # Check if output file exists
    if os.path.exists(output_file):
        print(f"PDF created: {output_file}")
    else:
        print("PDF not created")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()