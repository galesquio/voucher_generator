import secrets
import qrcode
import xml.etree.ElementTree as et
from PIL import Image

import os
# Load the SVG file
tree = et.parse('template12.svg')
root = tree.getroot()


def convert_svg_to_pdf(input_svg, output_pdf):
# Construct the command
    inkscape_command = f"inkscape --export-filename={output_pdf} {input_svg}"

    # Execute the command
    os.system(inkscape_command)
    #print(f"Conversion successful! Output saved as {output_pdf}")

def update_gc(qr_, qr_text, code_):
    qr_elem = None
    for elem in root.iter():
        if elem.attrib.get('id') == qr_:
            qr_elem = elem
            break

    # If we found the image, replace it with a new QR code
    if qr_elem is not None:
        # Create a QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Add data to the QR code
        data = 'https://wjvcompany.pythonanywhere.com/wjvgift/default/qrredeem/%s'%code_#"Hello, World!"
        qr.add_data(data)
        qr.make(fit=True)

        # Generate an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image as a temporary file
        temp_filename = '%s.png'%qr_
        img.save(temp_filename)

        # Replace the image element's href attribute with the new image filename
        qr_elem.attrib['{http://www.w3.org/1999/xlink}href'] = temp_filename

    # Find the text element with ID 'qr2_text'
    text_elem = None
    for elem in root.iter():
        if elem.attrib.get('id') == qr_text:
            text_elem = elem
            break

    # If we found the text element, update its value
    if text_elem is not None:
        text_elem.text = code_


######################################################
num_codes = 99
code_length = 9

# Generate the codes in batches of 3
codes = set()
keyword = [['qr1','qr1_text'],['qr2','qr2_text'],['qr3','qr3_text']]
page_ctr = 1
for i in range(0, num_codes, 3):
    batch = []
    while len(batch) < 3:
        code = 'BB' + secrets.token_hex(code_length // 2 + 1)[:code_length - 1]
        batch.append(code.upper())
        codes.add(code.upper())
    for idx, code_ in enumerate(batch):
        key__ = keyword[idx]
        print (code_)
        update_gc(key__[0],key__[1],code_)
    #print ('-------')

    tree.write('output__%s.svg'%page_ctr, encoding='utf-8', xml_declaration=True)
    from_='output__%s.svg'%page_ctr
    write_to='12hours_%s.pdf'%page_ctr
    #svg_file = 'input.svg'
    #pdf_file = 'output.pdf'

    convert_svg_to_pdf(from_, write_to)
    page_ctr+=1