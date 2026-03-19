import sys
import os

# Try to read DWG/DXF file
try:
    import ezdxf
except ImportError:
    print("ezdxf not installed")
    sys.exit(1)

input_file = r"C:\Users\陈定平\.openclaw\media\outbound\330f91c8-9488-474e-ab6f-a4f309eeabf2.dwg"
output_file = r"C:\Users\陈定平\.openclaw\media\outbound\converted.pdf"

if not os.path.exists(input_file):
    print(f"Input file not found: {input_file}")
    sys.exit(1)

try:
    # Try to load as DXF
    doc = ezdxf.readfile(input_file)
    print(f"File loaded successfully. DXF version: {doc.dxfversion}")
    
    # For now, just report success
    # In production, you would convert to PDF here
    print(f"Would convert to: {output_file}")
    
    # Simple conversion: create a PDF with some representation
    # This is a placeholder - actual conversion requires more work
    import matplotlib.pyplot as plt
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    Frontend(ctx, out).draw_layout(doc.modelspace(), finalize=True)
    
    fig.savefig(output_file, dpi=300)
    print(f"PDF saved to: {output_file}")
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)