#(c) 2022 Tim Huckaby (@timhuckaby)
#
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####



# import the blender's python API and python's os module
import bpy, os

# select all the mesh objects in the scene
objects = bpy.context.scene.objects
for ob in objects:
    ob.select_set(ob.type == "MESH")

# get the current selection
selection = bpy.context.selected_objects

grouped_inventory = {} # Replaces 'result'

# determine metric vs imperial
unit_settings = bpy.context.scene.unit_settings
isImperial = unit_settings.system == "IMPERIAL"
CONVERSION_FACTOR = 1

# Set tolerance and conversion factor based on unit system
if isImperial:
    TOLERANCE = 1.0 / 16.0  # 0.0625 inches
    CONVERSION_FACTOR = 39.370  # meters to inches
else:
    TOLERANCE = 1.5  # 1.5mm
    CONVERSION_FACTOR = 1000  # meters to millimeters

def get_normalized_key(d):
    # This function snaps the dimension to the nearest multiple of TOLERANCE for grouping purposes.
    return round((d + (TOLERANCE / 2.0)) / TOLERANCE) * TOLERANCE

# iterate through the selected objects
for sel in selection:
    # get the current object's dimensions; convert from meters to inches if isImperial, otherwise millimeters. Round to 3 decimal places 
    dims = sel.dimensions
    x = float(round(sel.dimensions.x * CONVERSION_FACTOR, 3))
    y = float(round(sel.dimensions.y * CONVERSION_FACTOR, 3))
    z = float(round(sel.dimensions.z * CONVERSION_FACTOR, 3))
    # format and output to the screen
    unit_str = "in" if isImperial else "mm"
    scr = "%s %s - %.03f%s x %.03f%s x %.03f%s\n" % (sel.name, sel.active_material.name, x, unit_str, y, unit_str, z, unit_str)
    print(scr)

    # --- Create Normalized Key ---
    norm_x = get_normalized_key(x)
    norm_y = get_normalized_key(y)
    norm_z = get_normalized_key(z)

    size_key = (norm_x, norm_y, norm_z) # This is the group identifier

    # Store or update the group data
    if size_key not in grouped_inventory:
        grouped_inventory[size_key] = {
            "count": 0,
            "base_name": sel.name, # Use the first name encountered for reference
            "material": sel.active_material.name,
            "dimensions": (norm_x, norm_y, norm_z),
            "actual_dimensions": []  # Track actual dimensions for group verification
        }

    # Update the group statistics
    grouped_inventory[size_key]["count"] += 1
    grouped_inventory[size_key]["actual_dimensions"].append((x, y, z))


    # write the selected object's name and dimensions to a string for the file output
    # if you want to output to a txt file to open in word, notepad, etc. then use this line:
    # result += "%s - %.02fin x %.02fin x %.02fin\n" % (sel.name, x, y, z)
    # if you want to output to a csv file to open in excel so you can sort, etc. then use this line:

print(grouped_inventory)

result_csv = "" # Re-initializing the variable for CSV output based on grouped inventory

# If all items in a group have matching actual dimensions, use those instead of normalized
for key, data in grouped_inventory.items():
    actual_dims_set = set(data["actual_dimensions"])
    if len(actual_dims_set) == 1:  # All dimensions in the group are identical
        data["dimensions"] = data["actual_dimensions"][0]

# get path to render output (ie: C:\Users\TimHuckaby\)
tempFolder = os.path.expanduser('~')
# make a filename
# if you are creating a text file for word, notepad, etc uncomment this next line:
# filename = os.path.join (tempFolder, "Documents\CutList.txt")
# if you are creating a csv file for excel uncomment this next line:

filename = os.path.join (tempFolder, "Documents\CutList_Grouped.csv")

# confirm path exists
os.makedirs(os.path.dirname(filename), exist_ok=True)

# open the file to write to
file = open(filename, "w")

# write the data to file
# write the header for excel.  if you are creating a txt file you can comment out this next line:

if isImperial:
    file.write("Name (Reference), Material, Count, Length (in), Width (in), Height (in)\n")
else:
    file.write("Name (Reference), Material, Count, Length (mm), Width (mm), Height (mm)\n")

# Iterate over the grouped inventory to generate output
for key, data in grouped_inventory.items():
    norm_x, norm_y, norm_z = data["dimensions"]
    # Format: Reference Name, Material, Count, X, Y, Z
    file.write("%s, %s, %d, %.3f, %.3f, %.3f\n" % (data["base_name"], data["material"], data["count"], norm_x, norm_y, norm_z))
# close the file
file.close()
