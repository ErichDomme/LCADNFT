import clr

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.UI import *

import System
from System.Collections.Generic import List
from System.Windows.Forms import FolderBrowserDialog

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


def select_directory():
    """
    Allows the user to select a directory and returns the selected path.
    Returns None if no path was selected.
    """
    dialog = FolderBrowserDialog()
    dialog.Description = "Select a Folder"
    dialog.ShowNewFolderButton = True

    if dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK:
        return dialog.SelectedPath
    return None


def get_ifc_options():
    # Example placeholder for IFC options setup
    options = IFCExportOptions()
    # options.SpaceBoundaries = 2  # This was previously causing an error
    return options


def export_ifc_file(doc, options, selected_path):
    if not selected_path:
        raise Exception("No directory selected for export.")

    # Construct the full file path using the selected directory
    file_path = System.IO.Path.Combine(selected_path, "ExportedIFC.ifc")

    # Execute export (replace with your export logic if different)
    doc.Export(selected_path, file_path, options)


def main():
    selected_path = select_directory()

    if selected_path:
        options = get_ifc_options()
        export_ifc_file(doc, options, selected_path)
    else:
        TaskDialog.Show("Error", "No directory was selected. Export cancelled.")


if __name__ == "__main__":
    main()
