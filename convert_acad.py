import sys
import os
import win32com.client

input_file = r"C:\Users\陈定平\.openclaw\media\outbound\330f91c8-9488-474e-ab6f-a4f309eeabf2.dwg"
output_file = r"C:\Users\陈定平\.openclaw\media\outbound\converted.pdf"

try:
    # Create AutoCAD application
    acad = win32com.client.Dispatch("AutoCAD.Application")
    print("AutoCAD COM object created")
    
    # Make AutoCAD visible (optional)
    acad.Visible = True
    
    # Open the document
    print(f"Opening {input_file}")
    doc = acad.Documents.Open(input_file)
    print("Document opened")
    
    # Try Export method
    print("Attempting Export...")
    try:
        # Try different format names
        for fmt in ["PDF", "AcadPDF", "DWG To PDF", "PDF"]:
            try:
                doc.Export(output_file, fmt)
                print(f"Exported using format {fmt}")
                break
            except Exception as e:
                print(f"Export with {fmt} failed: {e}")
                continue
        else:
            print("All export formats failed")
    except Exception as e:
        print(f"Export error: {e}")
    
    # Try Plot method
    print("Attempting Plot...")
    try:
        # Get layout
        layout = doc.ActiveLayout
        # Configure plot
        layout.ConfigName = "DWG To PDF.pc3"
        layout.PaperSize = "A4"
        layout.PlotType = 1  # Extents
        layout.ScaleLineweights = False
        layout.CenterPlot = True
        # Plot to file
        doc.Plot.PlotToFile(output_file)
        print(f"Plotted to {output_file}")
    except Exception as e:
        print(f"Plot error: {e}")
    
    # Close document without saving
    doc.Close(False)
    print("Document closed")
    
    # Quit AutoCAD
    acad.Quit()
    
except Exception as e:
    print(f"Overall error: {e}")
    import traceback
    traceback.print_exc()