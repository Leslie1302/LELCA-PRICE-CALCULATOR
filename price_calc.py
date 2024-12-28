import pandas as pd
import streamlit as st  # For an interactive interface

# Step 1: User inputs with Streamlit
st.title("Block Cost and Price Calculator")

# Cement and sand quantities
cement_quantity = st.number_input("How many bags of cement would be used for this round of work?", min_value=0, step=1)
trips_sand = st.number_input("How many trips of sand would be used for this round of work?", min_value=0, step=1)

# Dropdown for block type with a weight factor (for example, different types of blocks have different weights)
block_types = {
    "5 inch Hollow": 7.5,
    "6 inch Hollow": 8.5,
    "5 inch Solid": 7.7,
    "6 inch Solid": 8.7
}
block_type = st.selectbox("Select the block type:", options=list(block_types.keys()))

# Input costs
cement_unitprice = st.number_input("What is the price of cement today?", min_value=0, step=1)
trips_sand_unitprice = st.number_input("What is the price of a trip of sand today?", min_value=0, step=50)
labor = st.number_input("How much will labor cost you today?", min_value=0, step=5)

# Step 2: Initialize session state for calculations
if 'total_cost' not in st.session_state:
    st.session_state.total_cost = 0
if 'cost_per_block' not in st.session_state:
    st.session_state.cost_per_block = 0
if 'final_price_per_block' not in st.session_state:
    st.session_state.final_price_per_block = 0
if 'margin' not in st.session_state:
    st.session_state.margin = 0
if 'num_blocks' not in st.session_state:
    st.session_state.num_blocks = 1  # Default to 1 to prevent the error

# Step 3: Calculate costs and display outputs
if st.button("Calculate Costs"):
    cement_cost = cement_quantity * cement_unitprice
    sand_cost = trips_sand * trips_sand_unitprice
    miscellaneous = 0.1 * (cement_cost + sand_cost + labor)
    total_cost = cement_cost + sand_cost + labor + miscellaneous

    # Save to session state
    st.session_state.total_cost = total_cost

    # Display total cost
    st.write(f"Total Production Cost: {st.session_state.total_cost:.2f}")

# Profit margin and number of blocks input
margin = st.number_input("Enter the profit margin percentage:", min_value=0, step=1, value=st.session_state.margin)
num_blocks = st.number_input(f"How many {block_type} blocks will be produced?", min_value=1, step=1, value=st.session_state.num_blocks)

# Ensure the number of blocks cannot be less than 1
if num_blocks < 1:
    num_blocks = 1

# Save margin and number of blocks to session state
st.session_state.margin = margin
st.session_state.num_blocks = num_blocks

# Calculate cost per block and final price only after inputs are filled
if st.session_state.total_cost > 0 and num_blocks > 0:
    cost_per_block = st.session_state.total_cost / num_blocks
    final_price_per_block = cost_per_block * (1 + margin / 100)

    # Save to session state
    st.session_state.cost_per_block = cost_per_block
    st.session_state.final_price_per_block = final_price_per_block

    # Step 4: Output results
    st.write(f"Production Cost per Block: {st.session_state.cost_per_block:.2f}")
    st.write(f"Final Selling Price per Block: {st.session_state.final_price_per_block:.2f}")

    # Step 5: Option to download results as CSV
    data = {
        "Block Type": [block_type],
        "Total Production Cost": [st.session_state.total_cost],
        "Cost per Block": [st.session_state.cost_per_block],
        "Final Price per Block": [st.session_state.final_price_per_block],
        "Profit Margin (%)": [margin]
    }
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)

    # Download the CSV file
    st.download_button(label="Download CSV", data=csv, file_name="block_cost_report.csv", mime="text/csv")
