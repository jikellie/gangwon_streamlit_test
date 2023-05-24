import streamlit as st
import pandas as pd
import string
from collections import Counter

df = pd.read_csv(r"travel+tags.csv")

#### streamlit from here ###

# Get all unique tags from the 'tags' column
all_tags = set(tag for tags in df['tags'] for tag in tags)

# Define the tag search function
def tag_search(query, dataframe):
    query_tags = query.split()  # Split the query into individual tags

    # Filter the DataFrame based on the query tags
    results = dataframe[dataframe['tags'].apply(lambda tags: all(tag in tags for tag in query_tags))]

    return results

# Define the Streamlit app
def main():
    # Set app title
    st.title("Tag Search App")

    # Create a search bar with autocomplete
    query = st.multiselect(
        "Enter tags to search",
        options=list(all_tags),
        default=[],
        key="search_tags"
    )

    # Perform search and display results
    if query:
        search_results = tag_search(' '.join(query), df)
        st.dataframe(search_results)

# Run the Streamlit app
if __name__ == '__main__':
    main()