# import pandas as pd
# from scipy.stats import ttest_ind

# # Load the dataset
# data = pd.read_csv('/home/dataset/EDS-1013.gct', sep='\t', skiprows=2)

# # Extract unique subtypes and subtype_4class values
# subtypes = data.loc[data['id'] == 'subtype', :].iloc[0, 4:].dropna().unique()
# subtype_4class = data.loc[data['id'] == 'subtype_4class', :].iloc[0, 4:].dropna().unique()

# # Extract columns corresponding to Basal and Luminal subtypes
# basal_columns = data.columns[data.loc[data['id'] == 'subtype', :].iloc[0] == 'Basal'].tolist()
# luminal_columns = data.columns[data.loc[data['id'] == 'subtype', :].iloc[0] == 'Luminal'].tolist()

# # Convert columns corresponding to Basal and Luminal subtypes to numeric format
# basal_data_numeric = data[basal_columns].apply(pd.to_numeric, errors='coerce')
# luminal_data_numeric = data[luminal_columns].apply(pd.to_numeric, errors='coerce')

# # Retain rows (genes) that don't have NaN values in either Basal or Luminal data
# common_genes = basal_data_numeric.dropna().index.intersection(luminal_data_numeric.dropna().index)
# basal_clean = basal_data_numeric.loc[common_genes]
# luminal_clean = luminal_data_numeric.loc[common_genes]

# # Perform t-test for each gene
# p_values = {}
# for gene in common_genes:
#     t_stat, p_val = ttest_ind(basal_clean.loc[gene], luminal_clean.loc[gene])
#     p_values[gene] = p_val

# # Convert to a pandas Series for easier manipulation
# p_values_series = pd.Series(p_values)

# # Filter genes with p-value < 0.05
# significant_genes = p_values_series[p_values_series < 0.05]

# print(significant_genes)



import pandas as pd
from scipy.stats import ttest_ind

# Load the dataset
data = pd.read_csv('/home/dataset/EDS-1013.gct', sep='\t', skiprows=2)

# Extract unique subtypes and subtype_4class values
subtypes = data.loc[data['id'] == 'subtype', :].iloc[0, 4:].dropna().unique()
subtype_4class = data.loc[data['id'] == 'subtype_4class', :].iloc[0, 4:].dropna().unique()

# Extract columns corresponding to Basal and Luminal subtypes
basal_columns = data.columns[data.loc[data['id'] == 'subtype', :].iloc[0] == 'Basal'].tolist()
luminal_columns = data.columns[data.loc[data['id'] == 'subtype', :].iloc[0] == 'Luminal'].tolist()

# Convert columns corresponding to Basal and Luminal subtypes to numeric format
basal_data_numeric = data[basal_columns].apply(pd.to_numeric, errors='coerce')
luminal_data_numeric = data[luminal_columns].apply(pd.to_numeric, errors='coerce')

# Retain rows (genes) that don't have NaN values in either Basal or Luminal data
common_genes = basal_data_numeric.dropna().index.intersection(luminal_data_numeric.dropna().index)
basal_clean = basal_data_numeric.loc[common_genes]
luminal_clean = luminal_data_numeric.loc[common_genes]

# Perform t-test for each gene
p_values = {}
for gene in common_genes:
    t_stat, p_val = ttest_ind(basal_clean.loc[gene], luminal_clean.loc[gene])
    p_values[gene] = p_val

# Convert to a pandas Series for easier manipulation
p_values_series = pd.Series(p_values)

# Filter genes with p-value < 0.05
significant_genes = p_values_series[p_values_series < 0.05]

# Extract gene symbols for the significant genes
gene_symbols = data.loc[significant_genes.index, 'Name_GeneSymbol']

# Create a dataframe with gene symbols and their corresponding p-values
result_df = pd.DataFrame({
    'GeneSymbol': gene_symbols,
    'p-value': significant_genes.values
})

print(result_df)
