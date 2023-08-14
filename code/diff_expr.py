import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Load and preprocess the data
data = pd.read_csv('/home/dataset/EDS-1013.gct', sep='\t', skiprows=2)
expression_data = data.drop(columns=['id', 'PROBE Name_GeneSymbol', 'ID_geneid', 'DESCRIPTION'], errors='ignore')
expression_data = expression_data.replace('na', float('nan'))
expression_data = expression_data.apply(pd.to_numeric, errors='coerce')

# Perform t-test for two groups
cell_line1 = expression_data['184A1']
cell_line2 = expression_data['184B5']
t_stat, p_values = ttest_ind(cell_line1, cell_line2)

# Extract differentially expressed genes
alpha = 0.05
significant_genes = p_values[p_values < alpha].index

# Visualization for validation
for gene in significant_genes[:5]:  # Adjust this to view more genes
    sns.boxplot(data=expression_data.loc[gene])
    plt.title(f"Expression Distribution for Gene {gene}")
    plt.ylabel("Expression Value")
    # plt.show()
    plt.savefig('/home/dataset/charts/gene_expr.png')
