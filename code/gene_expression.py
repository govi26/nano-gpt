# import pandas as pd

# # Attempt to load the dataset
# try:
#     data = pd.read_csv('/home/dataset/EDS-1013.gct', sep='\t', skiprows=2)
# except Exception as e:
#     error_message = str(e)
#     data = None

# print(data.head() if data is not None else error_message)




# # # Separating meta-data from gene expression data
# meta_data = data.iloc[:5, :]
# expression_data = data.iloc[5:, :]

# # # Drop the first few columns from expression data which are not related to expression values
# # expression_data = expression_data.drop(columns=['id', 'PROBE Name_GeneSymbol', 'ID_geneid', 'DESCRIPTION'])

# # # Convert expression data to numeric type
# # expression_data = expression_data.astype(float)

# # # Compute basic statistics
# # basic_statistics = expression_data.describe().transpose()

# # print(basic_statistics)

 


# #  # Correcting the column names and dropping them
# # expression_data = expression_data.drop(columns=['id', 'PROBE Name_GeneSymbol', 'ID_geneid', 'DESCRIPTION'], errors='ignore')

# # # Convert expression data to numeric type
# # expression_data = expression_data.astype(float)

# # # Compute basic statistics
# # basic_statistics = expression_data.describe().transpose()

# # print(basic_statistics)




# # # Replace non-numeric values with NaN and convert data to float
# # expression_data = expression_data.replace('na', float('nan'))
# # expression_data = expression_data.astype(float)

# # # Compute basic statistics
# # basic_statistics = expression_data.describe().transpose()

# # (basic_statistics)




# # Convert any non-numeric values to NaN
# expression_data = expression_data.apply(pd.to_numeric, errors='coerce')

# # Compute basic statistics
# basic_statistics = expression_data.describe().transpose()

# print(basic_statistics)





# # Compute mean expression for each gene across all cell lines
# mean_expression = expression_data.mean(axis=1)

# # Identify top 10 genes based on mean expression
# top_genes = mean_expression.nlargest(10)

# print(top_genes)




# # Compute the difference in expression for each gene between the two cell lines
# expression_difference = expression_data['184A1'] - expression_data['184B5']

# # Identify top 10 genes with most significant differences in expression
# top_differential_genes = expression_difference.abs().nlargest(10)

# print('top_differential_genes - ', top_differential_genes)




# import seaborn as sns
# import matplotlib.pyplot as plt

# # Extract expression data for top differentially expressed genes across all cell lines
# heatmap_data = expression_data.loc[top_differential_genes.index]

# # Plot the heatmap
# plt.figure(figsize=(14, 10))
# sns.heatmap(heatmap_data, cmap="RdBu_r", center=0)
# plt.title("Expression Patterns of Top Differentially Expressed Genes")
# plt.ylabel("Genes")
# plt.xlabel("Cell Lines")
# plt.xticks(rotation=90)
# # plt.show()
# plt.savefig('/home/dataset/charts/heatmap.png')




# # Select three genes from the top differentially expressed genes for boxplot visualization
# selected_genes = top_differential_genes.index[:3]

# # Plot boxplots for the selected genes
# plt.figure(figsize=(15, 10))

# for idx, gene in enumerate(selected_genes, 1):
#     plt.subplot(3, 1, idx)
#     sns.boxplot(data=expression_data.loc[gene], orient='h')
#     plt.title(f"Expression Distribution for Gene {gene}")
#     plt.xlabel("Expression Value")

# plt.tight_layout()
# # plt.show()
# plt.savefig('/home/dataset/charts/boxplot.png')




import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data again and preprocess as before
data = pd.read_csv('/home/dataset/EDS-1013.gct', sep='\t', skiprows=2)

# Separate meta-data from gene expression data
expression_data = data.drop(columns=['id', 'PROBE Name_GeneSymbol', 'ID_geneid', 'DESCRIPTION'], errors='ignore')

# Convert non-numeric values to NaN and data to float
expression_data = expression_data.replace('na', float('nan'))
expression_data = expression_data.apply(pd.to_numeric, errors='coerce')

# Identify top 10 genes based on mean expression
mean_expression = expression_data.mean(axis=1)
top_genes = mean_expression.nlargest(10)

# Compute the difference in expression for each gene between two cell lines
expression_difference = expression_data['184A1'] - expression_data['184B5']
top_differential_genes = expression_difference.abs().nlargest(10)

# Extract data for visualization
heatmap_data = expression_data.loc[top_differential_genes.index]
selected_genes = top_differential_genes.index[:3]

# Visualization: Heatmap for top differentially expressed genes
plt.figure(figsize=(14, 10))
sns.heatmap(heatmap_data, cmap="RdBu_r", center=0)
plt.title("Expression Patterns of Top Differentially Expressed Genes")
plt.ylabel("Genes")
plt.xlabel("Cell Lines")
plt.xticks(rotation=90)
# plt.show()
plt.savefig('/home/dataset/charts/heatmap.png')


# Visualization: Boxplots for selected genes
plt.figure(figsize=(15, 10))
for idx, gene in enumerate(selected_genes, 1):
    plt.subplot(3, 1, idx)
    sns.boxplot(data=expression_data.loc[gene], orient='h')
    plt.title(f"Expression Distribution for Gene {gene}")
    plt.xlabel("Expression Value")
plt.tight_layout()
# plt.show()
plt.savefig('/home/dataset/charts/boxplot.png')

