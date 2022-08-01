import convertapi

convertapi.api_secret = 'DBuhCGfisLXtWsTg'
convertapi.convert('pdf', {
    'File': '/home/samarth/learningProject/resumes/Screenshot (44).png'
}, from_format = 'png').save_files('/home/samarth/learningProject/pdfs')