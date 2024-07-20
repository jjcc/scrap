import pymupdf  # PyMuPDF
import requests
# failure attempt to convert HMTL to PDF
def url_to_pdf(url, output_path):
    # Fetch the HTML content
    response = requests.get(url)
    html_content = response.text

    # Create a new PDF document
    doc = pymupdf.open()

    # Add a new page
    page = doc.new_page()

    # Insert the HTML content into the page
    page.insert_htmlbox(page.rect, html_content)

    # Save the PDF
    doc.save(output_path)
    doc.close()

# Usage
url = "https://www-oedigital-com.translate.goog/news/514718-autonomous-survey-technology-cutting-the-umbilical?_x_tr_sl=auto&_x_tr_tl=zh-CN&_x_tr_hl=en-US&_x_tr_pto=wapp"
output_path = "data/output.pdf"
url_to_pdf(url, output_path)
