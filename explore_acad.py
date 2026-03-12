import win32com.client
import pythoncom

# Ensure proper COM initialization
pythoncom.CoInitialize()

try:
    # Connect to AutoCAD
    acad = win32com.client.Dispatch("AutoCAD.Application")
    print(f"AutoCAD Version: {acad.Version}")
    print(f"Visible: {acad.Visible}")
    print(f"WindowState: {acad.WindowState}")
    
    # Explore methods and properties
    print("\n=== AutoCAD Application Methods ===")
    for attr in dir(acad):
        if not attr.startswith('_'):
            try:
                obj = getattr(acad, attr)
                if callable(obj):
                    print(f"Method: {attr}")
                else:
                    print(f"Property: {attr} = {obj}")
            except:
                print(f"Attribute (error): {attr}")
    
    # Try to list document properties
    if acad.Documents.Count > 0:
        doc = acad.ActiveDocument
        print(f"\n=== Document: {doc.Name} ===")
        print(f"FullName: {doc.FullName}")
        
        # Try to get plot configuration
        print("\n=== Plot Configurations ===")
        try:
            plot_configs = doc.PlotConfigurations
            for i in range(plot_configs.Count):
                config = plot_configs.Item(i)
                print(f"  {config.Name}")
        except Exception as e:
            print(f"  Error listing configs: {e}")
    
    # Check if we can get the active layout
    try:
        layout = doc.ActiveLayout
        print(f"\n=== Active Layout: {layout.Name} ===")
        for attr in ['PaperSize', 'PlotType', 'ConfigName', 'CanonicalMediaName']:
            try:
                val = getattr(layout, attr)
                print(f"  {attr}: {val}")
            except:
                print(f"  {attr}: (error)")
    except Exception as e:
        print(f"Layout error: {e}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    pythoncom.CoUninitialize()