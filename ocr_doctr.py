import os
from PIL import Image
import cv2
import numpy as np
import re
import io
import json
import sys

from doctr.models import ocr_predictor
from doctr.io import DocumentFile

# --- English words dictionary setup ---
try:
    import nltk
    nltk.download('words', quiet=True)
    from nltk.corpus import words as nltk_words
    ENGLISH_WORDS = set(w.lower() for w in nltk_words.words())
except Exception as e:
    # print(f"Warning: Could not load nltk words corpus: {e}")
    ENGLISH_WORDS = set()

def is_meaningful(word):
    # Consider a word meaningful if it's in the dictionary and at least 3 letters
    return word.lower() in ENGLISH_WORDS and len(word) >= 3

def count_meaningful_words(words):
    return sum(1 for w in words if is_meaningful(w))

try:
    doctr_model = ocr_predictor(pretrained=True)
except Exception as e:
    # print(f"Error loading Doctr OCR predictor: {e}")
    doctr_model = None

def ocr_and_count_words(image_pil_object, model):
    img_byte_arr = io.BytesIO()
    image_pil_object.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    doc = DocumentFile.from_images([img_byte_arr])
    result = model(doc)
    words = []
    for page in result.pages:
        for block in page.blocks:
            for line in block.lines:
                words.extend([word.value for word in line.words])
    return words

