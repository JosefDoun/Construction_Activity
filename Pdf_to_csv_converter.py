import os, tabula

folder_contents = os.listdir()

for file in folder_contents:
    if file.endswith('.pdf'):
        tabula.convert_into(file, file.split('.')[0] + '.csv', pages = 'all')

