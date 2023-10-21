# Import necessary .NET assemblies
import clr

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

import System.Windows.Forms as WinForms

# Function to export IFC
def export_to_ifc(doc, export_path):
    ifc_options = IFCExportOptions()
    ifc_options.FileVersion = IFCVersion.IFC2x3
    doc.Export(export_path, ".ifc", ifc_options)


# Main function
def main():
    # Show folder browser dialog to get export path
    folder_browser = WinForms.FolderBrowserDialog()
    if folder_browser.ShowDialog() == WinForms.DialogResult.OK:
        export_path = folder_browser.SelectedPath
        # Ensure path ends with .ifc
        if not export_path.lower().endswith(".ifc"):
            export_path += r"\model.ifc"
        # Export IFC
        try:
            export_to_ifc(doc=revit.doc, export_path=export_path)
            TaskDialog.Show("Success", "IFC Exported Successfully!")
        except Exception as e:
            TaskDialog.Show("Error", f"Error exporting IFC: {str(e)}")


# Run main function
main()
