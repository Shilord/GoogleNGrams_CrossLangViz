import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils import * 
def compare_words():
    # --- Header ---
    st.title("Compare Word Trends")
    st.caption("""
    Compare the historical popularity of multiple words simultaneously.  
    Enter words below to generate a time-series comparison and a correlation heatmap.
    """)
    
    st.divider()

    # --- Main Page Configuration Controls ---
    # We use columns to keep the UI clean without using the sidebar
    config_col1, config_col2, config_col3 = st.columns([1, 2, 1])

    with config_col1:
        # Language Selection
        selected_lang_name = st.selectbox(
            "Select Language Corpus",
            options=list(lang_to_lang_translation.keys()),
            index=0
        )
        selected_lang_code = lang_to_lang_translation[selected_lang_name]

    with config_col2:
        # Date Range Slider
        min_year, max_year = st.slider(
            "Select Year Range",
            min_value=MIN_YEAR,
            max_value=MAX_YEAR,
            value=(1800, 2019)
        )

    with config_col3:
        # Smoothing Slider
        smoothing = st.slider("Smoothing (Rolling Avg)", 1, 10, 5)

    st.divider()

    # --- Input Form ---
    with st.form(key='compare_form'):
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input(
                "Enter words to compare (comma separated)",
                placeholder="e.g., data, science, ai, machine learning",
                # value="data, science"
            )
        with col2:
            st.write("") # Spacer for vertical alignment
            st.write("") 
            submit_button = st.form_submit_button(label='Run Comparison', type="primary")

    # --- Logic & Visualizations ---
    if submit_button and user_input:
        # 1. Parse Input
        words = [w.strip() for w in user_input.split(',') if w.strip()]
        
        if len(words) < 2:
            st.warning("Please enter at least two words to compare.")
        else:
            with st.spinner(f"Fetching data for {len(words)} words..."):
                
                # 2. Prepare Data for get_frequency
                input_df = pd.DataFrame({
                    'word': words,
                    'language': [selected_lang_code] * len(words)
                })

                # 3. Fetch Data using existing utils function
                raw_df = get_frequency(input_df)

                if not raw_df.empty:
                    # Filter by selected year range
                    mask = (raw_df['year'] >= min_year) & (raw_df['year'] <= max_year)
                    filtered_df = raw_df.loc[mask].copy()

                    # --- VISUALIZATION 1: Time Series ---
                    st.subheader("Frequency Over Time")
                    
                    # Apply Smoothing
                    filtered_df['freq_smooth'] = filtered_df.groupby('word')['frequency'].transform(
                        lambda x: x.rolling(window=smoothing, min_periods=1).mean()
                    )

                    fig_ts = go.Figure()
                    
                    # Plot each word
                    for word in words:
                        word_data = filtered_df[filtered_df['word'] == word]
                        if not word_data.empty:
                            fig_ts.add_trace(go.Scatter(
                                x=word_data['year'],
                                y=word_data['freq_smooth'],
                                mode='lines',
                                name=word,
                                hovertemplate="<b>%{y:.8f}</b><extra></extra>"
                            ))

                    fig_ts.update_layout(
                        template="plotly_dark",
                        xaxis_title="Year",
                        yaxis_title=f"Frequency ({smoothing}-Year Avg)",
                        height=500,
                        hovermode="x unified",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    st.plotly_chart(fig_ts, use_container_width=True)

                    # --- VISUALIZATION 2: Correlation Heatmap ---
                    st.subheader("Correlation Matrix")
                    st.caption("How closely do the trends of these words match? (1 = Perfect Match, -1 = Inverse Trend)")

                    # Pivot data for correlation: Rows=Year, Cols=Words, Values=Frequency
                    pivot_df = filtered_df.pivot(index='year', columns='word', values='freq_smooth')
                    
                    # Calculate Correlation
                    corr_matrix = pivot_df.corr()

                    # Create Heatmap
                    fig_corr = go.Figure(data=go.Heatmap(
                        z=corr_matrix.values,
                        x=corr_matrix.columns,
                        y=corr_matrix.index,
                        colorscale='RdBu', 
                        zmin=-1, 
                        zmax=1,
                        text=np.round(corr_matrix.values, 2),
                        texttemplate="%{text}",
                        textfont={"size": 12}
                    ))

                    fig_corr.update_layout(
                        template="plotly_dark",
                        height=500,
                        width=500,
                        xaxis_side="bottom",
                        yaxis=dict(
                            scaleanchor="x", 
                            scaleratio=1, 
                            showgrid=False, 
                            showline=False, 
                            zeroline=False,
                            ticks="",   # Removes the tick marks
                            ticklen=0   # Brings the labels right up to the heatmap
                        ),
                        margin=dict(l=70, r=50, t=50, b=50),
                        xaxis=dict(
                            showgrid=False, 
                            showline=False, 
                            zeroline=False
                        )
                    )
                    st.plotly_chart(fig_corr)