from PIL import Image
import pytesseract
import os
import shutil
import requests
from bs4 import BeautifulSoup

def clear_terminal():
    # Clear terminal for macOS
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

def fetch_disease_keywords():
    # Web scraping to get a list of medical conditions from Wikipedia
    url = "https://en.wikipedia.org/wiki/List_of_medical_conditions"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        keywords = [link.text.lower() for link in soup.find_all('a') if link.get('href') and "/wiki/" in link.get('href')]
        return keywords
    else:
        print(f"Failed to fetch keywords. Status code: {response.status_code}")
        return []

def identify_disease(text, keywords):
    for keyword in keywords:
        if kmp_search(text.lower(), keyword.lower()):
            return keyword

    return None

def process_images_in_directory(input_directory, keywords):
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_directory, filename)
            output_text_file = os.path.splitext(filename)[0] + ".txt"

            text_file_path, text = extract_text_from_image(image_path, output_text_file)

            if text_file_path and text:
                disease = identify_disease(text, keywords)
                if disease:
                    output_folder = os.path.join(input_directory, disease)
                    move_to_folder(image_path, output_folder)

if __name__ == "__main__":
    desktop_path = os.path.expanduser("~/Desktop")
    input_directory = os.path.join(desktop_path, "Ai")  # Change this to your input directory

    # Fetch disease keywords from the internet (Wikipedia)
    disease_keywords = fetch_disease_keywords()

    if disease_keywords:
        process_images_in_directory(input_directory, disease_keywords)
    else:
        print("No disease keywords fetched. Exiting.")
