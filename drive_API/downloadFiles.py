from pdfminer.high_level import extract_text
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import convertapi
import cv2
import pytesseract


gauth = GoogleAuth()
drive = GoogleDrive(gauth)

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

def write_to_gsheet(folder_id, filename, phone, email):
    Scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

    creds = ServiceAccountCredentials.from_json_keyfile_name("/home/samarth/learningProject/drive_API/secret_key.json", scopes=Scopes)
    file = gspread.authorize(creds)
    workbook = file.open("Candidates information")
    sheet = workbook.sheet1
    candidate_info = [folder_id, filename, phone, email, 'https://www.linkedin.com/in/sam-tyagi-6b6487245/']
    sheet.append_row(candidate_info)


def convert_to_pdf(file_path, typ):
    convertapi.api_secret = 'DBuhCGfisLXtWsTg'
    convertapi.convert('pdf', {
        'File': file_path
    }, from_format = typ).save_files('/home/samarth/learningProject/drive_API')


folder = '1CyGmVF4JxVTEte47PtYrYjyGjYv5Oc5H'

# Upload files
# directory = "D:/pyGuru/Youtube/Google services/Google drive backup/data"
# for f in os.listdir(directory):
# 	filename = os.path.join(directory, f)
# 	gfile = drive.CreateFile({'parents' : [{'id' : folder}], 'title' : f})
# 	gfile.SetContentFile(filename)
# 	gfile.Upload()

# Download files
file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
for index, file in enumerate(file_list):
	# print(index+1, 'file downloaded : ', file['title'])
    folder_id = file['id']
    print('folder id: ', file['id'])
    fl = drive.ListFile({'q' : f"'{folder_id}' in parents and trashed=false"}).GetList()
    for f in fl:
        # print(f['title'], f['id'])
        length = len(f['title'])
        typ = ''
        for i in range(length-1,-1,-1):
            if f['title'][i] == '.':
                break
        typ = f['title'][i+1:]
        if typ == 'pdf':
            text = extract_text(f['title'])
            # print(text)
            emails = extract_emails(text)
            phone_number = extract_phone_number(text)
            linkedIn = extract_linkedIn(text)
            if emails:
                print(emails[0])
            print(phone_number)
            write_to_gsheet(folder_id,f['title'], phone_number, emails[0])
        elif typ == 'docx' or typ == 'doc':
            convert_to_pdf(f['title'], typ)
            # l = len(f['title'])
            # upto_dot = 0
            # for i in range(l-1,-1,-1):
            #     if f['title'][i] == '.':
            #         upto_dot = i
            #         break
            converted_file_path = f['title'][:i+1] + 'pdf'
            text = extract_text(converted_file_path)
            emails = extract_emails(text)
            phone_number = extract_phone_number(text)
            linkedIn = extract_linkedIn(text)
            if emails:
                print(emails[0])
            print(phone_number)
            if emails and phone_number:
                write_to_gsheet(folder_id, f['title'], phone_number, emails[0])
        elif typ in ['png', 'jpeg', 'jpg']:
            tessdata_dir_config= r'/--tessdata-dir "/home/samarth/learningProject/dj_env/lib/python3.8/site-packages/"'
            img = cv2.imread(f['title'])
            text = pytesseract.image_to_string(img, config=tessdata_dir_config)
            emails = extract_emails(text)
            phone_number = extract_phone_number(text)
            linkedIn = extract_linkedIn(text)
            if emails:
                print(emails[0])
            print(phone_number)

            if emails and phone_number:
                write_to_gsheet(folder_id, f['title'], phone_number, emails[0])



    print('----------------------------------------------------------------------------------')
    # for i,f in enumerate(fl):
    #     print(f['title'], f['id'])

	# file.GetContentFile(file['title'])