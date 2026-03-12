import sys
import os
import pythoncom
import win32com.client

input_file = r"C:\Users\陈定平\.openclaw\media\outbound\330f91c8-9488-474e-ab6f-a4f309eeabf2.dwg"
output_file = r"C:\Users\陈定平\.openclaw\media\outbound\converted.pdf"

# Try eDrawings COM
try:
    print("Attempting to create eDrawings COM object...")
    # Try known ProgIDs
    for progid in ["EModelViewer.EModelViewerCtrl", "eDrawings.Control", "eDrawings.eDrawingControl"]:
        try:
            edrawings = win32com.client.Dispatch(progid)
            print(f"Success with {progid}")
            break
        except:
            continue
    else:
        print("No eDrawings COM object found")
        
    # If we have edrawings object, try to open file and export
    if 'edrawings' in locals():
        print("Opening file...")
        edrawings.OpenDoc(input_file, False, False, False, "")
        
        # Need to find export method. Might be SaveAs or Export
        # Try SaveAs
        try:
            edrawings.SaveAs(output_file)
            print(f"Saved to {output_file}")
        except:
            print("SaveAs failed, trying other methods...")
            # Try printing to PDF
            # This is more complex
            
except Exception as e:
    print(f"COM error: {e}")

# Try AutoCAD COM if available
try:
    print("\nTrying AutoCAD COM...")
    acad = win32com.client.Dispatch("AutoCAD.Application")
    print("AutoCAD COM object created")
    doc = acad.Documents.Open(input_file)
    # Export to PDF
    doc.Export(output_file, "PDF")
    doc.Close()
    print(f"Exported to {output_file}")
except Exception as e:
    print(f"AutoCAD COM error: {e}")