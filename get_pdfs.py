import os

# Le os arquivos da pasta, é usado em "leitor_crlv.py"

def pdfGet(dir):
  list = []
  for file in os.listdir(dir):
    # Check whether file is in text format or not
    if file.endswith(".PDF") or file.endswith(".pdf") :
        file_path = f"{file}"
        list.append(str(file_path))
  return (list)

