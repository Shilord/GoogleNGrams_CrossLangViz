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
    corpus which includes data for several languages. One can observe linguistic and cultural trends through visualizing how these 
    frequencies change over time and for different languages.     
    </p>
    <hr style="border-top: 1px solid #333; width: 50%; margin: 20px auto;">
    <div class="instruction-header">Definitions</div>
    <p class="instruction-text">
        <b>What is an N-gram?</b><br>
        N-grams have a more nuanced and complex definition in linguistics and corpus analysis, but for the 
    purpose of this dashboard, can be understood as any word or string of words of length n (becoming a phrase). 
        <br><br>
        <b>What is Frequency?</b><br>
        In this dashboard, all mentions of "frequency" refer to relative frequency based on data from the Google 
    Ngram dataset. Please note that many visualizations (all of main dashboard) report said frequency in micro units 
    (10<sup>−6</sup>, also known as parts per million - ppm, symbol: µ). Relative frequency for an Ngram is defined 
    as the number of times it appears per million words in the literature from that language for that year. While the 
    Google Books corpus is not all-inclusive or entirely free of sampling bias, the relative frequency still serves 
    as an appropriate metric for "popularity" or "usage" of a given word or phrase.   
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
    phrases that tell a story.
    </div>
    <div class="step-box">
        <div class="step-title">5. Compare Word Trends</div>
       You may also use the Compare Words tab to compare frequencies of words you choose, like creating your own fun facts graph.
    </div>
    <div style="margin-top: 20px; padding: 10px;">
        <p style="font-size: 18px; color: #a8a8a8;">
            Ready to explore? Head to the 
            <a href="?tab=Dashboard" target="_self" style="color: #4da6ff; text-decoration: none; font-weight: bold;">
                Dashboard
            </a> !
        </p>
    </div>
    <hr style="border-top: 1px solid #333; width: 50%; margin: 10px auto;">
    <div class="instruction-header">Disclaimer</div>
    <p class="instruction-text">
        In this dashboard, we aim to provide an enhanced version of the Google Ngrams Viewer that is able to compare word 
    frequencies across languages. We cannot guarantee appropriate translations or synonyms for all search terms. This is a 
    data science project, and not a linguistics project. We recognize the many shortcomings of our methods of translation and 
    synonym creation using pre-existing Python packages and API calls. This includes how they may fail to capture an intended 
    meaning for certain languages or search terms. However, these issues are out of the scope of this project at this time. 
    Please consider this when taking the information from this dashboard.    
    </p>
    <hr style="border-top: 1px solid #333; width: 50%; margin: 20px auto;">
    <div class="instruction-header">Known Issues</div>
    <div class="step-box">
        The auto detect language function is unreliable. We highly suggest manually selecting the input language for linguistic search.
    </div>
    <div class="step-box">
        The deep-translator Python package used does not always provide accurate translations. In rare circumstances, the package does 
        not provide any output at all for another language(s) (therefore some languages may be missing outright from the visualizations).
    </div>
    <div class="step-box">
        When the input term is not English, it is first translated to English and synonyms are generated in English before it is then 
        translated to the other languages (including back to the original input language). This means that in certain circumstances, 
        if the most common translation back into the input language is different from the input term, the word or phrase shown for the 
        input language is not the input term.
    </div>
    </div>
</div>
""", unsafe_allow_html=True)
        
#st.video("guide.mp4")        