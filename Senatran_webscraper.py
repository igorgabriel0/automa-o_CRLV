import time
import pyautogui
import pyperclip
import pandas as pd
from tkinter.filedialog import askopenfilename
import os
import webbrowser
from GETSCRV import *
import TEXTOPDF as topdf



class WebScraper:
    
    def __init__(self):
        self.combined_data = pd.DataFrame(columns=['Modelo', 'Placa', 'ID'])
    
    def run(self,pages):
        self.abrir_console()
        total_time = 0
        total_rows = 0
    
        for i in range (0,pages):
            try:
                dados = self.copiar_conteudo()
                dados = self.clean_string(dados)
                dt = self.create_data_set(dados)
                self.combined_data = self.combined_data.append(dt, ignore_index=True)
                self.go_to_next_page()
                total_rows += len(dt)
                total_time += 4 + 2 + 3 + len(dt) * (3 + 4 + 4 + 2 + 0.5)  # estimated time for each step
                progress = (i + 1) / pages
                remaining_time = total_time * (1 - progress) / progress
                print(f"Processed page {i+1} of {pages} ({progress:.2%}), estimated time remaining: {remaining_time:.2f} seconds")
                self.get_download(dt)
                self.voltar_listagem()
            except:
                print(f"Index Error, on page {i}")
        self.combined_data.to_csv('my_dataset.csv', index=False)

    def voltar_listagem(self):
        pyautogui.typewrite("window.location.href = 'https://portalservicos.senatran.serpro.gov.br/#/veiculos/meus-veiculos'")
        pyautogui.press('enter')

    def export_excel(self, dt, directory):
            nome_planilha = "Senatram"
            data_to_excel = pd.ExcelWriter(directory+"/"+nome_planilha+".xlsx", engine='xlsxwriter')
            dt.to_excel(data_to_excel, sheet_name='sheet1', index=False)
            data_to_excel.save()
            print("\nExportado com sucesso para o Excel!")
            print("".join(["Nome do arquivo gerado: '", nome_planilha, ".xlsx'"]))

    def copiar_conteudo(self):
        time.sleep(4)
        pyautogui.typewrite('copy(document.body.innerText);')
        pyautogui.press('enter')
        time.sleep(2)
        console_output = pyperclip.paste()
        
        return console_output
    def ir_para_veiculo(self, link):
        time.sleep(4)
        pyautogui.typewrite(link)
        pyautogui.press('enter')
        time.sleep(2)
    def abrir_console(self):
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'shift', 'j')
    def limpar_console(self):
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'l')
    def clean_string(self, string):
        lines = string.split('\n')
        # Find the index of the first line that contains the word "Filtrar"
        index = next((i for i, line in enumerate(lines) if 'Filtrar' in line), None)
        # If the word "Filtrar" was found, delete all lines before it
        if index is not None:
            lines = lines[index+1:]
        # Join the remaining lines back into a string
        new_string = '\n'.join(lines)
        lines = new_string.split('\n')
        # Remove the last 4 lines
        linhas_filtradas = lines[:-13]
        # Re-join the remaining lines into a new string
        new_string = '\n'.join(linhas_filtradas)
        return(new_string)
    def create_data_set(self, string):
        lines = string.split('\n')
        # Create an empty list to store the data
        data = []
        # Loop through the lines and create a dictionary for each record
        for i in range(0, len(lines), 3):
            record = {}
            record['Modelo'] = lines[i]
            record['Placa'] = lines[i+1]
            record['ID'] = lines[i+2]
            data.append(record)
        # Create a Pandas DataFrame with the data
        df = pd.DataFrame(data)
        df = df.replace('\r', '', regex=True)
        # Save the DataFrame to a CSV file
        #df.to_csv('my_dataset.csv', index=False)

        # Print the DataFrame

        return df

    def create_data_set(self, string,df):
        lines = string.split('\n')
        # Create an empty list to store the data
        data = []
        # Loop through the lines and create a dictionary for each record
        for i in range(0, len(lines), 3):
            record = {}
            record['Modelo'] = lines[i]
            record['Placa'] = lines[i+1]
            record['ID'] = lines[i+2]
            data.append(record)
        # Create a Pandas DataFrame with the data

        #df = pd.DataFrame(data)
        dataframe_aux = pd.DataFrame(data,columns=['Modelo', 'Placa', 'ID'])

        df = pd.concat([df,dataframe_aux])
        df = df.replace('\r', '', regex=True)
        # Save the DataFrame to a CSV file
        #df.to_csv('my_dataset.csv', index=False)

        # Print the DataFrame

        return df

    def adquirir_dados(self,pages,check=True):
        df = pd.DataFrame(columns=['Modelo', 'Placa', 'ID'])
        self.abrir_console()
        total_time = 0
        total_rows = 0

        for i in range (0,pages):
            try:   
                dados = self.copiar_conteudo()
                dados = self.clean_string(dados)
                dt = self.create_data_set(dados,df)
                self.combined_data = pd.concat([dt,self.combined_data])
                if check == True:
                    if i<=3:self.go_to_next_page(str(i+2))    
                else:self.go_to_next_page("5")
                time.sleep(3)
                total_rows += len(dt)
                total_time += 4 + 2 + 3 + len(dt) * (3 + 4 + 4 + 2 + 0.5)  # estimated time for each step

                progress = (i + 1) / pages
                remaining_time = total_time * (1 - progress) / progress

                print(f"Processed page {i+1} of {pages} ({progress:.2%}), estimated time remaining: {remaining_time:.2f} seconds")
            except:
                pass
        try:
            self.combined_data = self.combined_data.drop_duplicates(['Modelo', 'Placa', 'ID'])
            self.combined_data.to_excel("Dados.xlsx")
        except:
            for i in range(100):
                try:
                    self.combined_data.to_excel(f"Dados({i+1}).xlsx")
                    return
                except:
                    pass
                
    def go_to_next_page(self,page_num="7"):
        time.sleep(3)
        pyautogui.typewrite(f'document.getElementsByClassName("page-link")[{page_num}].click()')
        pyautogui.press('enter')

    def pdfGet(dir):
        list = []
        for file in os.listdir(dir):
          # Check whether file is in text format or not
          if file.endswith(".PDF") or file.endswith(".pdf") :
              file_path = f"{file}"
              list.append(str(file_path))
        return (list)
    
    def get_download(self,Dados):
        batch_size = 50
        processados = 0
        total_rows = len(Dados)
        for index, row in Dados.iterrows():
            time.sleep(3)
            placa = row['Placa']
            print('---------------------------------------')
            print(placa)
            id = row['ID']
            print('---------------------------------------')
            print(id)
            pyautogui.typewrite("window.location.href = 'https://portalservicos.senatran.serpro.gov.br/#/veiculos/meus-veiculos'")
            pyautogui.press('enter')
            time.sleep(4)
            # text = "window.location.href = 'https ://portalservicos.senatran.serpro.gov.br/#/veiculos/meus-veiculos/detalhes/" + str(placa) + "/" + str(id) + "/false'"
            # self.ir_para_veiculo(text)
            pyautogui.typewrite("window.location.href = 'https://portalservicos.senatran.serpro.gov.br/#/veiculos/meus-veiculos/detalhes/" + str(placa) + "/" + str(id) + "/false'")
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(5)
            pyautogui.typewrite('document.getElementsByClassName("text-bold")[0].click()')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(2)   
            progress = (index + 1) / total_rows
            print(f"Processed row {index+1} of {total_rows} ({progress:.2%})")
            processados +=1
            if processados % batch_size ==0:
                savestate = Dados.iloc[:index+1]
                savestate.to_excel("Progresso.xlsx")

            #   Mover para pasta certa (MUDAR QUANDO NECESSÁRIO)
            origem = r"C:\Users\gvm.indicadores\Documents\CRLVS"
            caminho = r"C:\Users\gvm.indicadores\JSL SA\Grupo Vamos - Indicadores - Documentação CRLV - Documentação CRLV\PDF Consolidado"
            print(f"\nLENDO {placa}...\n")
            lista_arquivos = os.listdir(caminho)
            for arquivo in lista_arquivos:
                try:
                    os.replace(f"{origem}/{arquivo}", f"{caminho}/{arquivo}")
                    print("MOVIDO") 
                except:
                    pass
        Lista_pdfs = WebScraper.pdfGet(caminho)
        for i in (Lista_pdfs):
          try:
            text = topdf.convert_pdf_to_string("".join([str(caminho),'/',str(i)]))
            ano = getExerc(text)
            print(f"ARQUIVO: {i}")
            if ano >= "2023":
                pasta = "VIGENTE"
            else:
                pasta = "NAO VIGENTE"

            dir_final = r"C:\Users\gvm.indicadores\JSL SA\Grupo Vamos - Indicadores - Documentação CRLV - Documentação CRLV\PDF Consolidado"+f"/{pasta}"
            if not os.path.exists(f'{dir_final}'):
                os.makedirs(f'{dir_final}')
                print(f"PASTA: {pasta} criada")
            else:
                print(f"\nJá existe a pasta {pasta}\n")

            print(f"\nLENDO {i}...\n")
            os.replace(f"{caminho}/{i}", f"{caminho}/{pasta}/{i}")
            print(f"MOVIDO") 

          except Exception as e:
            print(f"\nERRO ARQUIVO: {i} | {e}")
            time.sleep(2)
    
        print("Downloads: Done")         
     
    def adquirir_crlvs(self):
        planilha = askopenfilename()
        time.sleep(1)
        self.abrir_console()
        df = pd.read_excel(planilha, engine = 'openpyxl')
        self.get_download(df)   