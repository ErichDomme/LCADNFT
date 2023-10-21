import clr
import os
import json

# .NET references
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
clr.AddReference("System.Windows.Forms")
clr.AddReference("Microsoft.VisualBasic")
clr.AddReference('System.Net')

# Imports
from Autodesk.Revit.DB import IFCExportOptions, IFCVersion, Transaction
from Autodesk.Revit.UI import TaskDialog
from System.Windows.Forms import FolderBrowserDialog, DialogResult
from Microsoft.VisualBasic import Interaction
from System.Net import WebClient, WebHeaderCollection, WebException
from System.Text import Encoding

# Function to export IFC
def export_to_ifc(doc, export_folder, filename):
    ifc_options = IFCExportOptions()
    ifc_options.FileVersion = IFCVersion.IFC2x3
    doc.Export(export_folder, filename, ifc_options)

# Function to get filename from user
def get_filename_from_user(export_folder):
    while True:
        default_filename = "model"
        prompt_text = "Enter desired filename for the IFC export (without extension):"
        title = "Filename"
        filename = Interaction.InputBox(prompt_text, title, default_filename)
        if not filename:
            return None  # User pressed cancel
        complete_path = os.path.join(export_folder, filename + ".ifc")
        if os.path.exists(complete_path):
            TaskDialog.Show(
                "File Exists",
                "A file with this name already exists. Please choose another name.",
            )
            continue
        else:
            return filename

# Function to upload file to IPFS using Pinata
def pin_file_to_ipfs(file_path):
    api_endpoint = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    api_key = "93407b953284346d89e2"
    api_secret = "c6153a7e62502c242c7c7415b40bab18fea5dd921457e632a58eab03c194c736"
    
    client = WebClient()
    client.Headers.Add("pinata_api_key", api_key)
    client.Headers.Add("pinata_secret_api_key", api_secret)
    
    try:
        response = client.UploadFile(api_endpoint, file_path)
        response_string = Encoding.UTF8.GetString(response)
        return json.loads(response_string)
    except WebException as e:
        return str(e.Response.GetResponseStream().ReadToEnd())

# Main function
def main():
    # Show folder browser dialog to get export path
    folder_browser = FolderBrowserDialog()
    if folder_browser.ShowDialog() == DialogResult.OK:
        export_folder = folder_browser.SelectedPath
        filename = get_filename_from_user(export_folder)

        if filename:
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
                Task
