import re
from pdfminer.high_level import extract_text
 
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
LINKEDIN_REG = re.compile(r'((http(s?)://)*([www])*\.|[linkedin])[linkedin/~\-]+\.[a-zA-Z0-9/~\-_,&=\?\.;]+[^\.,\s<]')

def extract_text_from_pdf(pdf_path):
    # print(extract_text(pdf_path))
    return extract_text(pdf_path)
 
 
def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)


def extract_linkedIn(resume_text):
    return re.findall(LINKEDIN_REG, resume_text)


def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)
 
    if phone:
        number = ''.join(phone[0])
 
        if resume_text.find(number) >= 0 and len(number) < 16:
            return number
    return None
 
 
if __name__ == '__main__':
    text = extract_text_from_pdf('pdfs/test_resume.pdf')
    emails = extract_emails(text)
    phone_number = extract_phone_number(text)
    linkedIn = extract_linkedIn(text)
    print(text)
    if emails:
        print(emails[0])
    # if linkedIn:
    print(linkedIn)

    print(phone_number)