import clr

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
clr.AddReference("System.Windows.Forms")

from Autodesk.Revit.DB import IFCExportOptions, IFCVersion, Transaction
from Autodesk.Revit.UI import TaskDialog
from System.Windows.Forms import FolderBrowserDialog, DialogResult

# Function to export IFC
def export_to_ifc(doc, export_folder, filename):
    ifc_options = IFCExportOptions()
    ifc_options.FileVersion = IFCVersion.IFC2x3
    doc.Export(export_folder, filename, ifc_options)

# Function to get filename from user
def get_filename_from_user():
    td = TaskDialog("Filename")
    td.MainInstruction = "Enter desired filename for the IFC export"
    td.MainContent = "Please provide a name without extension (.ifc will be added):"
    td.AddCommandLink(TaskDialogCommandLinkId.CommandLink1, "Proceed with export")
    td.AddCommandLink(TaskDialogCommandLinkId.CommandLink2, "Cancel export")

    res = td.Show()
    if res == TaskDialogResult.CommandLink1:
        return td.CommandLinkText
    return None

# Main function
def main():
    # Show folder browser dialog to get export path
    folder_browser = FolderBrowserDialog()
    if folder_browser.ShowDialog() == DialogResult.OK:
        export_folder = folder_browser.SelectedPath
        filename = get_filename_from_user()

        if filename is not None:
            filename = filename + ".ifc"
            # Export IFC
            try:
                active_doc = __revit__.ActiveUIDocument.Document
                # Start a transaction
                with Transaction(active_doc, "IFC Export") as t:
                    t.Start()
                    export_to_ifc(
                        doc=active_doc, export_folder=export_folder, filename=filename
                    )
                    t.Commit()
                TaskDialog.Show("Success", "IFC Exported Successfully!")
            except Exception as e:
                TaskDialog.Show("Error", "Error exporting IFC: {}".format(str(e)))

# Run main function
main()


# import clr

# clr.AddReference("RevitAPI")
# clr.AddReference("RevitAPIUI")
# clr.AddReference("System.Windows.Forms")

# from Autodesk.Revit.DB import IFCExportOptions, IFCVersion, Transaction
# from Autodesk.Revit.UI import TaskDialog
# from System.Windows.Forms import FolderBrowserDialog, DialogResult

# # Function to export IFC
# def export_to_ifc(doc, export_folder, filename):
#     ifc_options = IFCExportOptions()
#     ifc_options.FileVersion = IFCVersion.IFC2x3
#     doc.Export(export_folder, filename, ifc_options)


# # Main function
# def main():
#     # Show folder browser dialog to get export path
#     folder_browser = FolderBrowserDialog()
#     if folder_browser.ShowDialog() == DialogResult.OK:
#         export_folder = folder_browser.SelectedPath
#         filename = "model.ifc"

#         # Export IFC
#         try:
#             active_doc = __revit__.ActiveUIDocument.Document
#             # Start a transaction
#             with Transaction(active_doc, "IFC Export") as t:
#                 t.Start()
#                 export_to_ifc(
#                     doc=active_doc, export_folder=export_folder, filename=filename
#                 )
#                 t.Commit()
#             TaskDialog.Show("Success", "IFC Exported Successfully!")
#         except Exception as e:
#             TaskDialog.Show("Error", "Error exporting IFC: {}".format(str(e)))


# # Run main function
# main()
