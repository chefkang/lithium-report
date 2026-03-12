import sys
import os
import time

# Add the gen_py cache path
import win32com.client.gencache
import pythoncom
import win32com.client

input_file = r"C:\Users\陈定平\.openclaw\media\outbound\330f91c8-9488-474e-ab6f-a4f309eeabf2.dwg"
output_file = r"C:\Users\陈定平\.openclaw\media\outbound\converted.pdf"

# Clean output file
if os.path.exists(output_file):
    os.remove(output_file)

def main():
    # Initialize COM in STA mode
    pythoncom.CoInitialize()
    
    try:
        print("Creating AutoCAD COM object...")
        # Use EnsureDispatch to get proper type info
        acad = win32com.client.gencache.EnsureDispatch("AutoCAD.Application")
        acad.Visible = True
        
        print(f"AutoCAD Version: {acad.Version}")
        
        # Close any existing documents
        print("Closing existing documents...")
        while acad.Documents.Count > 0:
            try:
                doc = acad.Documents.Item(0)
                doc.Close(False)
            except:
                pass
            time.sleep(0.5)
        
        time.sleep(1)
        
        # Open the target file
        print(f"Opening {input_file}")
        try:
            # Try Documents.Open first
            doc = acad.Documents.Open(input_file)
            print(f"Successfully opened: {doc.Name}")
        except Exception as e:
            print(f"Open failed: {e}")
            return
        
        # Create a simple script that uses PLOT command
        print("Creating plot script...")
        script = f'''FILEDIA
0
-PLOT
Yes
Model
"DWG To PDF.pc3"
"ISO A4 (210.00 x 297.00 MM)"
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
Yes
FILEDIA
1
'''
        
        # Save script to temp file
        script_path = os.path.join(os.environ['TEMP'], 'plot_dwg.scr')
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script)
        
        print(f"Script saved to: {script_path}")
        
        # Run the script
        print("Running plot script...")
        try:
            doc.SendCommand(f'SCRIPT "{script_path}" ')
        except Exception as e:
            print(f"SendCommand error: {e}")
            # Try direct commands
            print("Trying direct command sequence...")
            commands = script.split('\n')
            for cmd in commands:
                if cmd.strip():
                    try:
                        doc.SendCommand(cmd.strip() + ' ')
                    except:
                        pass
                    time.sleep(0.1)
        
        # Wait for plot to finish
        print("Waiting for plot completion...")
        for i in range(30):  # Wait up to 30 seconds
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"✓ PDF created: {output_file} ({file_size} bytes)")
                break
            time.sleep(1)
        
        if not os.path.exists(output_file):
            print("✗ PDF not created after waiting")
            
            # Try one more approach - use ExportPDF command if available
            print("Trying ExportPDF command...")
            try:
                # AutoCAD 2013+ has PDFEXPORT command
                doc.SendCommand('PDFEXPORT ')
                doc.SendCommand(f'"{output_file}" ')
                time.sleep(5)
                
                if os.path.exists(output_file):
                    file_size = os.path.getsize(output_file)
                    print(f"✓ PDF created with PDFEXPORT: {output_file} ({file_size} bytes)")
                else:
                    print("✗ PDFEXPORT also failed")
            except Exception as e:
                print(f"PDFEXPORT error: {e}")
        
        # Close document
        print("Closing document...")
        try:
            doc.Close(False)
        except:
            pass
        
        # Close AutoCAD
        print("Closing AutoCAD...")
        try:
            acad.Quit()
        except:
            pass
        
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    main()