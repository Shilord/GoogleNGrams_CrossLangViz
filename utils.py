import pandas as pd
import numpy as np
from deep_translator import GoogleTranslator
import requests
import streamlit as st
import geopandas as gpd
from streamlit_folium import st_folium
import folium
from assets.world_map_css import *
import plotly.graph_objects as go
#Add a function for detecting language of input keyword 


languages = ['en', 'es', 'fr', 'de', 'it', 'ru', 'zh-CN', 'iw'] # list of languages used
NGRAM_API_URL = "https://books.google.com/ngrams/json" # API endpoint

lang_code_to_display = {
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch',
    'it': 'Italiano',
    'ru': 'Русский',
    'zh': '中文',
    'iw': 'עִברִית'
}
lang_to_lang_translation = {'English':'en', 
                            'Chinese': 'zh-CN', 
                            'French':'fr', 
                            'German':'de',
                            'Hebrew':'iw', 
                            'Italian':'it',
                            'Russian':'ru', 
                            'Spanish':'es'}
# sets parameters for API call
def set_params(word, corpus):
    params = {'content': word,
              'year_start': 1500,
              'year_end': 2022,
              'corpus': corpus,
              'smoothing': 0,
              'case_insensitive': 'on'}
    return params

# function to get direct translations for words
def get_languages(input, input_lang, langs_selected):
    df = pd.DataFrame({'word' : input,
                       'language' : input_lang}, index = [0])
    for lang in langs_selected:
        if lang != input_lang:
            translator = GoogleTranslator(source = input_lang, target = lang)
            new_entry = pd.DataFrame({'word' : translator.translate(input),
                            'language' : lang}, index = [0])
            df = pd.concat([df, new_entry], ignore_index = True)
            df['language'] = df['language'].replace('zh-CN', 'zh')
    return df

# gets frequency data from google ngram API
def get_frequency(df):
    years = list(range(1500, 2023))
    data = pd.DataFrame()
    for i in range(len(df)):
        response = requests.get(NGRAM_API_URL, params = set_params(df['word'][i], df['language'][i],), timeout = 30)
        if response.status_code == 200:
            x = response.json()
            if x:
                freq = x[0]['timeseries']
            else:
                freq = [0] * len(years)
        else:
            freq = [0] * len(years)
        data = pd.concat([data, pd.DataFrame({'word': df['word'][i], 
                                              'language' : df['language'][i],
                                              'year' : years, 
                                              'frequency' : freq})], ignore_index = True)
    return data

# main function to run (combines above functions)
def get_translations(word, input_lang, langs_needed):
    return get_frequency(get_languages(word, input_lang, langs_needed))


