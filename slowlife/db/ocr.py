import pytesseract
import re
from PIL import Image

# The following line is for Windows users only. You may need to change the path below depending
# on the path of your Tesseract OCR installation.
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Open the image file
image = Image.open('../resources/ss/data/generated/building/apothecary.png')

# Convert the image to grayscale
image = image.convert("L")

# Perform OCR on the image
text = pytesseract.image_to_string(image)

# Print the extracted text to the console
print(text)

# 1. Earnings is in the row with Earnings:
pattern = re.compile(r'.*{type}.*\+([0-9].*)%', re.IGNORECASE)

types = ['Inspiring', 'Diligent', 'Brave', 'Informed', 'Unfettered']
pos = []
for line in text.splitlines():
    print(f'Checking line: [{line}]')
    for typ in types:
        pattern = re.compile(r'{type}', re.IGNORECASE)
        result = re.search(pattern, line)
        if result is not None:
            print(line, result, '||', result.groups(), '||', result.group(result.lastindex))
            pos[typ] = result.group(result.lastindex)

# Total unlocked skills: 681
# ‘@ Inspiring Building Earning Bonus +4593%
# ‘@ Diligent Building Earning Bonus +4776%
# @Brave Building Earning Bonus +4658%
#
# @ Informed Building Earning Bonus +4746%
# @ Unfettered Building Earning Bonus +4604%

# Parse last number
