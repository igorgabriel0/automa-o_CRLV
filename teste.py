from tkinter import Tk, PhotoImage, Label, Frame, Button
from a import info, baixa
from leitor_crlv6 import ini_crlv_pdf
import os
from crlv_snowflake_final import snow_flake_api

root = Tk()
root.title("Aplicativo de Apoio Vamos")
root.geometry("350x350")
bg = PhotoImage(file="vamo3.png")
root.configure(bg="white")
label = Label(root, image=bg)
label.pack() 
frame = Frame(root, background="white")
frame.pack(pady=10)  
botao1 = Button(frame, text="ADQUIRIR INFOS - PLACA", command=info)
botao2 = Button(frame, text="BAIXAR - CRLV", command=baixa)
botao3 = Button(frame, text="Planilhar CRLVs - PDFS", command=ini_crlv_pdf)
botao4 = Button(frame, text="SUBIR PARA SNOW FLAKE", command=snow_flake_api)
imagem = PhotoImage(file="vamo3.png")
botao1.grid(row=0, column=0, padx=3, pady=3)
botao2.grid(row=1, column=0, padx=3, pady=3)    
botao3.grid(row=2, column=0, padx=3, pady=3)
botao4.grid(row=3, column=0, padx=3, pady=3)


root.mainloop()
