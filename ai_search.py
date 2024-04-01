from PIL import Image
import pytesseract
import os
import shutil
import time

def clear_terminal():
    os.system("clear")

clear_terminal()

def kmp_search(text, pattern):
    def build_kmp_table(pattern):
        m = len(pattern)
        kmp_table = [0] * m
        j = 0
        

        for i in range(1, m):
            while j > 0 and pattern[i] != pattern[j]:
                j = kmp_table[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            kmp_table[i] = j

        return kmp_table

    m = len(pattern)
    n = len(text)
    kmp_table = build_kmp_table(pattern)

    i = j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if j == m:
                return True  
        else:
            if j != 0:
                j = kmp_table[j - 1]
            else:
                i += 1

    return False  

def extract_text_from_image(image_path, output_text_file):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        output_file_path = os.path.join(os.path.dirname(image_path), output_text_file)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text extracted successfully and saved to {output_file_path}")
        return output_file_path, text

    except Exception as e:
        print(f"Error: {e}")
        return None, None

def move_to_folder(image_path, output_folder):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        shutil.move(image_path, os.path.join(output_folder, os.path.basename(image_path)))
        print(f"Image file moved to {output_folder}")

    except Exception as e:
        print(f"Error: {e}")

def identify_disease(text):
    diseases_keywords = {
        "cancer": ["cancer", "tumor", "oncology", "malignant", "carcinoma"],
        "fever": ["fever", "flu", "infection", "high temperature", "viral"],
        "diabetes": ["diabetes", "insulin", "blood sugar", "hyperglycemia", "type 2"],
        "asthma": ["asthma", "bronchitis", "respiratory", "wheezing", "breathing difficulty"],
        "hypertension": ["hypertension", "high blood pressure", "BP", "hypertensive", "heart disease"],
        "arthritis": ["arthritis", "joint pain", "rheumatism", "osteoarthritis", "inflammatory arthritis"],
        "allergy": ["allergy", "hay fever", "allergic", "allergen", "hypersensitivity"],
        "headache": ["headache", "migraine", "cephalgia", "tension headache", "cluster headache"],
        "depression": ["depression", "mental health", "sadness", "psychological", "mood disorder"],
    }

    for disease, keywords in diseases_keywords.items():
        for keyword in keywords:
            if kmp_search(text.lower(), keyword.lower()):
                return disease

    return None

def process_images_in_directory(input_directory):
    start_time = time.time()
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_directory, filename)
            output_text_file = os.path.splitext(filename)[0] + ".txt"

            text_file_path, text = extract_text_from_image(image_path, output_text_file)

            if text_file_path and text:
                disease = identify_disease(text)
                if disease:
                    output_folder = os.path.join(input_directory, disease)
                    move_to_folder(image_path, output_folder)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Processing completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    desktop_path = os.path.expanduser("~/Desktop")
    input_directory = os.path.join(desktop_path, "Ai")

    process_images_in_directory(input_directory)
