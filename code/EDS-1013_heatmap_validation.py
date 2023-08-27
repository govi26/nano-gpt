# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Load the gene expression data
# data = pd.read_csv('/home/dataset/EDS-1013.gct', sep='\t', skiprows=2)

# # Remove metadata rows
# expression_data = data.iloc[5:].copy()

# # Set the 'Name_GeneSymbol' as the index for the rows
# expression_data.set_index('Name_GeneSymbol', inplace=True)

# # Convert the expression data to numeric values
# expression_data = expression_data.apply(pd.to_numeric, errors='coerce')

# # Compute the Median Absolute Deviation (MAD) for each gene
# mad_values = expression_data.mad(axis=1)

# # Sort genes based on MAD values in descending order
# sorted_genes = mad_values.sort_values(ascending=False)

# # Select the top 100 genes based on MAD values
# top_100_genes = sorted_genes.head(100).index

# # Filter the expression data for these genes
# top_genes_data = expression_data.loc[top_100_genes]

# # Drop non-expression columns for clustering
# cluster_data = top_genes_data.drop(columns=['id', 'PROBE', 'ID_geneid', 'DESCRIPTION'])

# # Create a heatmap with hierarchical clustering
# plt.figure(figsize=(15, 20))
# sns.clustermap(cluster_data, cmap="vlag", row_cluster=True, col_cluster=True, center=0, linewidths=.75, figsize=(15, 15))
# # plt.show()
# plt.savefig('/home/dataset/charts/EDS-1013-heatmap.png')



# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Load the gene expression data
# data = pd.read_csv('/home/dataset/EDS-1013.gct', sep='\t', skiprows=2)

# # Remove metadata rows
# expression_data = data.iloc[5:].copy()

# # Set the 'Name_GeneSymbol' as the index for the rows
# expression_data.set_index('Name_GeneSymbol', inplace=True)

# # Convert the expression data to numeric values
# expression_data = expression_data.apply(pd.to_numeric, errors='coerce')

# # Compute the Median Absolute Deviation (MAD) for each gene using the DataFrame's mad method
# mad_values = expression_data.mad(axis=1)

# # Sort genes based on MAD values in descending order
# sorted_genes = mad_values.sort_values(ascending=False)

# # Select the top 100 genes based on MAD values
# top_100_genes = sorted_genes.head(10).index

# # Filter the expression data for these genes
# top_genes_data = expression_data.loc[top_100_genes]

# # Drop non-expression columns for clustering
# cluster_data = top_genes_data.drop(columns=['id', 'PROBE', 'ID_geneid', 'DESCRIPTION'])

# # Create a heatmap with hierarchical clustering
# plt.figure(figsize=(15, 20))
# sns.clustermap(cluster_data, cmap="vlag", row_cluster=True, col_cluster=True, center=0, linewidths=.75, figsize=(15, 15))
# # plt.show()
# plt.savefig('/home/dataset/charts/EDS-1013-heatmap.png')



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the gene expression data
data_new = pd.read_csv('/home/dataset/EDS-1013.gct', sep='\t', skiprows=2)

# Remove metadata rows
expression_data_new = data_new.iloc[5:].copy()

# Extract the subtype row
subtypes_new = data_new.loc[data_new['id'] == 'subtype'].iloc[:, 5:].transpose()
subtypes_new.columns = ['subtype']

# Filter the data to include only samples with "Basal" or "Luminal" subtype and create a copy to avoid SettingWithCopyWarning
filtered_subtypes_new = subtypes_new[subtypes_new['subtype'].isin(['Basal', 'Luminal'])].copy()

# Update the color map for the subtypes
subtype_colors_new = {
    "Luminal": "red",
    "Basal": "green"
}

# Map the updated subtype colors
filtered_subtypes_new['color'] = filtered_subtypes_new['subtype'].map(subtype_colors_new)

# Set the 'Name_GeneSymbol' as the index for the rows
expression_data_new.set_index('Name_GeneSymbol', inplace=True)

# Convert the expression data to numeric values
expression_data_new = expression_data_new.apply(pd.to_numeric, errors='coerce')

# Compute the Median Absolute Deviation (MAD) for each gene
mad_values_new = expression_data_new.mad(axis=1)

# Sort genes based on MAD values in descending order
sorted_genes_new = mad_values_new.sort_values(ascending=False)

# Select the top 50 genes based on MAD values
top_50_genes_new = sorted_genes_new.head(5).index

# Filter the expression data for these top 50 genes
top_50_genes_data_new = expression_data_new.loc[top_50_genes_new]

# Filter the top 50 gene expression data to include only the selected samples (Basal and Luminal)
filtered_cluster_data_top_50 = top_50_genes_data_new[filtered_subtypes_new.index]

# Create the heatmap with hierarchical clustering using Euclidean distance and subtype annotations for top 50 genes
plt.figure(figsize=(15, 15))
sns.clustermap(filtered_cluster_data_top_50, cmap="vlag", row_cluster=True, col_cluster=True, center=0, linewidths=.75, figsize=(15, 15),
               col_colors=filtered_subtypes_new['color'], cbar_pos=(0.02, 0.65, 0.05, 0.18), metric="euclidean")
# plt.show()
plt.savefig('/home/dataset/charts/EDS-1013-heatmap.png')

top_5_genes_new = sorted_genes_new.head(5)
print(top_5_genes_new)

