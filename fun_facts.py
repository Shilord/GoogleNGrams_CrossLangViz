import streamlit as st

def show_fun_facts():
    st.title("🎯 Fun Facts About Languages")
    
    st.markdown("""
    ### Interesting Linguistic Facts
    
    - **Most Spoken Language**: English has approximately 1.5 billion speakers worldwide
    - **Fastest Growing**: Spanish is one of the fastest-growing languages
    - **Chinese Characters**: Mandarin uses over 50,000 characters, but only ~3,500 are commonly used
    - **Google Books**: The Google Books Ngram corpus contains over 8 million books
    - **Language Evolution**: New words are added to dictionaries every year based on usage trends
    
    ### Did You Know?
    
    The Google Ngrams data can reveal:
    - Cultural shifts and historical events
    - Technology adoption patterns
    - Social movements through language
    - Scientific discovery trends
    """)
    
    st.info("💡 Use the Dashboard to explore these trends yourself!")
    
    # You can add more interactive content here
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Languages Supported", "7")
        st.metric("Books Analyzed", "8M+")
    with col2:
        st.metric("Year Range", "1600-2022")
        st.metric("Total Years", "422")