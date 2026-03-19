import win32com.client
import pythoncom
import os
import time

input_file = r"C:\Users\陈定平\.openclaw\media\outbound\330f91c8-9488-474e-ab6f-a4f309eeabf2.dwg"
output_file = r"C:\Users\陈定平\.openclaw\media\outbound\converted.pdf"

# Clean output file
if os.path.exists(output_file):
    os.remove(output_file)

pythoncom.CoInitialize()

try:
    print("Connecting to AutoCAD...")
    acad = win32com.client.Dispatch("AutoCAD.Application")
    acad.Visible = True  # Make visible for debugging
    
    print(f"AutoCAD Version: {acad.Version}")
    
    # Close any open documents first
    for i in range(acad.Documents.Count - 1, -1, -1):
        try:
            doc = acad.Documents.Item(i)
            print(f"Closing: {doc.Name}")
            doc.Close(False)
        except:
            pass
    
    time.sleep(1)
    
    # Open the document directly using Documents.Open
    print(f"\nOpening {input_file}")
    try:
        doc = acad.Documents.Open(input_file)
        print(f"Opened: {doc.Name}")
    except Exception as e:
        print(f"Error opening file: {e}")
        # Try with SendCommand approach
        print("Trying SendCommand approach...")
        # First ensure we have a document
        if acad.Documents.Count == 0:
            acad.Documents.Add()
            time.sleep(1)
        
        doc = acad.ActiveDocument
        doc.SendCommand(f'OPEN "{input_file}" ')
        time.sleep(3)
    
    # Now we should have the document open
    if acad.Documents.Count == 0:
        print("No document open, creating new one...")
        doc = acad.Documents.Add()
    else:
        doc = acad.ActiveDocument
    
    print(f"Working with document: {doc.Name}")
    
    # Set FILEDIA to 0 to suppress file dialogs
    doc.SendCommand("FILEDIA 0 ")
    time.sleep(0.5)
    
    # Try using the PLOT command with a script file approach
    print("\nCreating plot script...")
    script_content = f"""_PLOT
Y
Model
DWG To PDF.pc3
ISO A4 (210.00 x 297.00 MM)
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
"{output_file}"
Yes
Y
"""
    
    script_path = r"C:\Users\陈定平\.openclaw\workspace\plot_script.scr"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"Script saved to: {script_path}")
    
    # Run the script
    print("Running plot script...")
    doc.SendCommand(f'SCRIPT "{script_path}" ')
    
    # Wait for plot to complete
    print("Waiting for plot to complete...")
    time.sleep(10)
    
    # Check if file was created
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"✓ PDF created successfully: {output_file} ({file_size} bytes)")
    else:
        print("✗ PDF not created")
        print("\nTrying direct SendCommand sequence...")
        
        # Try direct command sequence
        commands = [
            "_.PLOT\n",
            "Y\n",
            "Model\n",
            "DWG To PDF.pc3\n",
            "ISO A4 (210.00 x 297.00 MM)\n",
            "Millimeters\n",
            "Landscape\n",
            "No\n",
            "Extents\n",
            "Fit\n",
            "Center\n",
            "Yes\n",
            "1:1\n",
            "0.00,0.00\n",
            "Yes\n",
            "No\n",
            "No\n",
            "No\n",
            f'"{output_file}"\n',
            "Yes\n",
            "Y\n",
        ]
        
        for cmd in commands:
            print(f"Sending: {cmd.strip()}")
            doc.SendCommand(cmd)
            time.sleep(0.5)
        
        time.sleep(5)
        
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✓ PDF created: {output_file} ({file_size} bytes)")
        else:
            print("✗ Still no PDF")
    
    # Reset FILEDIA
    doc.SendCommand("FILEDIA 1 ")
    
    # Close document without saving
    time.sleep(1)
    doc.Close(False)
    print("Document closed")
    
    # Close AutoCAD
    time.sleep(1)
    acad.Quit()
    print("AutoCAD closed")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    
    try:
        acad.Quit()
    except:
        pass
        
finally:
    pythoncom.CoUninitialize()