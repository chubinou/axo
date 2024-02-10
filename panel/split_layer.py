import xml.etree.ElementTree as ET
import sys
import os
import copy

def ink_ns(s):
    return "{http://www.inkscape.org/namespaces/inkscape}"+s

def svg_ns(s):
    return "{http://www.w3.org/2000/svg}"+s

def separate_layers(svg_file):
    # Parsing the SVG file
    ET.register_namespace("","http://www.w3.org/2000/svg")
    ET.register_namespace("inkscape","http://www.inkscape.org/namespaces/inkscape")
    ET.register_namespace("sodipodi","http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")

    
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Finding all layers
    layers = {}
    for layer in root.findall('{http://www.w3.org/2000/svg}g'):
        if not layer.get(ink_ns('groupmode')) == "layer":
            continue
        layer_id = layer.get(ink_ns("label"))
        layers[layer_id] = layer

    # Creating output directory
    output_dir = os.path.splitext(svg_file)[0] + "_layers"
    os.makedirs(output_dir, exist_ok=True)

    # Saving each layer to a separate file
    for layer_id, layer in layers.items():
        layer_file = os.path.join(output_dir, f"{layer_id}.svg")

        # Create a copy of the original SVG tree
        layer_tree = copy.deepcopy(tree)

        # Remove all layers except the current one
        
        for group in layer_tree.findall('./{http://www.w3.org/2000/svg}g'):
            if not layer.get(ink_ns('groupmode')) == "layer":
                continue

            if group.get(ink_ns('label')) != layer_id:
                layer_tree.getroot().remove(group)

        # Write the modified tree to file
        layer_tree.write(layer_file, encoding="UTF-8", xml_declaration=True)

    print(f"{len(layers)} layers separated and saved to {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python separate_layers.py <path_to_svg_file>")
        sys.exit(1)

    svg_file = sys.argv[1]
    separate_layers(svg_file)
