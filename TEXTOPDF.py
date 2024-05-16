from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

#Essas linhas importam as bibliotecas necessárias para o processamento de arquivos PDF.

def convert_pdf_to_string(file_path):
    output_string = StringIO()
    # Abre o arquivo PDF como um arquivo binário
    with open(file_path, 'rb') as in_file:
        # Cria um parser para o arquivo PDF
        parser = PDFParser(in_file)
        # Cria um documento PDF a partir do parser
        doc = PDFDocument(parser)
        # Cria um gerenciador de recursos
        rsrcmgr = PDFResourceManager()
        # Cria um conversor de texto
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        # Cria um interpretador de página
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Processa cada página do PDF
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    # Retorna a string contendo o texto do PDF
    return output_string.getvalue()

# Essa função convert_pdf_to_string recebe o caminho do arquivo PDF como entrada e retorna uma string contendo todo o texto do PDF. 
# Ela faz isso abrindo o arquivo PDF, criando um parser para o arquivo, criando um documento PDF, criando um gerenciador de recursos, 
# criando um conversor de texto, criando um interpretador de página e, finalmente, 
# processando cada página do PDF e adicionando o texto resultante à string de saída.
                
def convert_title_to_filename(title):
    # Converte o título para letras minúsculas
    filename = title.lower()
    # Substitui os espaços por underscores
    filename = filename.replace(' ', '_')
    # Retorna o nome de arquivo válido para o título
    return filename

# Essa função convert_title_to_filename recebe um título como entrada e retorna um nome de arquivo válido para esse título. 
# Ela converte o título para letras minúsculas e substitui os espaços por underscores.

def split_to_title_and_pagenum(table_of_contents_entry):
    # Remove quaisquer espaços em branco no início e no final da entrada
    title_and_pagenum = table_of_contents_entry.strip()
    # Inicializa as variáveis de título e número da página como None
    title = None
    pagenum = None
    # Verifica se a entrada não está vazia
    if len(title_and_pagenum) > 0:
        # Verifica se o último caractere da entrada é um dígito
        if title_and_pagenum[-1].isdigit():
            # Encontra o ponto em que o título termina e o número da página começa
            i = -2
            while title_and_pagenum[i].isdigit():
                i -= 1
            # Obtém o título removendo os espaços em branco no início e no final
            title = title_and_pagenum[:i].strip()
            # Obtém o número da página convertendo para inteiro
            pagenum = int(title_and_pagenum[i:].strip())
    return title, pagenum