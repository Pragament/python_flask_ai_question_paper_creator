import json
import os
import cv2
from pdf2image import convert_from_path
from PIL import Image

def convert_pdf_to_image(pdf_path):
    images = convert_from_path(pdf_path, dpi=300)
    if not images:
        raise Exception("Failed to convert PDF.")
    return images[0]

def generate_template_json_from_omr(image_path, output_path="template.json", total_questions=40):
    template = {
        "pageDimensions": [2480, 3508],
        "bubbleDimensions": [45, 45],
        "customLabels": {
            "AdmissionNo": ["digit1", "digit2", "digit3", "digit4", "digit5"]
        },
        "fieldBlocks": {},
        "preProcessors": [
            {
                "name": "CropPage",
                "options": { "morphKernel": [10, 10] }
            }
        ],
        "outputColumns": [],
        "emptyValue": ""
    }

    # Admission Number block
    template["fieldBlocks"]["AdmissionBlock"] = {
        "fieldType": "QTYPE_MCQ10",
        "origin": [80, 520],
        "fieldLabels": ["A1", "A2", "A3", "A4", "A5"],
        "bubblesGap": 50,
        "labelsGap": 45
    }

    # MCQ Blocks
    q_per_subject = total_questions // 5
    remainder = total_questions % 5
    subjects = ["Math1", "Math2", "Physics", "Chemistry", "MAT"]
    options_per_q = 4
    origin_x = 400
    origin_y = 1100
    field_counter = 1

    for i, subject in enumerate(subjects):
        q_count = q_per_subject + (1 if i == 0 and remainder > 0 else 0)
        labels = [f"Q{field_counter + j}" for j in range(q_count)]

        template["fieldBlocks"][f"{subject}_Block"] = {
            "fieldType": f"QTYPE_MCQ{options_per_q}",
            "origin": [origin_x + (i * 300), origin_y],
            "fieldLabels": labels,
            "bubblesGap": 55,
            "labelsGap": 55
        }

        template["outputColumns"].extend(labels)
        field_counter += q_count

    template["outputColumns"] = ["A1", "A2", "A3", "A4", "A5"] + template["outputColumns"]

    with open(output_path, "w") as f:
        json.dump(template, f, indent=4)

    print(f"Template JSON saved to {output_path}")

def main():
    pdf_path = "Sample\omr_sheet.pdf"   # Replace with your actual OMR PDF file
    output_json_path = "template.json"
    total_questions = 40

    print("Converting PDF to image...")
    image = convert_pdf_to_image(pdf_path)
    image_path = "converted_omr.png"
    image.save(image_path)

    print("Generating template.json...")
    generate_template_json_from_omr(image_path, output_json_path, total_questions)

if __name__ == "__main__":
    main()
