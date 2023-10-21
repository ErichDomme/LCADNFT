import clr
import os
import tempfile
import json
import System
from System.Net import WebClient, WebException

# Importing required Revit and .NET assemblies
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog

# Import pyRevit libraries
from pyrevit import script

# 1. Generate IFC File
def export_ifc_file(doc):
    # Define the IFC options
    options = IFCExportOptions()
    options.AddOption("ExportBaseQuantities", "true")

    # Temporary filename
    tmp_file = tempfile.mktemp(suffix=".ifc")

    # Export IFC
    doc.Export(os.path.dirname(tmp_file), os.path.basename(tmp_file), options)

    return tmp_file


# 2. Upload to IPFS using IPFS's HTTP API
def upload_to_ipfs(file_path):
    client = WebClient()
    ipfs_api_url = "http://127.0.0.1:5001/api/v0/add"
    try:
        response_bytes = client.UploadFile(ipfs_api_url, file_path)
        response_text = System.Text.Encoding.UTF8.GetString(response_bytes)
        response_json = json.loads(response_text)
        return response_json["Hash"]
    except WebException as e:
        TaskDialog.Show("Error", f"Failed to upload to IPFS: {e.Message}")
        return None


# 3. Display hash and copy to clipboard
def display_hash_and_copy(hash_code):
    # Using pyRevit's forms to display a dialog box
    result = script.forms.alert(
        f"File Uploaded Successfully!\n\nIPFS Hash: {hash_code}",
        ok=False,
        yes=True,
        no=True,
        yes_text="Copy to Clipboard",
        no_text="Close",
    )
    if result == "Yes":
        script.clipboard.copy(hash_code)
        TaskDialog.Show("Success", "Hash copied to clipboard!")


def main():
    # Get the current document
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document

    # Export IFC
    ifc_file_path = export_ifc_file(doc)

    # Show an interim message
    TaskDialog.Show("Info", "IFC exported. Uploading to IPFS...")

    # Upload to IPFS
    ipfs_hash = upload_to_ipfs(ifc_file_path)

    # If successful, display the IPFS hash and provide the option to copy
    if ipfs_hash:
        display_hash_and_copy(ipfs_hash)


main()
