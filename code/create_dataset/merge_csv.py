import pandas as pd
import os

directory = './headers_n_abstracts'
all_files = os.listdir(directory)

combined_df = pd.DataFrame()

for file in all_files:
    if file.endswith('.csv'):
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)
        combined_df = pd.concat([combined_df, df])

combined_df.to_csv('header_abstract_final.csv', index=False)
