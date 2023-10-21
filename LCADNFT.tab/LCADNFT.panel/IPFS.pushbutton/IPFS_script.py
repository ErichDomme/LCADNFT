import clr
import requests
import os

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
clr.AddReference("System.Windows.Forms")

from Autodesk.Revit.DB import IFCExportOptions, IFCVersion, Transaction
from Autodesk.Revit.UI import TaskDialog
from System.Windows.Forms import FolderBrowserDialog, DialogResult


def export_to_ifc(doc, export_folder, filename):
    ifc_options = IFCExportOptions()
    ifc_options.FileVersion = IFCVersion.IFC2x3
    doc.Export(export_folder, filename, ifc_options)


def upload_to_ipfs(filepath):
    api_url = "http://127.0.0.1:5001/api/v0/add"
    
    with open(filepath, 'rb') as file:
        response = requests.post(api_url, files={'file': file})
        
    response_json = response.json()
    ipfs_hash = response_json.get('Hash')
    
    return ipfs_hash


def main():
    # Show folder browser dialog to get export path
    folder_browser = FolderBrowserDialog()
    if folder_browser.ShowDialog() == DialogResult.OK:
        export_folder = folder_browser.SelectedPath
        filename = "model.ifc"
        full_path = os.path.join(export_folder, filename)
        
        # Check if file with same name already exists
        if os.path.exists(full_path):
            TaskDialog.Show("Warning", "File with the same name already exists. Please use a different name.")
            return

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
            
            # Upload to IPFS
            ipfs_hash = upload_to_ipfs(full_path)
            TaskDialog.Show("IPFS", f"File uploaded to IPFS with hash: {ipfs_hash}")
            
        except Exception as e:
            TaskDialog.Show("Error", f"Error: {str(e)}")


# Run main function
main()
