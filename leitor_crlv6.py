from tkinter import filedialog 
import TEXTOPDF as topdf
from GETSCRV import *
from get_pdfs import pdfGet
import pandas as pd
import datetime
import os
import csv
import time
import pyautogui as gui
import requests
import json
import logging
import PyPDF2


def ini_crlv_pdf(imprimir=False): # Ativado por botão em "gui_novo.py"
    if not os.path.exists('Planilhas'):
        os.makedirs('Planilhas') # Se não existir pasta "Planilhas", será criada
    contador = 0
    text = ""
    df_final = pd.DataFrame() # Cria um dataframe final
    dia_atual = str(datetime.datetime.now()).split()[0] # Pega a data atual
    Lista_pdfs = "" 
    dt_erro = pd.DataFrame() # Cria um dataframe para erro
    diretorio = filedialog.askdirectory() # Você escolhe o diretório
    d = diretorio.split('/')
    Lista_pdfs = pdfGet(diretorio) # Lê os diretórios da pasta "diretorio" usando o Get_pdfs.py
    total = len(Lista_pdfs) # Conta quantos diretórios tem em "Lista_pdfs"
    print ("".join(["\nEncontrada os seguintes pdfs: ",str(Lista_pdfs)]))
    print ("".join(["\nTotal de ",str(total)," pdfs encontrados"]))
    print ("\nIniciando Processo de leitura de pdfs...")
    placa = ""
    

    def requisicao(): # Requisição de acesso a API do portal do cliente
        print('---------REQUISIÇÃO------------')
        teste = False # Mudar quando necessário
        
        payload = {
            "usuario": "integracaocrlv@grupovamos.com.br",
            "senha": "7DArxWCzvqMj6pG"
        }
    
        headers = {'Content-Type': 'application/json'}
        
        if teste == True:
            response = requests.post('https://gamapldigitalmobapihmlg.azurewebsites.net/api/loginpdc/integracao', headers=headers, json=payload)
        else:
            response = requests.post('https://gamacheckapi.azurewebsites.net/api/loginpdc/integracao', headers=headers, json=payload)
    
        if response.status_code == 200:
            url_cliente = response.url
            print("URL do cliente:", url_cliente)
            print('A API SE CONECTOU COM SUCESSO', response.status_code)
        else:
            print('---------------------------------------------')
            print("Erro ao acessar a URL:", response.status_code)
            print("ERRO AO TENTAR SE CONECTAR COM A API:", response.status_code)
            return None
        
        print('--------RESPONSE--------')
        print(response.text)
    
        return response.json()['accessToken']
    
    
    
    def api(token, dados, filename, filepath, placa): # Subindo os dados para o portal do cliente pela API

        teste = False # Mudar quando necessário
        
        try:
            with open(filepath, 'rb') as file:
                file_content = file.read()
                if not file_content:
                    print("O arquivo está vazio.")
                    return
        except Exception as e:
            print("Erro ao ler o arquivo PDF:", e)
            return
        
        
        # url = 'https://gamapldigitalmobapihmlg.azurewebsites.net/api/crlv' # HOMOLOGAÇÃO
        url = 'https://gamacheckapi.azurewebsites.net/api/crlv' # PRODUCAO
   
        print('---------------------DADOS DO JSON-------------------------')
        print(dados) # PRINT DOS DADOS

        
        files=[
            ('arquivo',(f'{placa}.pdf', open(filepath, 'rb'), 'application/pdf'))  
            ]
        headers = {
            'Authorization': f'Bearer {token}',
            # 'Content-Type': 'application/json'
        }
        payload = {"json" :json.dumps(dados)}
        if teste == True:
            response = requests.request("POST", url, headers=headers, data=payload, files=files) # Homologação
        else:
            response = requests.request("POST", url, headers=headers, data=payload, files=files)  # Producao
    
        print('--------RESPONSE--------')
        print(response.status_code)
        print(response.text)
        print('----HEADERS---')
        print(headers)
    
    dados_api = [] # LISTA DOS DADOS DA API
    token = requisicao()  # Obter o token fora do loop
    for i in Lista_pdfs:
        try:
            print('-----DIRETORIO-----')
            print(diretorio)
            print('-----I-----')
            print(i)
            print("".join([str(diretorio), '/', str(i)]))
            
            text = topdf.convert_pdf_to_string("".join([str(diretorio), '/', str(i)])) 
            
            if imprimir == True:
                print(text)
                return
            
            dados = { # Definir os dados dentro deste loop
                "Placa": getPlaca(text),
                "Chassi": getChassi(text),
                "CNPJ": '75541835000158',
                "Renavam": getRenavam(text),
                "Cor": getCOR(text),
                "ModeloAno": getAnoModelo(text),  
                "Categoria": getCategoria(text),
                "Carroceria": getCarroceria(text),
                "Proprietario": getNome(text),  
                "Local":  getLocal(text),
                "Data": getData(text),
                "CRVNum": getCRV(text),  
                "Tipo": getTipo(text),
                "Modelo": getModelo(text),
                "AnoFabricacao": getAnoModelo(text),
                "diretorio.": f'C:\\Users\gvm.indicadores\\JSL SA\Grupo Vamos - Indicadores - Documentação CRLV - Documentação CRLV\ABC\\{getPlaca(text)}.pdf'
            }

            api(token, dados, i, f'{diretorio}/{i}', getPlaca(text))
            print('----FOI----')
            print('---------------API---------------')
            print(api)
            
            def dados_csv(): # Transformando os crlvs não planilhados em csv
                with open('dados.csv', 'a', newline='') as diretorio_csv:
                    escritor_csv = csv.writer(diretorio_csv)
                    valores_string = [str(valor) for valor in dados.values()]
                    escritor_csv.writerow(valores_string) 
            
            try:
                print('------------------------------------------------------------------------------')
                print('TRANSFORMANDO diretorio EM CSV...')
                dados_csv()
            except:
                print('---------ERRO---------')
                
            with open('dados.csv', 'r') as diretorio_csv: # Corrigir a leitura do arquivo CSV
                    leitor_csv = csv.reader(diretorio_csv)
                    df_csv = pd.DataFrame(leitor_csv)
                    
            df_csv.columns = dados.keys() 
            
            contador += 1
            progresso = round((contador / total) * 100, 2)
            print("".join([str(contador), " de ", str(total), "  ", str(progresso), "% concluido"]))
            if contador % 500 == 0:
                try:
                    df_final.to_excel('Planilhas/' + dia_atual + f'.xlsx')
                except:
                    pass
                
            df_final = pd.concat([df_final, df_csv])  # Adiciona os dados ao DataFrame final
 
        except Exception as e:
            contador += 1
            print("".join(["ERRO NO diretorio '", str(i), f"': {e}, continuando."]))
            df_temp = pd.DataFrame()
            df_temp["diretorio"] = [i]
            dt_erro = pd.concat([dt_erro, df_temp])
            progresso = round((contador / total) * 100, 2)
            if contador % 500 == 0:
                try:
                    df_final.to_excel('Planilhas/' + dia_atual + f'.xlsx')
                except:
                    pass
            print("".join([str(contador), " de ", str(total), "  ", str(progresso), "% concluido"]))
            
    dt_erro.to_excel('Planilhas/' + dia_atual + '-Erros.xlsx')
    print(df_final)
    df_final.to_excel('Planilhas/' + dia_atual + '-Final.xlsx')
    print('--------TODOS OS CRVLS FORAM PLANILHADOS COM SUCESSO!--------')
