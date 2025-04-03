import pdfplumber
import pandas as pd
import zipfile
import os

def extract_table_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
                
        for page_num in range(2, len(pdf.pages)):  
            page = pdf.pages[page_num]
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)
        
        full_table = pd.concat(all_tables, ignore_index=True)
    
    return full_table

def replace_abbreviations(df):
    df.columns = df.columns.str.replace('OD', 'Odontologia', regex=False)
    df.columns = df.columns.str.replace('AMB', 'Ambulatório', regex=False)
    return df

# Função para salvar a tabela em um arquivo ZIP
def save_table_to_zip(df, zip_path, csv_filename):
    temp_csv_path = os.path.join(os.path.dirname(zip_path), csv_filename)
    df.to_csv(temp_csv_path, index=False)
    print(f"CSV salvo em {temp_csv_path}")
    
    # Criar o arquivo ZIP e adicionar o CSV
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(temp_csv_path, csv_filename)
        print(f"CSV foi adicionado ao ZIP: {zip_path}")
    
    # Remover o arquivo CSV temporário após adicionar ao ZIP
    os.remove(temp_csv_path)
    print(f"Arquivo CSV temporário removido: {temp_csv_path}")

pdf_path = 'Web_Scraping/anexos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf'

zip_output_path = 'Teste_fabio_spindola.zip'
csv_filename = 'rol_procedimentos.csv'

# Extrair a tabela e salvar em ZIP
table_df = extract_table_from_pdf(pdf_path)
table_df = replace_abbreviations(table_df)
save_table_to_zip(table_df, zip_output_path, csv_filename)

