# Blender-Cut-List

**Python Code to create a woodworking cut list in Excel format from a 3D drawing in Blender using the Blender API**

---

### Definition
A cut list for a Woodworking project is the Bill of Materials (BOM) for all the pieces of wood that need to be cut before assembly.

### Purpose
This Python script iterates through every mesh object in a Blender 3D drawing, generating a CSV-formatted Cut List that can then be imported and modified within Excel.

### Background
The most popular woodworking design software is SketchUp, which has native Cut List functionality, and most woodworking projects are designed using it. However, the initial model for this tool was created in **Blender**, an open-source 3D modeling and creation suite. Blender is capable of rendering 3D for movie animation and games.

My personal journey involved having to learn Blender to modify a model (specifically for a 2020 Toyota Tundra Truck Cap Camper Furniture set) that contained hundreds of pieces to be cut. Manually creating the cut list would have been a herculean task, with significant penalties for failure. I realized, **"There must be an automated way to do a cut list."**

### Programming Notes
Writing the code to automate this process actually took significantly more time than it would have taken to type out the cut list manually! Hopefully, this tool will save you a substantial amount of time.

*   I am primarily a **.NET developer** and had limited experience with Python when starting this project. Being an engineer by trade, I naturally tended toward over-engineering the solution.
*   I initially assumed that similar work—utilizing the Blender API and object model in Python—already existed for me to reference; this was not the case. My success is directly related to understanding the Blender object model, API, and the power of Python's real-time interpreter.

**Important Caveats:**
1.  As with any piece of software, it is never truly "done"; improvements are always possible.
2.  I have not tested this script against a wide variety of drawings, so rigorous testing with other models will likely reveal bugs or issues that need addressing.
3.  There are minor annoyances I haven't had time to fix. For instance, cameras and lights are mesh objects within Blender, causing them to be outputted to the cut list. It should be easy enough to spot and delete these entries in Excel.

### How to Use
1.  Open your 3D drawing file in **Blender**.
2.  Select **"Scripting"** from the main menu.
3.  You will see a command prompt area at the bottom left. Paste the code into this window and press **Enter**.
4.  The program will execute, and its output (the cut list) will be written to a file named `cut-list.csv` in your **Documents** folder (`...\my documents\`).

#### Next Steps in Excel:
Once you open `cut-list.csv` in Microsoft Excel, remember to:
1.  Go to the **Data** menu.
2.  Select **Filter**. This will put the spreadsheet into a structured format allowing you to easily sort by any column.
