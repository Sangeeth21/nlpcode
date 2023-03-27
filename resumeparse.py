import os
import PyPDF2
#import docx

# function to extract text from a PDF file
def extract_text_from_pdf(filename):
    with open(filename, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

# function to extract text from a DOCX file
# def extract_text_from_docx(filename):
#     doc = docx.Document(filename)
#     text = ''
#     for para in doc.paragraphs:
#         text += para.text + '\n'
#     return text

# function to write the extracted text to a file
def write_text_to_file(text, filename):
    with open(filename, 'w',encoding="utf-8") as file:
        file.write(text)

# main function to extract text from files and write to a file
def extract_text_and_write_to_file(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(os.path.join(input_dir, filename))
        # elif filename.endswith('.docx'):
        #     text = extract_text_from_docx(os.path.join(input_dir, filename))
        else:
            continue
        write_text_to_file(text, os.path.join(output_dir, os.path.splitext(filename)[0] + '.txt'))

# example usage
input_dir = './input_dir'
output_dir = './output_dir'
extract_text_and_write_to_file(input_dir, output_dir)