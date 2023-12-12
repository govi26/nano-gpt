# import pandas as pd
# from scipy.stats import ttest_ind
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Step 1: Load the data
# data = pd.read_csv('/home/dataset/TCGA_BRCA_RNASeqV2_2019.gct', sep='\t', skiprows=2)

# # Step 2: Preprocess the data
# # Transpose the data to have genes as columns
# data_transposed = data.transpose()

# # Create a header with the first row (which contains gene names)
# data_transposed.columns = data_transposed.iloc[0]

# # Remove the first row (which contains gene names)
# data_transposed = data_transposed[1:]

# # Reset the index
# data_transposed.reset_index(inplace=True)

# # Get the sample groups
# sample_groups = data_transposed['PAM50_mRNA']

# # Get the basal-like and luminal A groups
# basal_like_group = data_transposed[sample_groups == 'Basal-like']
# luminal_a_group = data_transposed[sample_groups == 'Luminal A']

# # Step 3: Perform differential gene expression analysis
# # Initialize an empty list to store the results
# results = []

# # Loop through each gene and perform a t-test
# for gene in data_transposed.columns[2:]:
#     t_stat, p_val = ttest_ind(basal_like_group[gene].astype(float), luminal_a_group[gene].astype(float), equal_var=False, nan_policy='omit')
#     results.append({'Gene': gene, 'P-Value': p_val})

# # Create a DataFrame from the results
# results_df = pd.DataFrame(results)

# # Get the top 50 differentially expressed genes
# top_50_genes = results_df.nsmallest(50, 'P-Value')

# # Step 4: Generate a heatmap
# # Get the top 50 gene names
# top_50_gene_names = top_50_genes['Gene'].values

# # Get the expression data for the top 50 genes
# top_50_gene_data = data_transposed[top_50_gene_names].astype(float)

# # Create a color map for the sample groups
# color_map = sample_groups.map({'Basal-like': 'red', 'Luminal A': 'blue'}).fillna('grey').tolist()

# # Generate a heatmap using Seaborn's clustermap function
# sns.clustermap(top_50_gene_data, cmap='coolwarm', col_cluster=False, 
#                row_cluster=False, cbar_kws={'label': 'Expression Level'}, 
#                col_colors=color_map, figsize=(20, 10), 
#                yticklabels=top_50_gene_names, dendrogram_ratio=(.1, .2))

# # Add a legend to indicate the sample groups
# plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Basal-like'),
#                     plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Luminal A'),
#                     plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='grey', markersize=10, label='Other')],
#            loc='upper right')

# # Set the title
# plt.title('Heatmap of Top 50 Differentially Expressed Genes', fontsize=14)

# # Display the plot
# plt.tight_layout()
# # plt.show()
# plt.savefig('/home/dataset/charts/TCGA_BRCA_RNASeqV2_2019-heatmap.png')




import pandas as pd
from scipy.stats import ttest_ind
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Load the data
data = pd.read_csv('/home/dataset/TCGA_BRCA_RNASeqV2_2019.gct', sep='\t', skiprows=2)

# Step 2: Preprocess the data
# Extract the 'PAM50_mRNA' column before transposing the data
sample_groups = data.loc[data['id'] == 'PAM50_mRNA'].iloc[0, 2:]

# Transpose the data to have genes as columns
data_transposed = data.drop('Description', axis=1).transpose()

# Create a header with the first row (which contains gene names)
data_transposed.columns = data_transposed.iloc[0]

# Remove the first row (which contains gene names)
data_transposed = data_transposed[2:]

# Reset the index
data_transposed.reset_index(inplace=True)

# Get the basal-like and luminal A groups
basal_like_group = data_transposed[sample_groups == 'Basal-like']
luminal_a_group = data_transposed[sample_groups == 'Luminal A']

# Step 3: Perform differential gene expression analysis
# Initialize an empty list to store the results
results = []

# Loop through each gene and perform a t-test (starting from the 3rd column to exclude non-gene columns)
for gene in data_transposed.columns[3:]:
    t_stat, p_val = ttest_ind(basal_like_group[gene].astype(float), luminal_a_group[gene].astype(float), equal_var=False, nan_policy='omit')
    results.append({'Gene': gene, 'P-Value': p_val})

# Create a DataFrame from the results
results_df = pd.DataFrame(results)

# Get the top 50 differentially expressed genes
top_50_genes = results_df.nsmallest(50, 'P-Value')

# Step 4: Generate a heatmap
# Get the top 50 gene names
top_50_gene_names = top_50_genes['Gene'].values

# Get the expression data for the top 50 genes
top_50_gene_data = data_transposed[top_50_gene_names].astype(float)

# Create a color map for the sample groups
color_map = sample_groups.map({'Basal-like': 'red', 'Luminal A': 'blue'}).fillna('grey').tolist()

# Generate a heatmap using Seaborn's clustermap function
sns.clustermap(top_50_gene_data, cmap='coolwarm', col_cluster=False, 
               row_cluster=False, cbar_kws={'label': 'Expression Level'}, 
               col_colors=color_map, figsize=(20, 10), 
               yticklabels=top_50_gene_names, dendrogram_ratio=(.1, .2))

# Add a legend to indicate the sample groups
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Basal-like'),
                    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Luminal A'),
                    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='grey', markersize=10, label='Other')],
           loc='upper right')

# Set the title
plt.title('Heatmap of Top 50 Differentially Expressed Genes', fontsize=14)

# Display the plot
plt.tight_layout()
# plt.show()
plt.savefig('/home/dataset/charts/TCGA_BRCA_RNASeqV2_2019-heatmap.png')
