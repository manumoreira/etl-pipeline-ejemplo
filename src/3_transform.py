import pandas as pd
import yaml
import os

def load_config(path='config/codebook.yml'):
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def transform_data():
    config = load_config()
    
    input_path = 'data/interim/encuesta_limpia.csv'
    output_path = 'data/processed/encuesta_procesada.csv'
    
    print(f"Leyendo datos limpios desde {input_path}...")
    df = pd.read_csv(input_path)
    
    # 1. Recodificación de valores (Categóricas y Likert a Numéricas)
    if 'value_mappings' in config:
        for col, mapping in config['value_mappings'].items():
            if col in df.columns:
                # Creamos una nueva columna con el sufijo '_cod' para no perder el dato original
                df[f"{col}_cod"] = df[col].map(mapping)
    
    # 2. Procesamiento de Preguntas de Respuesta Múltiple (One-Hot Encoding)
    if 'multiple_choice' in config:
        for col, meta in config['multiple_choice'].items():
            if col in df.columns:
                separator = meta['separator']
                prefix = meta['prefix']
                valid_options = meta['options']
                
                # Manejar valores nulos para evitar errores al hacer split
                df[col] = df[col].fillna("")
                
                for option in valid_options:
                    # Normalizar el nombre de la nueva columna (minúsculas, reemplazar espacios)
                    import unicodedata
                    clean_option = unicodedata.normalize('NFKD', option).encode('ASCII', 'ignore').decode('utf-8')
                    col_name = f"{prefix}_{clean_option.lower().replace(' ', '_')}"
                    
                    # Asignar 1 si la opción exacta está en la lista de respuestas separadas, 0 si no
                    df[col_name] = df[col].apply(lambda x: 1 if option in [item.strip() for item in x.split(separator)] else 0)
    
    # Las preguntas abiertas definidas en 'open_answer' se mantienen intactas en sus columnas originales
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Datos transformados guardados en {output_path}")
    print(f"Total de columnas finales: {len(df.columns)}")

if __name__ == '__main__':
    transform_data()