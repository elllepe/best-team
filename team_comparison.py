import streamlit as st
import pandas as pd
import openpyxl

# Set up the Streamlit app UI
st.title('Is Your Team Better Than Another?')

# File uploader to upload Excel file
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Load your Excel data from the uploaded file
    df = pd.read_excel(uploaded_file)
    
    # Clean the data (stripping any extra spaces)
    df['Winner'] = df['Winner'].str.strip()  # Strip any extra spaces from column names
    df['Loser'] = df['Loser'].str.strip()

    # Create a directed graph where the winner is the source and the loser is the target
    G = nx.from_pandas_edgelist(df, source='Winner', target='Loser', create_using=nx.DiGraph)

    # List all nodes in the graph
    nodes = list(G.nodes)

    # Dropdowns for selecting teams (match winners)
    my_team = st.selectbox('My Team', nodes)
    your_team = st.selectbox('Your Team', nodes)

    # Apply Dijkstra's algorithm to find the shortest paths from My Team to all other nodes
    if my_team in G and your_team in G:
        shortest_paths = nx.single_source_dijkstra_path(G, my_team)
        shortest_path_lengths = nx.single_source_dijkstra_path_length(G, my_team)

        # Initialize the path description as a list of strings
        path_description = [f"{my_team} are better than {your_team} because:\n"]

        # Check if the path exists
        if your_team in shortest_paths:
            path = shortest_paths[your_team]
            distance = shortest_path_lengths[your_team]

            # Loop through the path and describe the matchups
            for i in range(len(path) - 1):
                path_description.append(f"{path[i]} beat {path[i + 1]};\n")  # Adding each matchup to the list
               
            # Add the conclusion
            path_description.append(f"Therefore, {my_team} are better than {your_team}!")

        else:
            # If no path is found
            path_description = [f"{my_team} is not better than {your_team}"]

        # Display the final message
        st.write("\n".join(path_description))  # Join the list into a string with newlines and display it

    else:
        st.write("Please select valid teams that exist in the graph.")
else:
    st.write("Please upload an Excel file to proceed.")
