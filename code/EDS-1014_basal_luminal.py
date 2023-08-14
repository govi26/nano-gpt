import pandas as pd
from scipy.stats import ttest_ind

# Load the dataset
data = pd.read_csv("/home/dataset/EDS-1014.gct", sep="\t", skiprows=2)

# Extract the columns that indicate subtype for each sample
subtype = data.iloc[3, 5:].to_dict()
basal_columns = [col for col, subtype_label in subtype.items() if subtype_label == "Basal"]
luminal_columns = [col for col, subtype_label in subtype.items() if subtype_label == "Luminal"]

# Extract gene expression data for Basal and Luminal samples
basal_data = data[basal_columns].iloc[5:].reset_index(drop=True).apply(pd.to_numeric, errors='coerce').dropna()
luminal_data = data[luminal_columns].iloc[5:].reset_index(drop=True).apply(pd.to_numeric, errors='coerce').dropna()

# Perform t-test for each gene
p_values_corrected = []
for index in basal_data.index:
    t_stat, p_val = ttest_ind(basal_data.loc[index], luminal_data.loc[index])
    p_values_corrected.append(p_val)

# Extract gene symbols and create a DataFrame for results
gene_symbols_from_cleaned = data.loc[basal_data.index, "Name_GeneSymbol"]
results_aligned = pd.DataFrame({
    'GeneSymbol': gene_symbols_from_cleaned,
    'P-Value': p_values_corrected
})

# Filter for genes with p-value < 0.05 and remove "na" labels
differentially_expressed_genes_filtered = results_aligned[
    (results_aligned['P-Value'] < 0.05) & 
    (results_aligned['GeneSymbol'] != 'na')
]

print(differentially_expressed_genes_filtered)