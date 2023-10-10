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
                    # Extract desired properties (e.g., name, color, texture, etc.)
                    material_name = material.Name
                    # ... extract other properties as needed

                    # Store the data in the dictionary
                    material_data[material_name] = {
                        # ... store properties
                    }

# Print or return the material_data for further processing
print(material_data)
