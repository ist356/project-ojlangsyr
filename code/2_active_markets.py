import pandas as pd

def create_active_markets_csv(source_file, target_file):
    df = pd.read_csv(source_file)
    open_markets = df[df['closed'] == False]
    open_markets.to_csv(target_file, index=False)
    print(f"Active (open) markets saved to '{target_file}'.")

if __name__ == "__main__":
    source_file = 'cache/all_markets.csv'
    target_file = 'cache/active_markets.csv'
    create_active_markets_csv(source_file, target_file)


##########################################
active_markets = pd.read_csv('cache/active_markets.csv')
print(len(active_markets))
#################################################
df = pd.read_csv('cache/active_markets.csv')
assert (df['closed'] == False).all(), "Some rows in active_markets.csv are not open (closed != False)."
print("Validation passed: All rows in active_markets.csv have closed == False.")

#day 1 1726
#day 2 1739
#day 3 1787
#day 4 1801