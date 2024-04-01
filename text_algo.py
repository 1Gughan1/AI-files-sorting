from PIL import Image
import pytesseract
import os
import shutil
import platform
from ahocorasick import Automaton
import time

def clear_terminal():
    os.system("clear")

def build_automaton(keywords):
    automaton = Automaton()
    for keyword in keywords:
        automaton.add_word(keyword.lower(), keyword)
    automaton.make_automaton()
    return automaton

def extract_text_from_image(image_path, output_text_file):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        output_file_path = os.path.join(os.path.dirname(image_path), output_text_file)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text extracted successfully and saved to {output_file_path}")
        return output_file_path

    except Exception as e:
        print(f"Error: {e}")
        return None

def move_to_folder(image_path, keyword, base_folder):
    try:
        keyword_folder = os.path.join(base_folder, keyword.lower())
        if not os.path.exists(keyword_folder):
            os.makedirs(keyword_folder)

        
        shutil.move(image_path, os.path.join(keyword_folder, os.path.basename(image_path)))
        print(f"Image file moved to {keyword} folder")

    except Exception as e:
        print(f"Error: {e}")

def search_keywords(text, automaton):
    matches = set()
    for end_index, keyword in automaton.iter(text.lower()):
        start_index = end_index - len(keyword) + 1
        matches.add(keyword)
    return matches

def process_images_in_directory(input_directory):
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_directory, filename)
            output_text_file = os.path.splitext(filename)[0] + ".txt"

            text_file_path = extract_text_from_image(image_path, output_text_file)

            if text_file_path:
                with open(text_file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    found_keywords = search_keywords(content, keyword_automaton)
                    for keyword in found_keywords:
                        move_to_folder(image_path, keyword, input_directory)

if __name__ == "__main__":
    clear_terminal()

    desktop_path = os.path.expanduser("~/Desktop")
    input_directory = os.path.join(desktop_path, "Ai")

    keywords = ["Cancer", "Fever", "Asthma"]  
    keyword_automaton = build_automaton(keywords)

    start_time = time.time()
    process_images_in_directory(input_directory)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Processing completed in {elapsed_time:.2f} seconds.")
