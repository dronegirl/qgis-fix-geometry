# Load the layer by name
layer_name = "Mash West Farms"
layer = QgsProject.instance().mapLayersByName(layer_name)

if not layer:
    print(f"Layer '{layer_name}' not found.")
else:
    layer = layer[0]
    # Check if the layer is editable
    if not layer.isEditable():
        layer.startEditing()

    # Create a list to hold features with fixed geometries
    fixed_features = []

    for feature in layer.getFeatures():
        geometry = feature.geometry()

        # Check if the geometry is valid
        if not geometry.isGeosValid():
            print(f"Fixing geometry for feature ID: {feature.id()}")

            # Attempt to fix the geometry
            geometry = geometry.makeValid() # This method attempts to fix the invalid geometry

            # Create a new feature with the valid geometry
            new_feature = QgsFeature(feature)
            new_feature.setGeometry(geometry)
            # Add to the list of fixed features
            fixed_features.append(new_feature)

    # Remove invalid features (if needed) and add fixed features back to the layer
    if fixed_features:
        layer.deleteFeatures([f.id() for f in layer.getFeatures() if not f.geometry().isGeosValid()])
        layer.addFeatures(fixed_features)

    # Commit the changes and save
    layer.commitChanges()
    print("Geometry fixing complete.")