#Function to get synonyms
def get_synonyms(word, n_synonyms=5, topics=None, pos_filter=None):
    """
    word:       (str) The target word.
    n_synonyms: (int) Max results to return.
    topics:     (str/list/None) Context topics. Pass None to ignore.
    pos_filter: (str/None) 'noun', 'verb', 'adj', 'adv', 'u'. Pass None to ignore.
    """

    pos_map = {
        "noun": "n",      "n": "n",
        "verb": "v",      "v": "v",
        "adjective": "adj", "adj": "adj",
        "adverb": "adv",  "adv": "adv",
        "unknown": "u",   "u": "u" 
    }
    
    target_tag = None
    if pos_filter:
        target_tag = pos_map.get(str(pos_filter).lower().strip())
        if not target_tag:
            print(f"Warning: Unknown POS '{pos_filter}'. Ignoring POS filter.")

    base_url = "https://api.datamuse.com/words"
    payload = {
        "rel_syn": word,
        "md": "p" 
    }
    
    if topics:
        if isinstance(topics, list):
            payload["topics"] = ",".join(topics)
        else:
            payload["topics"] = topics

    try:
        response = requests.get(base_url, params=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            final_results = []
            
            for item in data:
                should_add = False
                
                if target_tag is None:
                    should_add = True
                else:
                    item_tags = item.get('tags', [])
                    if target_tag in item_tags:
                        should_add = True
                
                if should_add:
                    final_results.append(item['word'])
                
                if len(final_results) >= n_synonyms:
                    break
            
            return final_results
        else:
            print(f"API Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Connection Error: {e}")
        return []
    
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



def create_frequency_map(world_map, final_df, year):
    """
    Generates a clean, professional world map colored by relative frequency.
    """
    
    if final_df.empty:
        st.info("Press 'Run Linguistic Search' to generate the initial visualizations.")
        return

    freq_year = final_df[final_df['year'] == year].copy()
    
    if freq_year.empty:
        st.warning(f"No data available for year {year}")
        return
    
    target_languages = [
        'English', 'Español', 'Français', 'Deutsch', 
        'Italiano', 'Русский', '中文', 'עִברִית'
    ]
    
    # Create display_name column
    freq_year['display_name'] = freq_year['language'].map(lambda x: lang_code_to_display[x])
    
    # Aggregate by language: sum frequencies and collect all words
    freq_lookup_df = freq_year.groupby('display_name').agg({
        'frequency': 'sum',
        'word': lambda words: list(words.unique()),
        'is_synonym': 'first'
    }).reset_index()
    
    # Create formatted word-frequency pairs for display
    word_freq_display = {}
    for lang in freq_lookup_df['display_name'].unique():
        lang_data = freq_year[freq_year['display_name'] == lang]
        word_freqs = lang_data.groupby('word')['frequency'].sum().to_dict()
        sorted_word_freqs = sorted(word_freqs.items(), key=lambda x: x[1], reverse=True)
        formatted = ', '.join([f"{word} ({freq:.6f})" for word, freq in sorted_word_freqs])
        word_freq_display[lang] = formatted
    
    # Create lookup dictionaries
    freq_lookup = freq_lookup_df.set_index('display_name')['frequency'].to_dict()
    words_lookup = {lang: word_freq_display[lang] for lang in word_freq_display}
    
    # Prepare choices for np.select
    frequency_choices = [
        freq_lookup.get(lang, np.nan)
        for lang in target_languages
    ]
    word_display_choices = [
        words_lookup.get(lang, 'No data')
        for lang in target_languages
    ]
    
    # Create boolean masks for each language
    langs = [
        (world_map['Primary Language (based on 2015)'] == lang)
        for lang in target_languages
    ]
    
    # Assign values to world_map
    world_map['Frequency'] = np.select(langs, frequency_choices, default=np.nan)
    world_map['Words_Display'] = np.select(langs, word_display_choices, default='No data')
    world_map['Language'] = world_map['Primary Language (based on 2015)']
    
    # Format frequency for display
    world_map['Frequency_Display'] = world_map['Frequency'].apply(
        lambda x: f"{x:.6f}" if pd.notna(x) else "No data"
    )
    
    # Create base folium map
    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        min_zoom=2,
        max_zoom=6,
        tiles=None,
        zoom_control=True,
        scrollWheelZoom=False
    )
    # Add CSS (taken from assets/world_map_css) to style the legend
    m.get_root().html.add_child(folium.Element(world_map_css))
    
    freq_values = world_map['Frequency'].dropna()
    bins = list(freq_values.quantile([0, 0.2, 0.4, 0.6, 0.8, 1.0]))
    # Add choropleth layer with custom styling and highlight
    folium.Choropleth(
        geo_data=world_map,
        data=world_map,
        columns=['Country', 'Frequency'],
        key_on='feature.properties.Country',
        fill_color='viridis',
        fill_opacity=0.75,
        line_opacity=1,
        line_color='white',
        line_weight=1.5,
        legend_name='Relative Frequency',
        nan_fill_color='lightgrey',
        nan_fill_opacity=0.7,
        bins = bins,
        # reset = True
    ).add_to(m)

    style_function = lambda x: {
        'fillColor': 'transparent',
        'color': 'black',
        'weight': 1.5,
        'fillOpacity': 0
    }
    
    highlight_function = lambda x: {
        'fillColor': '#fcf7f7',
        'color': '#0a0a0a',
        'fillOpacity': 0.5,
        'weight': 3
    }
    
    folium.GeoJson(
        world_map,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['Country', 'Language', 'Words_Display', 'Frequency_Display'],
            aliases=['Country:', 'Language:', 'Words:', 'Frequency:'],
            sticky=False
        ),
        popup=folium.GeoJsonPopup(
            fields=['Country', 'Language', 'Words_Display', 'Frequency_Display'],
            aliases=['Country:', 'Language:', 'Words:', 'Frequency:']
        )
    ).add_to(m)
    
    # Display with cleaner settings
    st_folium(
        m, 
        width=None,
        height=600,
        returned_objects=[],
        use_container_width=True
    )



