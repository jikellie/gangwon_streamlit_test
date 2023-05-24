
import streamlit as st
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from collections import Counter

df = pd.read_csv(r"traveleng-cleaned2.csv")

def preprocess_text(text):
    # Define additional punctuation characters to remove
    additional_punctuation = ['’']

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation + ''.join(additional_punctuation)))

    # Convert text to lowercase
    text = text.lower()

    # Tokenize text
    tokens = word_tokenize(text)

    # Remove stopwords
    custom_stopwords = ["located", "enjoy", "also", "place", "visitors", "area", "various", "offers", "many", "well",
                        "including", "gangwondo", "korea", "one"]
    stop_words = set(stopwords.words('english')).union(custom_stopwords)

    tokens = [token for token in tokens if token not in stop_words]

    # Extract unique tags
    unique_tags = list(set(tokens))

    return unique_tags

# Apply preprocessing to the 'overview' column
df['tags'] = df['overview'].apply(preprocess_text)

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