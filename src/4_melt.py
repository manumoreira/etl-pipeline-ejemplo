import pandas as pd
import yaml
import os

def load_config(path='config/codebook.yml'):
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def melt_multiple_choice():
    config = load_config()
    input_path = 'data/interim/encuesta_limpia.csv'
    output_path = 'data/processed/encuesta_preg_mult.csv'
    
    df = pd.read_csv(input_path)
    
    if 'multiple_choice' not in config:
        return

    melted_dfs = []
    
    for col, meta in config['multiple_choice'].items():
        if col in df.columns and 'id_encuesta' in df.columns:
            separator = meta['separator']
            valid_options = meta['options']
            
            temp_df = df[['id_encuesta', col]].copy().dropna(subset=[col])
            
            # Normalizar separadores y dividir en listas
            temp_df[col] = temp_df[col].str.replace(r',\s*', separator, regex=True)
            temp_df[col] = temp_df[col].str.split(separator)
            
            # Expandir las listas en múltiples filas
            exploded_df = temp_df.explode(col)
            exploded_df[col] = exploded_df[col].str.strip()
            
            # Filtrar opciones no válidas (ruido)
            exploded_df = exploded_df[exploded_df[col].isin(valid_options)]
            
            exploded_df = exploded_df.rename(columns={col: 'opcion_seleccionada'})
            exploded_df['pregunta'] = col
            
            melted_dfs.append(exploded_df)

    if melted_dfs:
        final_long_df = pd.concat(melted_dfs, ignore_index=True)
        final_long_df = final_long_df[['id_encuesta', 'pregunta', 'opcion_seleccionada']]
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        final_long_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Datos despivotados guardados en {output_path}")

if __name__ == '__main__':
    melt_multiple_choice()