def create_timeseries(final_df):
    """
    Creates a polished Plotly time series chart with smoothing, 
    interactive language filters, and a range slider.
    """
    
    # --- 1. Data Preprocessing & Smoothing ---
    if final_df.empty:
        print("DataFrame is empty.")
        return go.Figure()

    # Map language codes to display names (Update this dictionary as needed)
    lang_code_to_display = {
        'en': 'English', 'ru': 'Russian', 'fr': 'French', 
        'zh': 'Chinese', 'iw': 'Hebrew', 'es': 'Spanish', 
        'it': 'Italian', 'de': 'German'
    }
    
    df = final_df.copy()
    df['display_language'] = df['language'].map(lambda x: lang_code_to_display.get(x, x))
    
    df['label'] = df.apply(
        lambda x: f"{x['word']} ({x['display_language']})" + (" [SYN]" if x['is_synonym'] == 1 else ""), 
        axis=1
    )

    # Sort by year to ensure the rolling average works correctly
    df = df.sort_values(by=['label', 'year'])

    # Calculate a 5-Year Rolling Average to smooth out the "spikes"
    # This makes the graph look much more like the official Google Ngram viewer
    df['frequency_smooth'] = df.groupby('label')['frequency'].transform(
        lambda x: x.rolling(window=5, min_periods=1).mean()
    )

    # --- 2. Initialize the Figure ---
    fig = go.Figure()

    # Get list of unique languages for the dropdown
    languages = sorted(df['display_language'].unique())

    # --- 3. Add Traces (Lines) ---
    # We iterate through every unique word/label and add it to the plot
    for label, group in df.groupby('label'):
        
        is_synonym = group['is_synonym'].iloc[0]
        language = group['display_language'].iloc[0]
        
        # Style: Main words are solid/thick; Synonyms are dashed/thinner
        line_style = dict(width=3) if is_synonym == 0 else dict(width=1.5, dash='dot')
        opacity = 1.0 if is_synonym == 0 else 0.7

        fig.add_trace(go.Scatter(
            x=group['year'],
            y=group['frequency_smooth'],
            mode='lines',
            name=label,
            line=line_style,
            opacity=opacity,
            # Store metadata for the filter logic
            meta={'language': language, 'is_synonym': is_synonym},
            hovertemplate=(
                "<b>%{text}</b><br>" +
                "Year: %{x}<br>" +
                "Freq: %{y:.2e}<extra></extra>"
            ),
            text=group['word'] # For the tooltip
        ))
    
    buttons = []
    
    # Option 1: "All Languages"
    buttons.append(dict(
        label="All Languages",
        method="update",
        args=[{"visible": [True] * len(fig.data)}]
    ))
    
    # Options for each specific language
    for lang in languages:
        # Generate a True/False list for traces that match this language
        visibility = [trace.meta['language'] == lang for trace in fig.data]
        
        buttons.append(dict(
            label=lang,
            method="update",
            args=[{"visible": visibility}]
        ))

    # Add the menu to the layout
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.2, # Position of the dropdown
                xanchor="left",
                y=1.17,
                yanchor="top",
                bgcolor="#2b2b2b", # Dark button background
                font=dict(color="white")
            )
        ]
    )
    # --- 5. Final Layout Polish (Dark Theme) ---
    fig.update_layout(
        template="plotly_dark", # Matches your screenshot's dark theme
        title={
            'text': "Word Frequency Over Time (Smoothed)",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Year",
        yaxis_title="Frequency (5-Year Moving Avg)",
        
        # The Range Slider (The mini-graph at the bottom)
        xaxis=dict(
            rangeslider=dict(visible=True),
            # thickness=0.05, 
            type="date" if pd.api.types.is_datetime64_any_dtype(df['year']) else "linear"
        ),
        showlegend=True,
                
        # Legend positioning
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(0,0,0,0)" # Transparent legend
        ),
        
        # Add annotation for the Dropdown
        annotations=[
            dict(text="Filter Language:", x=0, y=1.13, xref="paper", yref="paper", showarrow=False, font=dict(size=14))
        ],
        
        height=600 # Good height for viewing
    )

    return fig