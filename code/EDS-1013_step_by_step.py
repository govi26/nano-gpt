# import pandas as pd
# import numpy as np
# from scipy.stats import ttest_ind

# # Load the data
# data = pd.read_csv("/home/dataset/EDS-1013.gct", sep="\t", skiprows=2)

# # Extract the subtype row to identify cell lines classified as Basal or Luminal
# subtype_row = data[data['id'] == "subtype"].iloc[0, 4:]
# basal_cell_lines = subtype_row[subtype_row == "Basal"].index.tolist()
# luminal_cell_lines = subtype_row[subtype_row == "Luminal"].index.tolist()

# # Extract the gene expression data for Basal and Luminal cell lines
# gene_expression_data = data.iloc[5:, :].reset_index(drop=True)
# basal_data = gene_expression_data[["id", "DESCRIPTION"] + basal_cell_lines]
# luminal_data = gene_expression_data[["id", "DESCRIPTION"] + luminal_cell_lines]

# # Convert valid numeric strings to floats and replace non-numeric strings with NaN
# def convert_to_float(value):
#     try:
#         return float(value)
#     except ValueError:
#         return np.nan

# basal_numeric_data = basal_data.iloc[5:].set_index("id").drop(columns=["DESCRIPTION"]).applymap(convert_to_float)
# luminal_numeric_data = luminal_data.iloc[5:].set_index("id").drop(columns=["DESCRIPTION"]).applymap(convert_to_float)

# # Perform t-test for each gene
# p_values = []
# gene_ids = []
# for gene in basal_numeric_data.index:
#     basal_expression = basal_numeric_data.loc[gene].dropna()
#     luminal_expression = luminal_numeric_data.loc[gene].dropna()
    
#     # Only perform t-test if there are sufficient data points for both groups
#     if len(basal_expression) > 2 and len(luminal_expression) > 2:
#         t_stat, p_val = ttest_ind(basal_expression, luminal_expression)
#         p_values.append(p_val)
#         gene_ids.append(gene)

# # Combine results into a DataFrame
# diff_expr_results = pd.DataFrame({
#     'Gene_ID': gene_ids,
#     'p_value': p_values
# })

# # Sort results by p-value
# diff_expr_results = diff_expr_results.sort_values(by="p_value")

# # Display top differentially expressed genes
# print(diff_expr_results.head(10))


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv("/home/dataset/EDS-1013.gct", sep="\t", skiprows=2)

# Extract the subtype row to identify cell lines classified as Basal or Luminal
subtype_row = data[data['id'] == "subtype"].iloc[0, 4:]
basal_cell_lines = subtype_row[subtype_row == "Basal"].index.tolist()
luminal_cell_lines = subtype_row[subtype_row == "Luminal"].index.tolist()

# Extract the gene expression data for Basal and Luminal cell lines
gene_expression_data = data.iloc[5:, :].reset_index(drop=True)
basal_data = gene_expression_data[["id", "DESCRIPTION"] + basal_cell_lines]
luminal_data = gene_expression_data[["id", "DESCRIPTION"] + luminal_cell_lines]

# Convert valid numeric strings to floats and replace non-numeric strings with NaN
def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return np.nan

basal_numeric_data = basal_data.iloc[5:].set_index("id").drop(columns=["DESCRIPTION"]).applymap(convert_to_float)
luminal_numeric_data = luminal_data.iloc[5:].set_index("id").drop(columns=["DESCRIPTION"]).applymap(convert_to_float)

# Perform t-test for each gene
p_values = []
gene_ids = []
for gene in basal_numeric_data.index:
    basal_expression = basal_numeric_data.loc[gene].dropna()
    luminal_expression = luminal_numeric_data.loc[gene].dropna()
    
    # Only perform t-test if there are sufficient data points for both groups
    if len(basal_expression) > 2 and len(luminal_expression) > 2:
        t_stat, p_val = ttest_ind(basal_expression, luminal_expression)
        p_values.append(p_val)
        gene_ids.append(gene)

# Combine results into a DataFrame
diff_expr_results = pd.DataFrame({
    'Gene_ID': gene_ids,
    'p_value': p_values
})

# Sort results by p-value
diff_expr_results = diff_expr_results.sort_values(by="p_value")

# Display top differentially expressed genes
print(diff_expr_results.head(10))

# Extract expression data for the top genes from both Basal and Luminal datasets
top_genes = diff_expr_results["Gene_ID"].head(10).tolist()
heatmap_data_basal = basal_numeric_data.loc[top_genes, basal_cell_lines]
heatmap_data_luminal = luminal_numeric_data.loc[top_genes, luminal_cell_lines]

# Combine the data for heatmap
heatmap_data = pd.concat([heatmap_data_basal, heatmap_data_luminal], axis=1)

# Plot heatmap
plt.figure(figsize=(20, 10))
sns.heatmap(heatmap_data, cmap="RdBu_r", center=0)
plt.title('Expression Heatmap for Top Differentially Expressed Genes')
plt.show()
plt.savefig('/home/dataset/charts/EDS-1013-step_by_step_heatmap.png')