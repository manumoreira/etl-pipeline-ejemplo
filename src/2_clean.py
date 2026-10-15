import pandas as pd
import yaml
import os

def load_config(path='config/codebook.yml'):
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def clean_data():
    config = load_config()
    input_path = 'data/raw/encuesta_cruda.csv'
    output_path = 'data/interim/encuesta_limpia.csv'
    
    df = pd.read_csv(input_path)
    df = df.rename(columns=config['column_mappings'])
    
    if 'fecha_encuesta' in df.columns:
        df['fecha_encuesta'] = pd.to_datetime(df['fecha_encuesta'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    
    if 'edad' in df.columns:
        df['edad'] = df['edad'].astype(str).str.extract(r'(\d+)')[0]
        df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
        
    text_cols = df.select_dtypes(include=['object', 'string']).columns
    for col in text_cols:
        if col not in ['id_encuesta', 'sugerencias_soluciones', 'problemas_principales']:
            df[col] = df[col].str.strip().str.capitalize()
        else:
            df[col] = df[col].str.strip()

    df = df.dropna(how='all')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8')
    print("Datos limpios y normalizados guardados en data/interim.")

if __name__ == '__main__':
    clean_data()