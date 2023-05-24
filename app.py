import streamlit as st
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from collections import Counter

df = pd.read_csv(r"NER-testing\data\traveleng-cleaned2.csv")


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
                        "including"]
    stop_words = set(stopwords.words('english')).union(custom_stopwords)

    tokens = [token for token in tokens if token not in stop_words]

    # Extract unique tags
    unique_tags = list(set(tokens))

    return unique_tags


# Apply preprocessing to the 'overview' column
df['tags'] = df['overview'].apply(preprocess_text)

def tag_search(query, dataframe):
    query_tags = query.split()  # Split the query into individual tags

    # Filter the DataFrame based on the query tags
    results = dataframe[dataframe['tags'].apply(lambda tags: all(tag in tags for tag in query_tags))]

    return results

def main():
    # Set app title
    st.title("Tag Search App")

    # Create a search bar
    query = st.text_input("Enter tags to search", "")

    # Perform search and display results
    if query:
        search_results = tag_search(query, df)
        st.dataframe(search_results)


if __name__ == '__main__':
    main()