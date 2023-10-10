# Import necessary Revit API classes
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Wall

# Access the current Revit document
doc = __revit__.ActiveUIDocument.Document

# Create a dictionary to store material data
material_data = {}

# Traverse through building elements
for element in (
    FilteredElementCollector(doc)
    .OfCategory(BuiltInCategory.OST_Walls)
    .WhereElementIsNotElementType()
):  # Example for walls
    if isinstance(element, Wall):  # Check if the element is a Wall
        wall_type = element.WallType
        compound_structure = wall_type.GetCompoundStructure()

        if compound_structure:  # Check if the wall has a compound structure
            for layer in compound_structure.GetLayers():
                material_id = layer.MaterialId
                material = doc.GetElement(material_id)

                if material:
                    # Extract desired properties
                    material_name = material.Name

                    # Extract color
                    color = material.Color
                    if color:
                        color_value = (color.Red, color.Green, color.Blue)
                    else:
                        color_value = "N/A"

                    # Extract shininess and transparency
                    appearance_asset = material.AppearanceAssetId
                    if appearance_asset.IntegerValue > 0:
                        appearance_asset_element = doc.GetElement(appearance_asset)
                        shininess = appearance_asset_element.GetSingleConnectedAsset(
                            "generic_shininess"
                        )
                        transparency = appearance_asset_element.GetSingleConnectedAsset(
                            "generic_transparency"
                        )
                    else:
                        shininess = "N/A"
                        transparency = "N/A"

                    # Store the data in the dictionary
                    material_data[material_name] = {
                        "color": color_value,
                        "shininess": shininess,
                        "transparency": transparency,
                    }

# Print or return the material_data for further processing
print(material_data)
