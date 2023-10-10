# Access the current Revit document
doc = __revit__.ActiveUIDocument.Document

# Create a dictionary to store material data
material_data = {}

# Traverse through building elements
for element in FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Walls
):  # Example for walls
    # Get the material for the element
    material = element.Material
    if material:
        # Extract desired properties (e.g., name, color, texture, etc.)
        material_name = material.Name
        material_color = material.Color
        # ... extract other properties as needed

        # Store the data in the dictionary
        material_data[material_name] = {
            "color": material_color,
            # ... store other properties
        }

# Print or return the material_data for further processing
print(material_data)
