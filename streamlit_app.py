import streamlit as st
from utils import *

st.set_page_config(
    page_title="Linguistic Trends Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# from streamlit_extras.stylable_container import stylable_container


if 'search_run' not in st.session_state:
    st.session_state['search_run'] = False
if 'final_data' not in st.session_state:
    # Initialize with mock data structure or None
    st.session_state['final_data'] = pd.DataFrame() 

#Build world map
@st.cache_resource
def load_empty_map():
    empty_map = gpd.read_file("soc_071_world_languages.zip") 
    empty_map['geometry'] = empty_map['geometry'].simplify(tolerance=0.03, preserve_topology=True)

    # Cleaning map data
    empty_map = empty_map.loc[:, ['COUNTRY', 'FIRST_OFFI', 'geometry']]
    empty_map = empty_map.rename(columns={'COUNTRY': 'Country', 'FIRST_OFFI': 'Primary Language (based on 2015)'})
    empty_map['Primary Language (based on 2015)'] = empty_map['Primary Language (based on 2015)'].replace({'English': 'English', 'Spanish': 'Español', 'French': 'Français', 'German': 'Deutsch', 'Italian': 'Italiano', 'Russian': 'Русский', 'Standard Chinese or Mandarin': '中文', 'Hebrew': 'עִברִית'})
    map = empty_map.copy(deep=True)
    return map

empty_map = load_empty_map()

load_css('assets/styles.css')


st.title('Exploring Multicultural Linguistic Trends Through Google Ngrams')


col_keyword, col_expander = st.columns([3, 1])

with col_keyword:
    target_word = st.text_input(
        "Enter Keyword", 
        # value="example", 
        label_visibility="hidden", 
        placeholder="Enter Keyword"
    )

with col_expander:
    with st.expander("Add Context"):
        context_topics = st.text_input(
            "Context Topics",
            placeholder="e.g., finance, technology",
            # label_visibility="collapsed",
            help="A list of words that set the theme or context to narrow the search scope for the main keyword (e.g., 'medicine' or '19th century art') ."
        )
        pos_tag = st.selectbox(
            "Part of Speech", 
            ['None', 'Noun', 'Adjective', 'Verb', 'Adverb'],
            # index=0,
            # label_visibility="collapsed",
            help="Filter the keyword by its grammatical role in the corpus (e.g., searching 'run' only as a Verb)."
        )


st.subheader("Language and Synonym Settings")
col_lang, col_synonym_toggle, col_num_synonyms = st.columns([3.5, 1.5, 1]) 
def update_language_state():
    """Reads the current widget value and saves it to session_state."""
    # 'lang_select_widget' is the key assigned to the multiselect below.
    st.session_state['selected_languages'] = st.session_state['lang_select_widget']
with col_lang:
    # languages = ['English', 'Chinese', 'French', 'German', 'Hebrew', 'Italian', 'Russian', 'Spanish']
    # selected_langs = st.multiselect("Select Languages", languages, default=['English'])

    languages = ['English', 'Chinese', 'French', 'German', 'Hebrew', 'Italian', 'Russian', 'Spanish']
    ALL_LANGUAGES_OPTION = "All Languages"

    options_list = [ALL_LANGUAGES_OPTION] + languages

    if 'selected_languages' not in st.session_state:
        st.session_state['selected_languages'] = ['English'] 

    if ALL_LANGUAGES_OPTION in st.session_state['selected_languages'] and len(st.session_state['selected_languages']) != len(languages):
        st.session_state['selected_languages'] = languages

    selected_langs = st.multiselect(
        "Select Languages", 
        options_list, 
        default=st.session_state['selected_languages'], 
        on_change=update_language_state,
        key = 'lang_select_widget')

    if ALL_LANGUAGES_OPTION in selected_langs:
        filter_langs = languages 
    else:
        filter_langs = [lang for lang in selected_langs if lang != ALL_LANGUAGES_OPTION]

with col_synonym_toggle:
    st.write("Include Synonyms?")
    synonyms_choice = st.radio(
        "Synonyms",
        ["Yes", "No"],
        horizontal=True,
        label_visibility="collapsed",
        key="synonym_radio"
    )

# Conditional Input for Number of Synonyms
num_synonyms = 0
if synonyms_choice == "Yes":
    with col_num_synonyms:
        # st.caption is used to create the aligned 'Count' label
        st.caption("Synonyms Count") 
        num_synonyms = st.number_input(
            "Synonyms Count",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
            label_visibility="collapsed",
            key="num_synonyms_input",
            help="Maximum number of related synonyms to include in the search."
        )
else:
    with col_num_synonyms:
        st.write("") 


_,col_btn, _ = st.columns([1, 1, 1])
with col_btn:
    search_button = st.button(
        "Run Linguistic Search", 
        type="primary", 
        use_container_width=True,
        key="search_run_button"
    )

# st.markdown("---")
# st.write(f"**Current Search Word:** `{target_word}`")
# st.write(f"**Context Topics:** `{context_topics or 'None'}` | **POS Tag:** `{pos_tag}`")
# st.write(f"**Languages:** `{', '.join(selected_langs)}`")
# st.write(f"**Include Synonyms:** `{synonyms_choice}` (Count: `{num_synonyms}`)")
# # st.write(f"**Target Year:** `{year_range}`")

@st.cache_data
def get_synonyms_and_translations(target_word,num_synonyms,context_topics,pos_tag,input_language,selected_langs,is_phrase):
    #Find synonyms of target word
    if synonyms_choice=='Yes' and is_phrase==False:
        synonyms = get_synonyms(target_word,num_synonyms,context_topics,pos_tag)
        print(f"Synonyms: {synonyms}")
    else:
        synonyms = []

    #Find translations in 7 languages for all words and synonyms
    all_dfs = []
    for word in [target_word]+synonyms:
        is_synonym_flag = 1 if word != target_word else 0
        translations_df = get_translations(word,input_language,[lang_to_lang_translation[i] for i in selected_langs])
        translations_df['is_synonym'] = is_synonym_flag
        all_dfs.append(translations_df)

    raw_final_df = pd.concat(all_dfs, ignore_index=True)

    dedup_df = raw_final_df.sort_values(by='is_synonym', ascending=True)

    final_df = dedup_df.drop_duplicates(
        subset=['word', 'language', 'year'], 
        keep='first'
    )
    return final_df

if search_button:
    try:
        if len(target_word.strip().split(' '))>1:
            IS_PHRASE = True
        else:
            IS_PHRASE = False
        #Detect language of input keyword
        input_language = detect_language(target_word)
        if input_language not in languages:
            input_language = 'en'
        print("Detected Language:" + input_language)
        st.session_state['final_data'] = get_synonyms_and_translations(target_word,num_synonyms,context_topics,pos_tag,input_language,filter_langs,IS_PHRASE)
        
        st.session_state['search_run'] = True      
    except ValueError as e:
        st.session_state['search_run'] = False
        st.error(f"Validation Error: {e}")

if st.session_state['search_run']:
    st.subheader("Historical Date Filter")
    year_range = st.slider(
        "Select Target Year",
        min_value=1600,
        max_value=2022,
        value=2000, 
        step=1,
        help="Select a single specific year for the corpus analysis."
    )
    world_map = empty_map.copy(deep=True)
    create_frequency_map(world_map, st.session_state['final_data'], year_range)

    col_chart_left, col_chart_right = st.columns([1, 1])

    with col_chart_left:
        time_chart = create_timeseries(st.session_state['final_data'])
        st.plotly_chart(time_chart, use_container_width=True)

    with col_chart_right:
        st.markdown(
            """
            <h3 style='text-align: center; font-size: 20px;'>
                Terms by Max Frequency and Language
            </h3>
            """,
            unsafe_allow_html=True
        )
        word_cloud_image_buffer = create_word_cloud(st.session_state['final_data'], year_range=year_range)
        if word_cloud_image_buffer:
            st.image(word_cloud_image_buffer, use_container_width=True)
