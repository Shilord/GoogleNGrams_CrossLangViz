import streamlit as st

def show_instructions():
    
    st.title("How to Use This Dashboard")
    
    st.markdown("""
    ### Purpose and Background:
    We were initially inspired by the question: "How do different cultures emphasize different ideas?" 
    In our iterative search for relevant large datasets and refining this question, we eventually decided 
    on the Google Ngram dataset and the question "How does the usage of words or phrases vary over time 
    between different countries or languages?" The Google Ngram dataset is a massive collection of word 
    frequency data, derived from countless digitized books and other literature sources in the Google Books 
    corpus that includes data for several languages. As such, by visualizing how these frequencies change 
    over time and for different languages, one can observe linguistic and cultural trends.        

    ### What is an Ngram?
    N-grams have a more nuanced and complex definition in linguistics and corpus analysis, but for the 
    purpose of this dashboard, can be understood as any word or string of words (a phrase). 

    ### What is Frequency?
    In this dashboard, all mentions of "frequency" refer to relative frequency based on data from the Google 
    Ngram dataset. Relative frequency for an Ngram is defined as the number of times it appears per million 
    words in the literature from that language for that year. While the Google Books corpus is not all-inclusive 
    or entirely free of sampling bias, the relative frequency still serves as an appropriate metric for 
    "popularity" or "usage" of a given word or phrase.   

    ### Getting Started:
    ##### Dashboard:
    1. In the Dashboard tab, customize "Search Controls" before clicking "Run Linguistic Search" to begin 
    analysis (this may take a few moments). 
    2. Interact with the world map, bar graph, word cloud, and time series graph to understand linguistic trends such as how the 
    popularity of an Ngram has changed in the past 200 years, or how certain terms appear more often in one language than another. 
    3. Adjust the date slider to a target year and observe how frequencies may vary over time. 
    ##### Fun Facts:
    4. Feel free to visit the Fun Facts tab to view quick visualizations we've created with pre-chosen words and 
    phrases that tell a fun story.
    ##### Compare Words:
    5. You may also use the Compare Words tab to compare frequencies of words you choose, like creating your own fun facts graph.<br>
    
    Tooltips are provided for further details, or watch the short video guide below.

    """,
    unsafe_allow_html=True
    )
    
    #st.video("guide.mp4")

    st.success("✅ Ready to explore? Head to the Dashboard tab!")
