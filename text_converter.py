from PIL import Image
import pytesseract
import os
import shutil
import platform

def clear_terminal():
    # Clear terminal for macOS
    os.system("clear")
clear_terminal()
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

def move_to_folder(image_path, output_folder):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        shutil.move(image_path, os.path.join(output_folder, os.path.basename(image_path)))
        print(f"Image file moved to {output_folder}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    desktop_path = os.path.expanduser("~/Desktop")
    image1_path = os.path.join(desktop_path, "Ai", "sample1.png")
    image2_path = os.path.join(desktop_path, "Ai", "sample2.png")
    output_folder1 = os.path.join(desktop_path, "Ai", "cancer")
    output_folder2 = os.path.join(desktop_path, "Ai", "fever")

    # Extract text from the first image
    text_file1_path = extract_text_from_image(image1_path, "sample1.txt")

    if text_file1_path:
        with open(text_file1_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if "cancer" in content:
                move_to_folder(image1_path, output_folder1)
            if "Fever" in content:
                move_to_folder(image1_path, output_folder2)

    # Extract text from the second image
    text_file2_path = extract_text_from_image(image2_path, "sample2.txt")

    # Check for keywords and move the image to the appropriate folder
    
    if text_file2_path:
        with open(text_file2_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if "cancer" in content:
                move_to_folder(image2_path, output_folder1)
            if "Fever" in content:
                move_to_folder(image2_path, output_folder2)
