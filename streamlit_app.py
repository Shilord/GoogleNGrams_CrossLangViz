import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Linguistic Trends Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

alt.themes.enable("dark")

st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_mock_map_data():
    data = {
        'country': ['USA', 'Canada', 'Brazil', 'France', 'Germany', 'Russia', 'China', 'Australia', 'India', 'Argentina'],
        'iso_alpha': ['USA', 'CAN', 'BRA', 'FRA', 'DEU', 'RUS', 'CHN', 'AUS', 'IND', 'ARG'],
        'usage_frequency': np.random.randint(100, 10000, 10)
    }
    return pd.DataFrame(data)

@st.cache_data
def get_mock_time_series():
    years = list(range(1600, 2023))
    val = 50
    values = []
    for y in years:
        change = np.random.randint(-5, 7)
        val = max(0, val + change)
        values.append(val)
    return pd.DataFrame({'year': years, 'frequency': values})


def make_world_map(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(
        input_df, 
        locations=input_id, 
        color=input_column, 
        locationmode="ISO-3", 
        color_continuous_scale=input_color_theme,
        range_color=(0, max(input_df[input_column])),
        scope="world",
        labels={'usage_frequency':'Frequency'}
    )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        width = 500 
    )
    return choropleth

def make_time_series(input_df):
    chart = alt.Chart(input_df).mark_area(
        line={'color':'#29b5e8'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='#29b5e8', offset=0),
                   alt.GradientStop(color='rgba(41, 181, 232, 0)', offset=1)],
            x1=1, x2=1, y1=1, y2=0
        )
    ).encode(
        x=alt.X('year:O', axis=alt.Axis(title="Year", labelAngle=0)),
        y=alt.Y('frequency:Q', axis=alt.Axis(title="Ngram Frequency")),
        tooltip=['year', 'frequency']
    ).properties(
        title='Usage Over Time',
        height=300
    )
    return chart

st.title('Exploring Multicultural Linguistic Trends Through Google Ngrams')
st.markdown('---')

input_col1, input_col2, input_col3 = st.columns([2, 2, 1], gap="large")

with input_col1:
    target_word = st.text_input("Enter Keyword", value="example")
    
    year_range = st.slider(
        "Select Year Range",
        min_value=1600,
        max_value=2022,
        value=(1900, 2022)
    )

with input_col2:
    languages = ['English', 'Chinese', 'French', 'German', 'Hebrew', 'Italian', 'Russian', 'Spanish']
    selected_langs = st.multiselect("Select Languages", languages, default=['English'])

with input_col3:
    st.write("Include Synonyms?")
    synonyms = st.radio("Synonyms", ["Yes", "No"], horizontal=True, label_visibility="collapsed")



st.markdown("### Global Prevalence")


df_map = get_mock_map_data()
map_theme = 'plasma' 

map_chart = make_world_map(df_map, 'iso_alpha', 'usage_frequency', map_theme)
st.plotly_chart(map_chart, use_container_width=True)

st.markdown("---")

col_bottom = st.columns((2, 1), gap='medium')

with col_bottom[0]:
    st.markdown("#### Historical Frequency Trends")
    df_ts = get_mock_time_series()
    df_ts_filtered = df_ts[(df_ts['year'] >= year_range[0]) & (df_ts['year'] <= year_range[1])]
    
    time_chart = make_time_series(df_ts_filtered)
    st.altair_chart(time_chart, use_container_width=True)

with col_bottom[1]:
    st.markdown("#### Associated Word Cloud")

    
    st.info(f"Word Cloud for term: **'{target_word}'**")
    
    mock_words = pd.DataFrame({
        'word': ['linguistics', 'trends', 'data', 'culture', 'history', 'analysis', 'google', 'books'],
        'value': [100, 80, 65, 45, 40, 30, 25, 20]
    })
    
    cloud_placeholder = alt.Chart(mock_words).mark_text().encode(
        x=alt.X('value:Q', axis=None),
        y=alt.Y('word:N', axis=None, sort='-x'),
        size=alt.Size('value:Q', legend=None, scale=alt.Scale(range=[15, 50])),
        color=alt.Color('value:Q', legend=None, scale=alt.Scale(scheme='blues'))
    ).properties(height=250).configure_view(strokeWidth=0)
    
    st.altair_chart(cloud_placeholder, use_container_width=True)


with st.expander('About this Dashboard'):
    st.write('''
        - **Data Source**: Google Ngrams Viewer (Mock data used for UI demo).
        - **Map**: Visualizes the prevalence of the term across different linguistic regions.
        - **Time Series**: Shows the frequency of the term from 1600 to 2022.
    ''')
