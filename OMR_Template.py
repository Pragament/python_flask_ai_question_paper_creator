import json
import os
from pdf2image import convert_from_path
from PIL import Image

def convert_pdf_to_image(pdf_path):
    """Convert the first page of a PDF to an image."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    images = convert_from_path(pdf_path, dpi=300)
    if not images:
        raise Exception("Failed to convert PDF to image.")
    
    return images[0]  # Return only the first page

def generate_template_json_from_omr(image_path, output_path="template.json", total_questions=40):
    """Generate a valid OMR template.json file based on the image layout."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    template = {
        "pageDimensions": [2480, 3508],
        "bubbleDimensions": [45, 45],
        "customLabels": {
            "AdmissionNo": ["A1", "A2", "A3", "A4", "A5"]
        },
        "fieldBlocks": {},
        "preProcessors": [],  # ✅ CropPage removed to avoid boundary detection issue
        "outputColumns": [],
        "emptyValue": ""
    }

    # Admission Number block — QTYPE_MCQ5 (0–4 options per digit)
    template["fieldBlocks"]["AdmissionBlock"] = {
        "fieldType": "QTYPE_MCQ5",
        "origin": [80, 520],
        "fieldLabels": ["A1", "A2", "A3", "A4", "A5"],
        "bubblesGap": 50,
        "labelsGap": 45
    }

    # Subject blocks for MCQs
    q_per_subject = total_questions // 5
    remainder = total_questions % 5
    subjects = ["Math1", "Math2", "Physics", "Chemistry", "MAT"]
    options_per_q = 4
    origin_x = 400
    origin_y = 1100
    field_counter = 1

    for i, subject in enumerate(subjects):
        q_count = q_per_subject + (1 if i < remainder else 0)
        labels = [f"Q{field_counter + j:03}" for j in range(q_count)]

        template["fieldBlocks"][f"{subject}_Block"] = {
            "fieldType": f"QTYPE_MCQ{options_per_q}",
            "origin": [origin_x + (i * 300), origin_y],
            "fieldLabels": labels,
            "bubblesGap": 55,
            "labelsGap": 55
        }

        template["outputColumns"].extend(labels)
        field_counter += q_count

    # Prepend admission labels to output columns
    template["outputColumns"] = ["A1", "A2", "A3", "A4", "A5"] + template["outputColumns"]

    with open(output_path, "w") as f:
        json.dump(template, f, indent=4)

    print(f"✅ Template JSON saved to '{output_path}'")

def main():
    pdf_path = "./Sample/omr_sheet.pdf"  # Use the uploaded file
    output_json_path = "template.json"
    total_questions = 40

    print("🔄 Converting PDF to image...")
    image = convert_pdf_to_image(pdf_path)
    image_path = "converted_omr.png"
    image.save(image_path)

    print("🛠️ Generating template.json...")
    generate_template_json_from_omr(image_path, output_json_path, total_questions)

if __name__ == "__main__":
    main()
