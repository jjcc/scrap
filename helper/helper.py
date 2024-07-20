import os
import pymupdf

def convert_oxps_to_pdf(input_file, output_file):
    # Open the OXPS file
    doc = pymupdf.open(input_file)
    
    # Convert to PDF
    pdf_bytes = doc.convert_to_pdf()
    
    # Open the PDF bytes as a new document
    pdf_doc = pymupdf.open("pdf", pdf_bytes)
    
    # Save the PDF
    pdf_doc.save(output_file)
    
    # Close both documents
    doc.close()
    pdf_doc.close()


if __name__ == "__main__":

    walk = os.walk("output")
    for root, dirs, files in walk:
        for file in files:
            if file.endswith(".oxps"):
                input_oxps = os.path.join(root, file)
                output_pdf = os.path.join(root, file.replace(".oxps", "a.pdf"))
                convert_oxps_to_pdf(input_oxps, output_pdf)