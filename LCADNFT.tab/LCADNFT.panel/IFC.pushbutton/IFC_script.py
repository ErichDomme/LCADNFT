import clr
import os
import tempfile
import json
import System
from System.Net import WebClient, WebException

# Importing required Revit and .NET assemblies
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
clr.AddReference("System.Windows.Forms")
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog
import System.Windows.Forms

# Define IFC export options
def get_ifc_options():
    options = IFCExportOptions()
    options.FileVersion = IFCVersion.IFC2x3CV2
    options.SpaceBoundaries = 0
    options.ExportBaseQuantities = True
    options.IncludeSiteElevation = True
    return options


# Export current document to IFC
def export_ifc_file(doc, ifc_path):
    options = get_ifc_options()
    doc.Export(ifc_path, doc.Title, options)


# Upload IFC file to IPFS
def upload_to_ipfs(ifc_file):
    gateway_url = "http://127.0.0.1:5001/api/v0/add"
    with WebClient() as client:
        response = client.UploadFile(gateway_url, ifc_file)
        response_string = System.Text.Encoding.ASCII.GetString(response)
        response_json = json.loads(response_string)
        return response_json["Hash"]


# Show the IPFS hash and copy it to clipboard
def display_hash_and_copy(hash_code):
    message = "File Uploaded Successfully!\n\nIPFS Hash: " + hash_code
    TaskDialog.Show("Success", message)
    System.Windows.Forms.Clipboard.SetText(hash_code)


def main():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    with Transaction(doc, "Export IFC"):
        temp_file_path = tempfile.mktemp(suffix=".ifc")
        export_ifc_file(doc, temp_file_path)
    try:
        ipfs_hash = upload_to_ipfs(temp_file_path)
        display_hash_and_copy(ipfs_hash)
    except WebException as e:
        TaskDialog.Show("Error", "Failed to upload to IPFS: {}".format(e.Message))
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


if __name__ == "__main__":
    main()
