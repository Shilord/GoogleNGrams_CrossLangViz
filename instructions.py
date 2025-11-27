import streamlit as st

def show_instructions():
    st.title("📖 How to Use This Dashboard")
    
    st.markdown("""
    ### Getting Started
    
    #### 1. Enter Your Keyword
    - Type any word or phrase you want to analyze
    - Works best with common words that appear in published books
    
    #### 2. Add Context (Optional)
    - **Input Language**: Select the language of your keyword for better translation
    - **Part of Speech**: Filter by noun, verb, adjective, or adverb
    - **Context Topics**: Add related terms to narrow your search
    
    #### 3. Select Languages
    - Choose which languages to compare
    - Select "All Languages" to include all 7 supported languages
    
    #### 4. Include Synonyms (Optional)
    - Toggle "Yes" to include related words
    - Adjust the count (1-20) to control how many synonyms
    
    #### 5. Run Search
    - Click "Run Linguistic Search" to generate visualizations
    - Processing may take 10-30 seconds
    
    ### Understanding the Visualizations
    
    #### World Map
    - **Color intensity**: Shows relative frequency
    - **Hover**: View detailed information
    - **Grey countries**: Unsupported languages
    
    #### Time Series Chart
    - **Solid lines**: Original search term
    - **Dotted lines**: Synonyms
    - **Filter dropdown**: View specific languages
    
    #### Word Cloud
    - **Size**: Indicates relative frequency
    - **Color**: Represents language
    """)
    
    st.success("✅ Ready to explore? Head to the Dashboard tab!")