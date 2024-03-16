import pandas as pd
import re
from collections import defaultdict
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Load datasets
elements_df = pd.read_csv('C:\\Users\\goldw\\AI_project\\PTE.csv', encoding='utf-8')
compounds_df = pd.read_csv('C:\\Users\\goldw\\AI_project\\Compounds.csv', encoding='utf-8')

# Get element symbols
element_symbols = elements_df['Symbol'].unique().tolist()

# Define regex pattern for parsing molecular formulas
# Matches elements (Capital letter followed by optional lowercase letters) and optional counts
pattern = re.compile(r'([A-Z][a-z]?)(\d*)')

def parse_formula(formula, element_symbols):
    # initialize a count dictionary with all elements set to zero
    element_counts = {symbol: 0 for symbol in element_symbols}
    # find all elements and thieir counts in the formula
    matches = pattern.findall(formula)
    for(element, count) in matches:
        if element in element_counts:
            element_counts[element] = int(count) if count else 1
    # return the counts in the order of unique elements
    return [element_counts[element] for element in element_symbols]

# Create the binary presence matrix for compounds
binary_matrix = []
for formula in compounds_df['Molecular formula']:
    binary_matrix.append(parse_formula(formula, element_symbols))

# Convert the binary presence matrix into a dataframe
element_presence_df = pd.DataFrame(binary_matrix, columns = element_symbols)

# Select elemental properties
element_properties = elements_df[['Symbol', 'Electronegativity', 'Atomic Radius', 'Valence', 'Electron Affinity', 'First Ionization Potential']]

# Convert properties DataFrame to a dictionary for fast lookup
properties_dict = element_properties.set_index('Symbol').T.to_dict('list')

# Calculate the average properties for each compound
def calculate_average_properties(binary_vector, properties_dict, element_symbols):
    # initialize sums and counts
    property_sums = defaultdict(float)
    element_counts = defaultdict(int)

    # calculate the sum of properties for each element present in the compound
    for i, count in enumerate(binary_vector):
        if count > 0:
            element = element_symbols[i]
            properties = properties_dict.get(element, [None]*len(element_properties.columns)-1)  # Adjust the default list length
            for j, property_value in enumerate(properties):
                if property_value is not None:
                    property_key = element_properties.columns[j+1]  # +1 to skip 'Symbol' column
                    property_sums[property_key] += property_value * count
                    element_counts[property_key] += count
    
    # Calculate the average properties
    averages = {prop: (property_sums[prop] / element_counts[prop] if element_counts[prop] else None) for prop in property_sums}
    return [averages.get(prop) for prop in element_properties.columns[1:]]  # Skip 'Symbol' column

# Apply the average property calculation to each row in the binary matrix
average_properties = [calculate_average_properties(row, properties_dict, element_symbols) for row in binary_matrix]

# Create a DataFrame from the average properties
average_properties_names = [f"Avg {prop}" for prop in element_properties.columns[1:]]  # Skip 'Symbol' column
average_properties_df = pd.DataFrame(average_properties, columns=average_properties_names)

# Concatenate the binary presence matrix with the average properties DataFrame
final_features_df = pd.concat([element_presence_df, average_properties_df], axis=1)

scaler = StandardScaler()
scaled_features = scaler.fit_transform(final_features_df)
