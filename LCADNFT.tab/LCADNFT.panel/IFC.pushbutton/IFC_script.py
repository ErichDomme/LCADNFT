import clr

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
clr.AddReference("System.Windows.Forms")

from Autodesk.Revit.DB import IFCExportOptions, IFCVersion, Transaction
from Autodesk.Revit.UI import TaskDialog
from System.Windows.Forms import (
    FolderBrowserDialog,
    DialogResult,
    Form,
    TextBox,
    Button,
    Label,
)

# Function to export IFC
def export_to_ifc(doc, export_folder, filename):
    ifc_options = IFCExportOptions()
    ifc_options.FileVersion = IFCVersion.IFC2x3
    doc.Export(export_folder, filename, ifc_options)


# Custom input dialog to get filename
def input_filename_dialog(default_text="model.ifc"):
    form = Form()
    form.Width = 300
    form.Height = 150
    form.Text = "Input filename"

    label = Label()
    label.Text = "Enter filename for the IFC export:"
    label.Width = 280
    label.Location = Point(10, 10)
    form.Controls.Add(label)

    textbox = TextBox()
    textbox.Text = default_text
    textbox.Width = 280
    textbox.Location = Point(10, 40)
    form.Controls.Add(textbox)

    button = Button()
    button.Text = "OK"
    button.Width = 100
    button.Location = Point(190, 70)

    def button_event(sender, event):
        form.Close()

    button.Click += button_event
    form.Controls.Add(button)

    form.ShowDialog()

    return textbox.Text


# Main function
def main():
    # Show folder browser dialog to get export path
    folder_browser = FolderBrowserDialog()
    if folder_browser.ShowDialog() == DialogResult.OK:
        export_folder = folder_browser.SelectedPath

        # Ask user for filename
        filename = input_filename_dialog()

        # Check if filename ends with ".ifc". If not, append it.
        if not filename.endswith(".ifc"):
            filename += ".ifc"

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
