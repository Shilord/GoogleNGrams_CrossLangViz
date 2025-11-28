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
import detectlanguage
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

languages = ['English', 'Chinese', 'French', 'German', 'Italian', 'Russian', 'Spanish']
#Add to secrets
detectlanguage.configuration.api_key = "2f804e5b6f76b1bacb52d2ad6667f374"

MIN_YEAR = 1600
MAX_YEAR = 2022

NGRAM_API_URL = "https://books.google.com/ngrams/json" # API endpoint

lang_code_to_display = {
        'en': 'English', 'ru': 'Russian', 'fr': 'French', 
        'zh': 'Chinese', 'es': 'Spanish', 
        'it': 'Italian', 'de': 'German'
    }
lang_to_lang_translation = {'English':'en', 
                            'Chinese': 'zh-CN', 
                            'French':'fr', 
                            'German':'de', 
                            'Italian':'it',
                            'Russian':'ru', 
                            'Spanish':'es'}

LANGUAGE_COLORS_MAP = {
    'English': '#F4D03F',   # Soft Gold
    'Spanish': '#FF6B6B',   # Pastel Coral Red
    'French':  '#54A0FF',   # Sky Blue (High contrast against dark bg)
    'German':  '#9B59B6',   # Amethyst
    'Italian': '#FF9F43',   # Muted Orange
    'Russian': '#00D2D3',   # Turquoise
    'Chinese': '#2ECC71',   # Emerald Green
}

lang_to_translation = {'English':'English', 
                            'Chinese': '中文', 
                            'French':'Français', 
                            'German':'Deutsch', 
                            'Italian':'Italiano',
                            'Russian':'Русский', 
                            'Spanish':'Español'}

lang_to_translation_inverse = {v:k for k,v in lang_to_translation.items()}


#Detect language of input word
def detect_language(word):
    return detectlanguage.detect_code(word)

# sets parameters for API call
def set_params(word, corpus, min_year, max_year):
    params = {'content': word,
              'year_start': min_year,
              'year_end': max_year,
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
    years = list(range(MIN_YEAR, MAX_YEAR + 1))
    expected_len = len(years)
    all_data_frames = []

    for i in range(len(df)):
        freq = []
        response = requests.get(NGRAM_API_URL, params = set_params(df['word'][i], df['language'][i],MIN_YEAR,MAX_YEAR), timeout = 30)
        if response.status_code == 200:
            x = response.json()
            if x:
                freq = x[0]['timeseries']
            else:
                print(f"API Error for {df['word'][i]}: Status {response.status_code}")

        current_len = len(freq)
        if current_len == 0:
            freq = [0] * expected_len
        elif current_len < expected_len:
            # Pad the end with zeros if API returned incomplete data
            freq = freq + ([0] * (expected_len - current_len))
        elif current_len > expected_len:
            # Slice if API returned too much data
            freq = freq[:expected_len]
        temp_df = pd.DataFrame({
            'word': df['word'][i],
            'language': df['language'][i],
            'year': years,
            'frequency': freq
        })
        all_data_frames.append(temp_df)

    if all_data_frames:
        return pd.concat(all_data_frames, ignore_index=True)
    else:
        return pd.DataFrame()

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
    freq_year['display_name'] = freq_year['language'].map(lambda x: lang_to_translation[lang_code_to_display[x]])
    
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

        trace_color = LANGUAGE_COLORS_MAP.get(language, 'white')

        if is_synonym == 0:
            line_style = dict(width=3, color=trace_color)
            opacity = 1.0
        else:
            line_style = dict(width=1.5, dash='dot', color=trace_color)
            opacity = 0.7

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
            y=1,
            xanchor="right",
            x=1.2,
            bgcolor="rgba(0,0,0,0)" # Transparent legend
        ),
        
        # Add annotation for the Dropdown
        annotations=[
            dict(text="Filter Language:", x=0, y=1.13, xref="paper", yref="paper", showarrow=False, font=dict(size=14))
        ],
        
        height=600 # Good height for viewing
    )

    return fig

def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """Assigns color based on the word's assigned language, which is stored in kwargs."""
    language = kwargs.get('language', 'English') # Default to English if not found
    return LANGUAGE_COLORS_MAP.get(language, 'gray') # Default to gray if language not in map

