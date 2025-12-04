import streamlit as st

def show_instructions():
    # CSS to center text and style the page
    st.markdown("""
<style>
    .centered-container {
        text-align: center;
        font-family: 'Source Sans Pro', sans-serif;
        padding: 10px 0;
    }
    .instruction-title {
        color: #ffffff;
        margin-top: 0px;
        margin-bottom: 10px;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
    }
    .instruction-header {
        color: #4da6ff;
        margin-top: 30px;
        margin-bottom: 10px;
        font-size: 1.5rem;
        font-weight: 600;
    }
    .instruction-text {
        color: #e0e0e0;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .step-box {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        margin: 10px auto;
        max-width: 600px;
        border: 1px solid #3b3c45;
    }
    .step-title {
        font-weight: bold;
        color: #FF4B4B;
        font-size: 1.1rem;
    }
""", unsafe_allow_html=True)

    _, col_center, _ = st.columns([1, 6, 1])

    with col_center:
        # Note: The strings below are NOT indented to avoid the "Code Block" issue
        
        # st.markdown('<h1 style="text-align: center;">How to Use This Dashboard</h1>', unsafe_allow_html=True)
        st.markdown("""
                    <div class="instruction-title">
                        How to Use This Dashboard
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("""
<div class="centered-container">
    <div class="instruction-header">Purpose and Background</div>
    <p class="instruction-text">
        We were initially inspired by the question: "How do different cultures emphasize different ideas?" 
    In our iterative search for relevant large datasets and refining this question, we eventually decided 
    on the Google Ngram dataset. This took us on a journey to answer the question "How does the usage of words or phrases vary over time 
    between different countries or languages?" The Google Ngram dataset is a massive collection of word 
    frequency data, derived from countless digitized books and other literature sources in the Google Books 
    corpus which includes data for several languages. As such, by visualizing how these frequencies change 
    over time and for different languages, one can observe linguistic and cultural trends.        
    </p>
    <hr style="border-top: 1px solid #333; width: 50%; margin: 20px auto;">
    <div class="instruction-header">Definitions</div>
    <p class="instruction-text">
        <b>What is an N-gram?</b><br>
        N-grams have a more nuanced and complex definition in linguistics and corpus analysis, but for the 
    purpose of this dashboard, can be understood as any word or string of words (a phrase). 
        <br><br>
        <b>What is Frequency?</b><br>
        In this dashboard, all mentions of "frequency" refer to relative frequency based on data from the Google 
    Ngram dataset. Relative frequency for an Ngram is defined as the number of times it appears per million 
    words in the literature from that language for that year. While the Google Books corpus is not all-inclusive 
    or entirely free of sampling bias, the relative frequency still serves as an appropriate metric for 
    "popularity" or "usage" of a given word or phrase.   
    </p>
    <hr style="border-top: 1px solid #333; width: 50%; margin: 20px auto;">
    <div class="instruction-header">Getting Started</div>
    <div class="step-box">
        <div class="step-title">1. Dashboard Controls</div>
        In the Dashboard tab, customize "Search Controls" before clicking "Run Linguistic Search" to begin 
    analysis (this may take a few moments). 
    </div>
    <div class="step-box">
        <div class="step-title">2. Explore Visuals</div>
        Interact with the world map, bar graph, word cloud, and time series graph to understand linguistic trends such as how the 
    popularity of an Ngram has changed in the past 200 years, or how certain terms appear more often in one language than another. 
    </div>
    <div class="step-box">
        <div class="step-title">3. Time Travel</div>
        Adjust the date slider to a target year and observe how frequencies may vary over time. 
    </div>
    <div class="step-box">
        <div class="step-title">4. Fun Facts</div>
       Feel free to visit the Fun Facts tab to view quick visualizations we've created with pre-chosen words and 
    phrases that tell a fun story.
    </div>
    <div class="step-box">
        <div class="step-title">4. Compare Word Trends</div>
       You may also use the Compare Words tab to compare frequencies of words you choose, like creating your own fun facts graph.
    </div>
    <br>
    <div style="margin-top: 30px; padding: 20px; border-top: 1px solid #333;">
        <p style="font-size: 18px; color: #a8a8a8;">
            Ready to explore? Head to the 
            <a href="?tab=Dashboard" target="_self" style="color: #4da6ff; text-decoration: none; font-weight: bold;">
                Dashboard
            </a> !
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
        
#st.video("guide.mp4")        