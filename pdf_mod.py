# -*- coding: utf-8 -*-
import pymupdf # PyMuPDF
'''
remove some text and replace some text in a PDF file
'''

def remove_text(pdf_path, params, output_path):
    text_to_remove = params["text_to_remove"]
    text_to_remove2 = params["text_to_remove2"]
    text_to_replace = params["text_to_replace"]
    replacement_text = params["replacement_text"]
    doc = pymupdf.open(pdf_path)

    for page in doc:
        # remove text1
        areas = page.search_for(text_to_remove)
        for area in areas:
            expanded_area = pymupdf.Rect(area.x0-90, area.y0, area.x1+30, area.y1 + 20)  # Adjust the 5 value as needed
            page.add_redact_annot(expanded_area)
        page.apply_redactions()

        areas = page.search_for(text_to_remove2)
        for area in areas:
            expanded_area = pymupdf.Rect(area) 
            page.add_redact_annot(expanded_area)
        page.apply_redactions()


        font_name = "MicrosoftYaHei-Bold"

        # change  text
        areas = page.search_for(text_to_replace)
        for area in areas:
            font_info = page.get_text("dict", clip=area)["blocks"][0]["lines"][0]["spans"][0]
            font_name = font_info["font"]
            font_size = font_info["size"]

            # Step 2: Add redaction annotation
            #page.add_redact_annot(area,replacement_text,fontname=new_font)
            page.add_redact_annot(area)
            page.apply_redactions()
            page.insert_text(area.bl, replacement_text, fontname=font_name,fontsize=font_size, fontfile='font/msyhbd.ttc')  # Adjust size as needed

            
        #for drawing in page.get_drawings():
        #    if drawing["type"] == "l":
        #        pass
        #    if drawing["type"] == "l" and drawing["rect"].height <= 2:  # Likely an underline
        #        # Create a white rectangle to cover the underline
        #        page.draw_rect(drawing["rect"], color=(1, 1, 1), fill=(1, 1, 1))
    
    doc.save(output_path)
    doc.close()

# Usage
to_remove = "Machine Translated by Google"
params = {
    "text_to_remove": to_remove,
    "text_to_replace": "Autonomous Survey Technology",
    "replacement_text": "切断脐带的自主调查技术:",
    "text_to_remove2": "Cutting the Umbilical"

}

#remove_text("data/t2.pdf", params, "output/output2.pdf")
remove_text("data/海自の「新型艦」必要性に疑問符「その仕事、無人機でよくね？」 実は“全然ちがう役割”の可能性も!_（乗りものニュース） - Yahoo!ニュース.pdf", params, "output/output2.pdf")
