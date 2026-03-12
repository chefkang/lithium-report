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
            doc.Close(False)
        except:
            pass
    
    # Open the document
    print(f"Opening {input_file}")
    
    # Use SendCommand to open file with FILEDIA=0
    acad.ActiveDocument.SendCommand("FILEDIA 0 ")
    acad.ActiveDocument.SendCommand(f'OPEN "{input_file}" ')
    
    # Wait for file to open
    time.sleep(3)
    
    # Check if document opened
    if acad.Documents.Count == 0:
        print("Failed to open document")
        exit(1)
    
    doc = acad.ActiveDocument
    print(f"Opened: {doc.Name}")
    
    # Now plot to PDF using -PLOT command
    print("Starting plot command...")
    
    # Send the full plot command sequence
    commands = [
        "-PLOT ",        # Start plot command
        "Y ",           # Detailed plot configuration
        "Model ",       # Model tab
        "DWG To PDF.pc3 ",  # Printer/plotter
        "ISO A4 (210.00 x 297.00 MM) ",  # Paper size
        "Millimeters ", # Units
        "Landscape ",   # Orientation
        "No ",         # Plot upside down? No
        "Extents ",    # Plot area
        "Fit ",        # Scale to fit
        "Center ",     # Center the plot
        "Yes ",        # Plot with plot styles
        "1:1 ",        # Plot scale
        "0.00,0.00 ",  # Plot offset
        "Yes ",        # Plot with lineweights
        "No ",         # Plot with transparency
        "No ",         # Plot paper space last
        "No ",         # Hide paperspace objects
        f'"{output_file}" ',  # Output file
        "Yes ",        # Save changes to layout
        "Y ",          # Proceed with plot
    ]
    
    for cmd in commands:
        print(f"Sending: {cmd}")
        doc.SendCommand(cmd)
        time.sleep(0.5)
    
    # Wait for plot to complete
    print("Waiting for plot to complete...")
    time.sleep(5)
    
    # Check if file was created
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"✓ PDF created successfully: {output_file} ({file_size} bytes)")
    else:
        print("✗ PDF not created")
        
        # Try alternative method - use PUBLISH command
        print("\nTrying alternative method with PUBLISH...")
        publish_cmd = f'PUBLISH "{output_file}" "" "" "" "" "" "" "" '
        doc.SendCommand(publish_cmd)
        time.sleep(5)
        
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✓ PDF created with PUBLISH: {output_file} ({file_size} bytes)")
        else:
            print("✗ PUBLISH also failed")
    
    # Close document
    doc.Close(False)
    print("Document closed")
    
    # Reset FILEDIA
    acad.ActiveDocument.SendCommand("FILEDIA 1 ")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    try:
        acad.Quit()
        print("AutoCAD closed")
    except:
        pass
    pythoncom.CoUninitialize()