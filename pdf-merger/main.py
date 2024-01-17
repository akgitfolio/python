import os
import requests
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

def download_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.basename(url)
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
    else:
        raise ValueError(f"Error fetching PDF from {url}")

def merge_pdfs(pdf_files, output_filename):
    merger = PdfMerger()
    for pdf_file in pdf_files:
        try:
            pdf_path = download_pdf(pdf_file)
            merger.append(pdf_path)
        except ValueError as e:
            print(f"Error downloading {pdf_file}: {e}")
    merger.write(output_filename)
    merger.close()

def add_toc_and_page_numbers(input_pdf, output_pdf, recipes):
    writer = PdfWriter()
    toc_content = "Table of Contents\n\n"
    page_number = 1

    for recipe in recipes:
        toc_content += f"{page_number}. {recipe['title']}\n"
        page_number += len(PdfReader(recipe["url"]).pages)

    writer.add_blank_page()
    writer.pages[0].insert_text(toc_content)

    reader = PdfReader(input_pdf)
    for page in reader.pages:
        writer.add_page(page)

    for i in range(len(writer.pages)):
        writer.pages[i].insert_text(f"Page {i + 1}", position=(500, 10))

    with open(output_pdf, "wb") as f:
        writer.write(f)

dietary_preferences = ["Vegetarian", "Gluten-free"]
ingredients = ["chicken", "tomato", "basil"]
recipe_urls = [
    "https://www.allrecipes.com/recipe/237916/vegetarian-chili/",
    "https://www.inspiredtaste.net/21393/gluten-free-pasta-salad-recipe/",
    "https://food52.com/recipes/80750-spaghetti-pomodoro-with-tomato-and-basil",
]

filtered_recipes = []
for recipe in recipe_urls:
    if all(preference.lower() in recipe.lower() for preference in dietary_preferences):
        if all(ingredient.lower() in recipe.lower() for ingredient in ingredients):
            filtered_recipes.append({"title": os.path.basename(recipe), "url": recipe})

merge_pdfs([recipe["url"] for recipe in filtered_recipes], "merged_recipes.pdf")
add_toc_and_page_numbers("merged_recipes.pdf", "personalized_recipe_book.pdf", filtered_recipes)

print(f"Personalized recipe book created: personalized_recipe_book.pdf")
