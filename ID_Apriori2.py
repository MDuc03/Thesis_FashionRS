import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Load the CSV files
item_columns = ['item_id', 'cate_id', 'pic_url', 'title']
outfit_columns = ['outfit_id', 'item_ids']  # 'item_ids' is a semicolon-separated list of item IDs

items_df = pd.read_csv("E:\\Thesis\\data\\item.csv", header=None, names=item_columns)
outfits_df = pd.read_csv("E:\\Thesis\\data\\outfit_sample.arff", header=None, names=outfit_columns)

# Step 1: Convert item_ids to a list of item sets for Apriori processing
outfits_df['item_ids'] = outfits_df['item_ids'].apply(lambda x: str(x).split(';'))

# Step 2: Function to create a one-hot encoding for Apriori
def create_one_hot_matrix(outfits_df):
    itemsets = [outfit['item_ids'] for _, outfit in outfits_df.iterrows()]
    all_items = list(set(item for sublist in itemsets for item in sublist))  # Extract unique items
    one_hot_matrix = pd.DataFrame(columns=all_items, index=range(len(itemsets)), dtype=int).fillna(0)

    for idx, itemset in enumerate(itemsets):
        for item in itemset:
            one_hot_matrix.at[idx, item] = 1

    # Convert to boolean type for better performance
    one_hot_matrix = one_hot_matrix.astype(bool)

    return one_hot_matrix

# Step 3: Apply Apriori to find frequent itemsets
def apriori_model(min_support=0.01, min_lift=1):
    """
    Apply Apriori algorithm to the dataset and generate association rules.
    """
    # Create one-hot matrix
    one_hot_matrix = create_one_hot_matrix(outfits_df)

    # Apply Apriori to find frequent itemsets
    frequent_itemsets = apriori(one_hot_matrix, min_support=min_support, use_colnames=True)

    if frequent_itemsets.empty:
        print("No frequent itemsets found. Try lowering `min_support` or check your dataset.")
        return pd.DataFrame()

    # Generate association rules
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift, num_itemsets=len(frequent_itemsets))

    return rules

# Step 4: Save rules to ARFF file
def save_to_arff(df, file_path, relation_name="rules"):
    """
    Save DataFrame to ARFF file format.
    """
    with open(file_path, "w") as f:
        # Write the relation name
        f.write(f"@RELATION {relation_name}\n\n")

        # Write attribute information
        f.write("@ATTRIBUTE antecedents STRING\n")
        f.write("@ATTRIBUTE consequents STRING\n")
        f.write("@ATTRIBUTE support NUMERIC\n")
        f.write("@ATTRIBUTE confidence NUMERIC\n")
        f.write("@ATTRIBUTE lift NUMERIC\n")

        f.write("\n@DATA\n")

        # Write data
        for _, rule in df.iterrows():
            antecedents = ','.join([f"'{item}'" for item in rule['antecedents']])
            consequents = ','.join([f"'{item}'" for item in rule['consequents']])
            f.write(f"{{{antecedents}}},{{{consequents}}},{rule['support']},{rule['confidence']},{rule['lift']}\n")

# Train the Apriori model
rules = apriori_model(min_support=0.000001, min_lift=1)

if not rules.empty:
    # Save the rules to an ARFF file
    output_file = "E:\\Thesis\\data\\rule.arff"
    save_to_arff(rules, output_file)
    print(f"Association rules saved to {output_file}")
else:
    print("No rules generated.")
