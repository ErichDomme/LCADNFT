# Import necessary modules
import clr
import ipfshttpclient

# Import Revit API
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import Document, ExporterIFCUtils, IFCExportOptions
from Autodesk.Revit.DB.Architecture import RoomFilter
from Autodesk.Revit.UI import TaskDialog
import System.Windows.Forms as Forms

# Functions
def select_directory():
    """
    Allows the user to select a directory and returns the selected path.
    Returns None if no path was selected.
    """
    dialog = Forms.FolderBrowserDialog()
    dialog.Description = "Select a Folder"
    dialog.ShowNewFolderButton = True
    
    if dialog.ShowDialog() == Forms.DialogResult.OK:
        return dialog.SelectedPath
    return None

def get_ifc_options():
    """Set IFC export options."""
    options = IFCExportOptions()
    options.FileVersion = IFCExportFileVersion.IFC4
    options.SpaceBoundaryLevel = 0
    options.ExportBaseQuantities = True
    return options

def export_ifc_file(doc, options):
    """Export the document to IFC format."""
    folder_path = select_directory()
    if folder_path:
        file_path = folder_path + "\\exported_file.ifc"
        doc.Export(folder_path, file_path, options)
        return file_path
    else:
        raise Exception("The folder does not exist.")

def upload_to_ipfs(file_path):
    """Upload the file to IPFS and return the resulting hash."""
    try:
        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
        result = client.add(file_path)
        return result['Hash']
    except Exception, e:
        raise Exception("Failed to upload to IPFS: {0}".format(e.Message))

# Main script
doc = __revit__.ActiveUIDocument.Document
options = get_ifc_options()
file_path = export_ifc_file(doc, options)
ipfs_hash = upload_to_ipfs(file_path)
TaskDialog.Show('IPFS Hash', 'File uploaded to IPFS with hash: {0}'.format(ipfs_hash))
