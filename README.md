# Connect Paths - Inkscape Extension

This Inkscape extension allows you to connect multiple SVG paths in your document with various options for customization.

## Features

- Connect all the selected paths with adjustable curvature or straight line
- Multiple options for determining connection order
- Handling of composite paths

## Installation

1. Download the `join_paths.inx` and `join_paths.py` files.
2. Place these files in your Inkscape extensions folder (you will find this in System menu under Edit-Preferences).
3. Restart Inkscape if it's already running.

## Usage

1. Open your SVG file in Inkscape.
2. Select two or more paths or open shapes you want to connect.
3. Go to Extensions > Generate from Path > Connect Paths.
4. Choose your desired options:

   - **Curvature Factor**:

     - 0 creates straight lines.
     - Positive values create outward curves, negative values create inward curves.
     - Higher absolute values increase curve intensity.

   - **Path Order**:

     - Selection Order: Connects paths in the order they were selected.
     - Selection Order Reversed: Connects paths in reverse selection order.
     - Z-order: Connects paths based on their stack order in the document.
     - Z-order Reversed: Connects paths in reverse stack order.
     - Distance: Connects paths based on proximity. The first selected path is the starting point.

   - **Composite Path Handling**:

     - Break Apart and Join Separately: Treats each subpath as separate for connecting.
     - Treat as Single Path: Connects the entire composite path as one unit.

   - **Close Path**: If checked, connects the last path back to the first.
   - **Delete Original**: If checked, deletes the original paths after connecting.

5. Click "Apply" to connect the paths.

## License

[GPL2](https://github.com/Shriinivas/inkscapejoinpaths/blob/master/LICENSE)