def extract_text_from_image(image_pil_object, model, apply_preprocessing=False):
    final_image_for_doctr = image_pil_object

    if apply_preprocessing:
        cropped_img_cv = np.array(image_pil_object)
        if len(cropped_img_cv.shape) == 3 and cropped_img_cv.shape[2] == 3:
            cropped_img_cv = cv2.cvtColor(cropped_img_cv, cv2.COLOR_RGB2BGR)
        elif len(cropped_img_cv.shape) == 3 and cropped_img_cv.shape[2] == 4:
            cropped_img_cv = cv2.cvtColor(cropped_img_cv, cv2.COLOR_RGBA2RGB)
            cropped_img_cv = cv2.cvtColor(cropped_img_cv, cv2.COLOR_RGB2BGR)

        gray_image = cv2.cvtColor(cropped_img_cv, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        _, binarized_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        if binarized_image.dtype != np.uint8:
            binarized_image = binarized_image.astype(np.uint8)

        try:
            final_image_for_doctr = Image.fromarray(binarized_image, mode='L')
        except Exception as e:
            # print(f"Warning: Error converting processed array to PIL with mode='L': {e}. Trying without explicit mode.")
            final_image_for_doctr = Image.fromarray(binarized_image)

    img_byte_arr = io.BytesIO()
    final_image_for_doctr.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    doc_zone = DocumentFile.from_images([img_byte_arr])
    result_zone = model(doc_zone)

    extracted_lines = []
    for page in result_zone.pages:
        for block in page.blocks:
            for line in block.lines:
                extracted_lines.append(" ".join([word.value for word in line.words]).strip())
    
    return "\n".join(extracted_lines)

def perform_ocr_and_parse(image_path, apply_preprocessing=False):
    extracted_data = {
        "Name": None,
        "Father Name": None,
        "CNIC Number": None,
        "Date of Birth": None,
        "Gender": None,
        "Country of Stay": None,
    }

    if doctr_model is None:
        # print("Doctr OCR model could not be loaded. Cannot perform OCR.")
        return extracted_data

    try:
        full_image_pil = Image.open(image_path)

        # OCR for both orientations
        words_normal = ocr_and_count_words(full_image_pil, doctr_model)
        img_rotated = full_image_pil.rotate(180, expand=True)
        words_rotated = ocr_and_count_words(img_rotated, doctr_model)

        # Count meaningful words
        normal_score = count_meaningful_words(words_normal)
        rotated_score = count_meaningful_words(words_rotated)

        if rotated_score > normal_score:
            # print("Card is upside down (180° rotated).")
            full_image_pil = img_rotated
        # else
            # print("Card is correctly placed.")

        # OCR on correct orientation
        full_card_text = extract_text_from_image(
            full_image_pil, doctr_model, apply_preprocessing
        )

        if not full_card_text or not full_card_text.strip():
            # print("No text extracted. OCR output was empty.")
            return extracted_data


        all_lines_from_zone = full_card_text.split('\n')
        
        def find_and_extract_line(lines, keyword, extract_next=True, cleanup_regex=None):
            for i, line_text in enumerate(lines):
                cleaned_line_text = re.sub(r'[^a-zA-Z\s]', '', line_text).strip()
                if keyword.lower() in cleaned_line_text.lower():
                    if extract_next and i + 1 < len(lines):
                        val = lines[i+1].strip()
                        if cleanup_regex:
                            val = re.sub(cleanup_regex, '', val).strip()
                        return val
                    elif not extract_next:
                        if cleanup_regex:
                            line_text = re.sub(cleanup_regex, '', line_text).strip()
                        return line_text
            return None

        # Extract Name
        extracted_data["Name"] = find_and_extract_line(
            all_lines_from_zone, "Name", cleanup_regex=r'[^a-zA-Z\s]'
        )
        if extracted_data["Name"]: extracted_data["Name"] = extracted_data["Name"].title()

        # Extract Father Name
        extracted_data["Father Name"] = find_and_extract_line(
            all_lines_from_zone, "Father", cleanup_regex=r'[^a-zA-Z\s]'
        )
        if extracted_data["Father Name"]: extracted_data["Father Name"] = extracted_data["Father Name"].title()

        # Extract CNIC Number
        cnic_pattern = r'\b\d{5}[-\s]?\d{7}[-\s]?\d{1}\b'
        for line_text in all_lines_from_zone:
            match = re.search(cnic_pattern, line_text)
            if match:
                extracted_data["CNIC Number"] = match.group(0).replace(' ', '-').replace('--', '-')
                break

        # Extract Gender
        gender_found = False
        for i, line_text in enumerate(all_lines_from_zone):
            if "Gender" in line_text:
                gender_match = re.search(r'\b(M|F)\b', line_text, re.IGNORECASE)
                if gender_match:
                    extracted_data["Gender"] = gender_match.group(0).upper()
                    gender_found = True
                    break
                elif i + 1 < len(all_lines_from_zone):
                    next_line_text = all_lines_from_zone[i+1].strip()
                    gender_match = re.search(r'\b(M|F)\b', next_line_text, re.IGNORECASE)
                    if gender_match:
                        extracted_data["Gender"] = gender_match.group(0).upper()
                        gender_found = True
                        break
            if not gender_found and re.match(r'^\s*(M|F)\s*$', line_text.strip(), re.IGNORECASE):
                    extracted_data["Gender"] = line_text.strip().upper()
                    break

        # Extract Country of Stay
        for line_text in all_lines_from_zone:
            if "Country of Stay" in line_text:
                if "Pakistan" in line_text:
                    extracted_data["Country of Stay"] = "Pakistan"
                    break
            if "Pakistan" in line_text and extracted_data["Country of Stay"] is None:
                extracted_data["Country of Stay"] = "Pakistan"
                break
        
        # Extract Date of Birth
        dob_pattern = r'\b(\d{1,2}[-/.]\d{1,2}[-/.]\d{4})\b'
        for line_text in all_lines_from_zone:
            match = re.search(dob_pattern, line_text)
            if match:
                extracted_data["Date of Birth"] = match.group(1)
                break

        # Clean up temporary rotated image if any
        if os.path.exists("rotated_temp.jpg"):
            os.remove("rotated_temp.jpg")

        # If all fields are None, print full OCR text for manual inspection
        # if all(v is None for v in extracted_data.values()):
            # print("\nNo fields extracted. Place your card correctly and try again.")
            # print(full_card_text)

        return extracted_data

    except FileNotFoundError:
        # print(f"Error: Image file not found at {image_path}")
        return extracted_data
    except Exception as e:
        # print(f"An error occurred during main OCR process: {e}")
        return extracted_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    image_file = sys.argv[1]

    extracted_fields = perform_ocr_and_parse(
        image_file, apply_preprocessing=False
    )

    print(json.dumps(extracted_fields))

    # print("\n--- Final Extracted CNIC Fields ---")
    # for key, value in extracted_fields.items():
    #     print(f"{key}: {value}")