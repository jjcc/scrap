import json
import os
import re
from helper.common import kw2b_en, kw2b_fr, kw2b_jp, kw2b_ge,kwc, news
'''
collect information about the pdfs, and rename them
'''


def build_mapping():
    kw_list = {"en":kw2b_en, "fr":kw2b_fr,"ge":kw2b_ge,"jp":kw2b_jp }
    mapping = {}
    for lang in kw_list.keys():
        kw2b = kw_list.get(lang)
        kwc_list = [k.strip() for k in  kwc.split(",")]
        kw2b_list = [k.strip() for k in  kw2b.split(",")]
        kw_pair = zip(kwc_list,kw2b_list)

        mapc2b = {k:v for k,v in kw_pair}
        kw_pair = zip(kwc_list,kw2b_list)
        mapb2c = {v:k for k,v in kw_pair}
        lang_mapping = {"c2b":mapc2b,"b2c":mapb2c}

        mapping[lang] = lang_mapping
    return mapping

def get_file_info(filename):
    # map 'en_and Reconnaissance news_6.pdf' to 'en','and Reconaissance', 'news', 6
    pattern = r'^(\w+)_(.+?)\s(\w+)_(\d+)\.pdf$'
    match = re.match(pattern, filename)
    if match:
        language_code, title, category, number = match.groups()
        #print(f"Language Code: {language_code}")
        #print(f"Title: {title}")
        #print(f"Category: {category}")
        #print(f"Number: {number}")
    else:
        print("No match found")
        return None, None, None, None
    
    return language_code, title, category, number

mapping = build_mapping()
#with open("output/mappiong.json", 'w', encoding='utf-8') as f:
#    json.dump(mapping, f, indent=4)

for dirpath, dirnames, filenames in os.walk("output/trans"):
    for filename in filenames:
        if not filename.endswith(".pdf"):
            continue
        l,t, c, n = get_file_info(filename)
        lang_mapping = mapping.get(l)
        kwc = lang_mapping.get("b2c").get(t)
        print(kwc)
        print(f"Language: {l}, Title: {t}, Category: {c}, Number: {n}")
        new_filename = f"{l}_{kwc}_{n}.pdf"
        os.rename(f"output/trans/{filename}", f"output/trans/{new_filename}")
#fn = "en_Anti-Amphibious Landing Defenses news_6.pdf"
#l,t, c, n = get_file_info(fn)
#
#lang_mapping = mapping.get(l)
#kwc = lang_mapping.get("b2c").get(t)
#print(kwc)
#print("end")





print(l,t,c,n)
#mapping = build_mapping()
