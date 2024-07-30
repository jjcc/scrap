import os
from pdf2docx import Converter



pdf_file = 'output/trans/en_and Reconnaissance news_6.pdf'
docx_file = 'output/trans/en_and Reconnaissance news_6.docx'

def convert_pdf2docx(pdf_file, docx_file):
    cv = Converter(pdf_file)
    cv.convert(docx_file)      # all pages by default
    cv.close()

for dirpath, dirnames, filenames in os.walk("output/trans"):

    for filename in filenames:
        if not filename.endswith(".pdf"):
            continue
        abs_path = os.path.join(dirpath, filename)
        docx_path = dirpath.replace("trans","docx")
        target_path = os.path.join(docx_path, filename.replace(".pdf",".docx"))
        convert_pdf2docx(abs_path, target_path)
