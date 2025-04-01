import requests
from bs4 import BeautifulSoup
import os

# URL da página da ANS
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Fazendo a requisição HTTP
response = requests.get(url)
response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

# Analisando o conteúdo HTML
soup = BeautifulSoup(response.text, "html.parser")

# Encontrando os links para os anexos
anexos = soup.find_all("a", string=lambda text: text and "Anexo" in text)

# Diretório para salvar os arquivos
output_dir = "anexos"
os.makedirs(output_dir, exist_ok=True)

# Baixando e salvando apenas arquivos PDF
for anexo in anexos:
    anexo_url = anexo["href"]
    if anexo_url.startswith("/"):
        anexo_url = "https://www.gov.br" + anexo_url

    anexo_nome = anexo_url.split("/")[-1]

    # Verificando se o arquivo é um PDF
    if not anexo_nome.lower().endswith(".pdf"):
        print(f"Ignorado: {anexo_nome} (não é um PDF)")
        continue

    anexo_path = os.path.join(output_dir, anexo_nome)

    # Baixando o arquivo
    anexo_response = requests.get(anexo_url)
    anexo_response.raise_for_status()

    # Salvando o arquivo
    with open(anexo_path, "wb") as file:
        file.write(anexo_response.content)
    print(f"Arquivo {anexo_nome} baixado com sucesso para {anexo_path}")
