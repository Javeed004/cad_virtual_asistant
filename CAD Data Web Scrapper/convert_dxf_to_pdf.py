import FreeCAD, Import
import TechDraw
import os

# Input and output folders
input_folder = "cad_files_raw"
output_folder = "images"
os.makedirs(output_folder, exist_ok=True)

# Path to drawing template (adjust if needed)
# For Linux:
# template_path = "/usr/share/freecad/Mod/TechDraw/Templates/A4_Landscape.svg"
# For Windows (example):
template_path = "C:/Program Files/FreeCAD 1.0/data/Mod/TechDraw/Templates/A4_Landscape.svg"

# Loop through all .dxf or .DXF files
for filename in os.listdir(input_folder):
    if not filename.lower().endswith(".dxf"):
        continue

    input_path = os.path.join(input_folder, filename)
    base_name = os.path.splitext(filename)[0]
    output_pdf = os.path.join(output_folder, f"{base_name}.pdf")

    print(f"📄 Processing: {filename}")

    # Create a new FreeCAD document
    doc = FreeCAD.newDocument(base_name)
    
    # Import the DXF file
    Import.insert(input_path, base_name)

    # Create a drawing page and template
    page = doc.addObject('TechDraw::DrawPage', 'Page')
    template = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
    template.Template = template_path
    page.Template = template

    # Recompute the document and export to PDF
    doc.recompute()
    page.ViewObject.exportPdf(output_pdf)
    print(f"✅ PDF exported: {output_pdf}")
