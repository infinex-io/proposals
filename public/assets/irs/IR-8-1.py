import pandas as pd

# Define the months
months_A = list(range(13))  # 0 to 12 for Option A and B
months_B = list(range(13))
months_C = list(range(25))  # 0 to 24 for Option C

# Initial weights for soulbound NFTs
initial_weight_T2 = 0.6
initial_weight_T3 = 0.25

# Weight per ERC20 token
weight_per_G = 1 / 12

# Linear decay for soulbound NFTs
linear_decay_T2 = [round(initial_weight_T2 - (initial_weight_T2 / 12) * m, 2) for m in months_B]
linear_decay_T3 = [round(initial_weight_T3 - (initial_weight_T3 / 12) * (m - 12), 2) if m >= 12 else round(initial_weight_T3, 2) for m in months_C]

# Option A: Immediate distribution of 12 ERC20 tokens
erc20_received_A = [12] * 13
total_weight_erc20_A = [round(12 * weight_per_G, 2)] * 13
total_weight_A = total_weight_erc20_A  # No soulbound NFT for Option A

# Option B: 12-month linear vesting
erc20_received_B = list(range(13))  # 0 to 12 ERC20 tokens
total_weight_erc20_B = [round(m * weight_per_G, 2) for m in erc20_received_B]
total_weight_B = [round(total_weight_erc20_B[m] + linear_decay_T2[m], 2) for m in months_B]

# Option C: 1-year cliff + 12-month linear vesting
erc20_received_C = [0] * 13 + list(range(1, 13))  # Adjusted to match 25 months
total_weight_erc20_C = [round(erc20_received_C[m] * weight_per_G, 2) for m in months_C]
linear_decay_T3_adjusted = [round(initial_weight_T3 - (initial_weight_T3 / 12) * (m - 12), 2) if m >= 12 else round(initial_weight_T3, 2) for m in months_C]
total_weight_C = [round(total_weight_erc20_C[m] + linear_decay_T3_adjusted[m], 2) for m in months_C]

# Create DataFrames for visualization
data_A = {
    'Month': months_A,
    'ERC20 Received': erc20_received_A,
    'Weight of Each ERC20 Token': [round(weight_per_G, 2)] * 13,
    'Total Weight of ERC20 Tokens': total_weight_erc20_A,
    'Weight of Soulbound NFT': [0] * 13,
    'Total Weight': total_weight_A
}

data_B = {
    'Month': months_B,
    'ERC20 Received': erc20_received_B,
    'Weight of Each ERC20 Token': [round(weight_per_G, 2)] * 13,
    'Total Weight of ERC20 Tokens': total_weight_erc20_B,
    'Weight of Soulbound NFT': linear_decay_T2,
    'Total Weight': total_weight_B
}

data_C = {
    'Month': months_C,
    'ERC20 Received': erc20_received_C,
    'Weight of Each ERC20 Token': [round(weight_per_G, 2)] * 25,
    'Total Weight of ERC20 Tokens': total_weight_erc20_C,
    'Weight of Soulbound NFT': linear_decay_T3_adjusted,
    'Total Weight': total_weight_C
}

df_A = pd.DataFrame(data_A)
df_B = pd.DataFrame(data_B)
df_C = pd.DataFrame(data_C)

# Function to convert DataFrame to markdown table
def df_to_markdown(df, title):
    md = f"## {title}\n\n"
    md += df.to_markdown(index=False) + "\n\n"
    return md

# Convert dataframes to markdown
md_content = ""
md_content += df_to_markdown(df_A, "Option A Distribution")
md_content += df_to_markdown(df_B, "Option B Distribution")
md_content += df_to_markdown(df_C, "Option C Distribution")

# Save to markdown file
with open("ERC20_Soulbound_NFT_Distribution.md", "w") as f:
    f.write(md_content)

print("Markdown document created successfully.")
