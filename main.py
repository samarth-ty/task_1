import cv2
import pytesseract
import re

EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
LINKEDIN_REG = re.compile(r'((http(s?)://)*([www])*\.|[linkedin])[linkedin/~\-]+\.[a-zA-Z0-9/~\-_,&=\?\.;]+[^\.,\s<]')

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

# def convertImgToTxt(path):
#     pass
tessdata_dir_config= r'/--tessdata-dir "/home/samarth/learningProject/dj_env/lib/python3.8/site-packages/"'
img = cv2.imread('/home/samarth/learningProject/upscaledimg.png')
text = pytesseract.image_to_string(img, config=tessdata_dir_config)
print(text)
emails = extract_emails(text)
phone_number = extract_phone_number(text)
linkedIn = extract_linkedIn(text)
if emails:
    print(emails[0])
# if linkedIn:
print(linkedIn)

print(phone_number)
