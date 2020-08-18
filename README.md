### (Compatible with Inkscape versions 1.0 and 0.92)
![Demo](https://github.com/Shriinivas/etc/blob/master/inkscapejoinpaths/illustrations/inkscape_joinpaths_demo.gif)
# Inkscape Extension For Joining Paths<br>
This extension lets the user join SVG paths <br>

# Installation
There are two variants of this extension.<br><br>
<b>Without Optimized Option</b><br>
Script Files join_paths.py and join_paths.inx<br><br>
<b>With Optimized Option</b><br>
Script Files join_paths_optim.py and join_paths_optim.inx<br><br>
To install the extension copy the py and inx files in the user extension folder. The extension folder can be found from Edit->Preference dialog in the System option. You will need to restart inkscape after the files are copied.<br><br>
# Usage
After installation the extensions will be under Extensions->Modify Path menu. <br><br>
<b>Without Optimized Option</b><br>
Select the paths that are to be joined and invoke the 'Join Paths' menu option. The selected paths will be joined based on their Z-order (i.e. the lowest one in the document first and then the next one and so on) at their end nodes with a straight line segment. <br>
If the ending nodes of the paths coincide, they are merged and no new segment is created.<br><br>
<b>With Optimized Option</b><br>
This extension (Join Path Optimized) has a single option in the tool dialog, which says 'optimized'. When the option is unchecked the behavior is the same as the Join Paths extension described above. If it's checked, the paths are joined starting with the one with the lowest Z-order (one at the bottom most position in the document) and the successive paths to be joined are chosen based on the distance of their end nodes to the ending node of the earlier path, i.e. the one with one of the end nodes closest to the ending node of the earlier path is joined to it.<br><br>

# Tutorials
Quick Introduction: https://youtu.be/mC7rtjkT4kc
