# coding=utf-8


from Autodesk.Revit.DB import (
    Options,
    FilteredElementCollector,
    BuiltInCategory,
    Wall,
    Solid,
    ElementId,
)

doc = __revit__.ActiveUIDocument.Document

# Dictionary to store material data with volume and area
material_data = {}

# Traverse through building elements (e.g., walls)
for element in (
    FilteredElementCollector(doc)
    .OfCategory(BuiltInCategory.OST_Walls)
    .WhereElementIsNotElementType()
):
    # Get the element's geometry
    geo_element = element.get_Geometry(Options())

    for geo_object in geo_element:
        if isinstance(geo_object, Solid):
            # Calculate volume and area
            volume = geo_object.Volume
            area = geo_object.SurfaceArea

            # Get the materials for the element
            material_ids = element.GetMaterialIds(False)

            for material_id in material_ids:
                material = doc.GetElement(material_id)
                material_name = material.Name

                # If the material is not in the dictionary, add it
                if material_name not in material_data:
                    material_data[material_name] = {"volume": 0, "area": 0}

                # Accumulate volume and area for the material
                material_data[material_name]["volume"] += volume
                material_data[material_name]["area"] += area

# Print the material data with volume and area
for material, data in material_data.items():
    print("Material: {}".format(material))
    print("Volume: {} m³".format(data["volume"]))
    print("Area: {} m²".format(data["area"]))
    print("-----")