def create_word_cloud(final_df, year_range):
    """
    Generates a language-colored WordCloud with a transparent background
    and adjusted figure size to match the timeseries plot.
    """
    if final_df.empty:
        st.info("No data available to generate word cloud.")
        return None, pd.DataFrame()

    lang_to_lang_translation_inverse = {v:k for k,v in lang_to_lang_translation.items()}
    df = final_df.copy()
    df['display_language'] = df['language'].map(lambda x: lang_to_lang_translation_inverse.get(x, x))
    df = df.loc[df['year']==year_range]

    word_freq_max = df.groupby(['word', 'display_language']).agg(
        max_frequency=('frequency', 'max')
    ).reset_index()

    word_freq_max = word_freq_max[word_freq_max['max_frequency'] > 1e-9]
    
    data_for_display = word_freq_max.sort_values(by='max_frequency', ascending=False).head(20).copy()
    data_for_display['Color'] = data_for_display['display_language'].map(lambda x: LANGUAGE_COLORS_MAP.get(x, 'gray'))
    data_for_display = data_for_display.rename(columns={'word': 'Word', 'max_frequency': 'Max Frequency', 'display_language': 'Language'})
    data_for_display['Max Frequency'] = data_for_display['Max Frequency'].apply(lambda x: f"{x:.6e}")
    data_for_display = data_for_display[['Word', 'Language', 'Max Frequency', 'Color']]

    word_to_language_map = word_freq_max.set_index('word')['display_language'].to_dict()
    freq_dict = word_freq_max.set_index('word')['max_frequency'].to_dict()

    
    def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        language = word_to_language_map.get(word, 'English') 
        return LANGUAGE_COLORS_MAP.get(language, 'gray')

    
    wc = WordCloud(
        font_path = 'assets/NotoSansSC-Regular.ttf',
        width=800, 
        height=500, # Height matches the timeseries plot (500px)
        background_color='#0d1118', # Crucial step 1: Tell WordCloud not to draw a background
        max_words=100,
        normalize_plurals=False
    ).generate_from_frequencies(freq_dict)
    
    wc.recolor(color_func=custom_color_func)

    fig, ax = plt.subplots(figsize=(10, 6.25)) 
    
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0.0)
    
    ax.patch.set_facecolor('none')
    ax.patch.set_alpha(0.0)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True) 
    plt.close(fig) 
    
    # Reset Matplotlib style to default
    plt.style.use('default') 

    # Return the image buffer for display and the DataFrame for the table
    return buf


def create_frequency_map_plotly(world_map, final_df, year):
    """
    Generates a clean, professional world map colored by relative frequency using Plotly.
    """
    
    if final_df.empty:
        st.info("Press 'Run Linguistic Search' to generate the initial visualizations.")
        return None

    freq_year = final_df[final_df['year'] == year].copy()
    
    if freq_year.empty:
        st.warning(f"No data available for year {year}")
        return None
    
    target_languages = [
        'English', 'Español', 'Français', 'Deutsch', 
        'Italiano', 'Русский', '中文', 'עִברִית'
    ]
    
    # Create display_name column
    freq_year['display_name'] = freq_year['language'].map(lambda x: lang_to_translation[lang_code_to_display[x]])
    
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
    
    # Split into supported and unsupported languages
    map_supported = world_map[world_map['Frequency'].notna()].copy()
    map_unsupported = world_map[world_map['Frequency'].isna()].copy()
    map_unsupported['Frequency'] = 0

    map_supported['Language'] = [lang_to_translation_inverse[i] for i in list(map_supported['Language'])]
    
    # Create the plotly figure
    fig = go.Figure()
    
    # Add choropleth for supported languages
    fig.add_trace(go.Choropleth(
        locationmode='country names',
        locations=map_supported['Country'],
        z=map_supported['Frequency'],
        colorscale='Viridis',
        reversescale=False,
        autocolorscale=False,
        marker_line_color='black',
        marker_line_width=1.5,
        colorbar=dict(
            title='Relative Frequency',
            title_side='top',
            xanchor='left',
            x=1.02,
            y=0.5,
            len=0.7,
            thickness=15,
        ),
        customdata=list(zip(
            map_supported['Words_Display'],
            map_supported['Language'],
            map_supported['Frequency_Display']
        )),
        hovertemplate='<b>Country:</b> %{location}<br>' 
            '<b>Language:</b> %{customdata[1]}<br>' 
            '<b>Words:</b> %{customdata[0]}<br>' 
            '<b>Frequency:</b> %{customdata[2]}<extra></extra>',
        name='Supported Languages'
    ))
    
    # Add choropleth for unsupported languages
    fig.add_trace(go.Choropleth(
        locationmode='country names',
        locations=map_unsupported['Country'],
        z=map_unsupported['Frequency'],
        showscale=False,
        colorscale=[[0, 'lightgrey'], [1, 'lightgrey']],
        marker_line_color='black',
        marker_line_width=1.5,
        customdata=list(zip(
            map_unsupported['Words_Display'],
            map_unsupported['Language']
        )),
        hovertemplate='<b>Country:</b> %{location}<br>' 
            '<b>Language:</b> %{customdata[1]}<br>' 
            '<b>Words:</b> %{customdata[0]}<br>' 
            '<b>Frequency:</b> Unsupported Language<extra></extra>',
        name='Unsupported Languages',
        # hoverinfo='skip'
    ))
    
    # Update layout
    fig.update_layout(
        # title={
        #     'text': f'World Map Ngram Frequency - Year {year}',
        #     'x': 0.5,
        #     'xanchor': 'center',
        #     'y': 0.95,
        #     'xref': 'paper',
        #     'font': {'size': 20, 'color': 'white'}
        # },
        autosize=True,
        geo=dict(
            scope='world',
            showframe=False,
            showcoastlines=False,
            showlakes=False,
            projection_type='natural earth',
            projection_scale=1.1, 
            bgcolor='#0e1117',
            showland=True,
            landcolor='#262730',
            coastlinecolor='black',
            coastlinewidth=1
        ),
        annotations=[dict(
            x=0.5,
            y=-0.05,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://resourcewatch.org/data/explore/soc_071_world_languages" style="color: #1f77b4;">CIA World Factbook (2015)</a>',
            showarrow=False,
            font=dict(color='white', size=10)
        )],      
        font=dict(color='white'),
        paper_bgcolor='#0e1117',
        height=600,
        margin=dict(l=0, r=0, t=30, b=10, pad = 0),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    fig.update_traces(
        selector=dict(type='choropleth'),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_color="black",
            bordercolor="black"
        )
    )
    
    return fig

