import streamlit as st
from utils import *
from typing import Literal
from tooltips import *


MARGINS = {
    "top": "3.73rem",
    "bottom": "0",
}

STICKY_CONTAINER_HTML = """
<style>
div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown div.fixed-header-{i}) {{
    position: sticky;
    {position}: {margin};
    background-color: #0d1118;
    z-index: 999;
    border: 1px solid #262730;
    border-radius: 0.8rem;
    
    /* Padding now applies only to this specific box */
    padding-left: 2rem;
    padding-bottom: 1rem;
    padding-top: 1rem;
    padding-right: 1rem;
}}
</style>
<div class='fixed-header-{i}'/>
""".strip()

EQUAL_HEIGHT_CSS = """
<style>
/* 1. Fix Height for Alignment */
.equal-height-container {
    height: 600px !important;  /* Locks the height of the container */
    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* 2. Fix Unnecessary Space Below Subheaders (APPLIED TO ALL H3 HEADERS) */
/* This targets all st.subheader elements and removes their default bottom margin. */
section.main [data-testid="stVerticalBlock"] h3 {
    margin-bottom: -15px !important; 
    padding-bottom: 0px !important; 
}

/* 3. FINAL WORDCLOUD HEIGHT LOCK: Force the image element to fill the container height */
.equal-height-container img {
    height: 100% !important; 
    object-fit: contain; 
}
</style>
"""

# Not to apply the same style to multiple containers
count = 0

def sticky_container(
    *,
    height: int | None = None,
    border: bool | None = None,
    mode: Literal["top", "bottom"] = "top",
    margin: str | None = None,
):
    if margin is None:
        margin = MARGINS[mode]

    global count
    html_code = STICKY_CONTAINER_HTML.format(position=mode, margin=margin, i=count)
    count += 1

    # --- CRITICAL FIX ---
    # 1. If height is None, we use a standard container (no border by default).
    #    We do NOT pass 'height=None' or 'border=False' to avoid the StreamlitInvalidHeightError.
    if height is None:
        container = st.container()
        
    # 2. If height IS a number, we create a scrolling container and explicitly turn off the native border.
    else:
        container = st.container(height=height, border=False)

    container.markdown(html_code, unsafe_allow_html=True)
    return container

def custom_subheader(text, help_text=None):
    st.markdown("""
    <style>
    .custom-subheader {
        color: #ffffff;
        font-size: 1.75rem;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 6px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    """Custom subheader matching st.subheader styling with optional help tooltip"""
    st.markdown(
        f"<div class='custom-subheader'>{text}</div>",
        unsafe_allow_html=True,
        help=help_text     # Streamlit tooltip still works
    )

def show_dashboard():
        
    languages = ['English', 'Chinese', 'French', 'German', 'Italian', 'Russian', 'Spanish']

    input_language = None

    if 'search_just_completed' not in st.session_state:
        st.session_state['search_just_completed'] = False
    
    # Auto-collapse controls when search just completes
    if st.session_state.get('search_just_completed', False):
        st.session_state.toggle_controls = False
        st.session_state['search_just_completed'] = False 

    if 'app_initialized' not in st.session_state:
        default_df = pd.read_csv("example_data.csv") 
        st.session_state['final_data'] = default_df
        st.session_state['search_run'] = True 
        st.session_state.target_word = "example" 
        st.session_state.input_language = "Auto Detect"
        st.session_state.selected_languages = ['English', 'Chinese', 'French', 'German', 'Italian', 'Russian', 'Spanish']
        st.session_state.synonyms_choice = "Yes"
        st.session_state.num_synonyms = 3
        st.session_state.pos_tag = "None"
        st.session_state.context_topics = ""
        st.session_state['is_comparison'] = False
        st.session_state['is_phrase']=False

    if 'search_run' not in st.session_state:
        st.session_state['search_run'] = False
    if 'final_data' not in st.session_state:
        # Initialize with mock data structure or None
        st.session_state['final_data'] = pd.DataFrame() 

    if 'controls_expanded' not in st.session_state:
        st.session_state.controls_expanded = True
    if 'target_word' not in st.session_state:
        st.session_state.target_word = ""
    if 'input_language' not in st.session_state:
        st.session_state.input_language = "English"
    if 'pos_tag' not in st.session_state:
        st.session_state.pos_tag = "None"
    if 'context_topics' not in st.session_state:
        st.session_state.context_topics = ""
    if 'selected_languages' not in st.session_state:
        st.session_state.selected_languages = ['English']
    if 'synonyms_choice' not in st.session_state:
        st.session_state.synonyms_choice = "No"
    if 'num_synonyms' not in st.session_state:
        st.session_state.num_synonyms = 3
    if 'app_initialized' not in st.session_state:
        st.session_state.app_initialized = 1

    #Build world map
    @st.cache_resource
    def load_empty_map():
        map = pd.read_csv('empty_map.csv')
        return map

    empty_map = load_empty_map()
    
    load_css('assets/styles.css')

    # Styling then writing title
    st.markdown("""
    <style>
    .title {
        color: #ffffff;
        margin-top: 0px;
        margin-bottom: 10px;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)
    st.markdown("""
                    <div class="title">
                        Words Across Borders
                    </div>
                    """, unsafe_allow_html=True)
    
    #Subtitle
    st.markdown(
        '''
        <p style="font-size: 18px; color: #a8a8a8; text-align: center">
            Visualizing word frequencies over time and space via Google N-grams. An interactive exploration of the historical popularity of words, mapping their trends across languages to reveal the shifting landscape of human thought. See 
            <a href="?tab=User Manual" target="_self" style="color: #4da6ff; text-decoration: none;">
                User Manual
            </a>
        </p>
        ''', 
        unsafe_allow_html=True
    )

    with sticky_container(mode="top", border=True):
        # Header with toggle button
        col_header, col_toggle = st.columns([0.9, 0.1], vertical_alignment="bottom")
        with col_header:
            st.subheader("Search Controls",anchor = False, help='Start your query by playing with these controls.')
            
        with col_toggle:
            # st.write("")
            if st.session_state.get('toggle_controls', True):  # Read from key
                label = "▲ Collapse"
            else:
                label = "▼ Expand"
            st.checkbox(
                label,
                value=st.session_state.get('toggle_controls', True),
                key="toggle_controls",
                label_visibility="visible"
            )

        
        if st.session_state.get('toggle_controls', True):
            col_keyword, col_expander = st.columns([3, 1])

            with col_keyword:
                target_word = st.text_input(
                    "Enter Keyword",
                    value=st.session_state.target_word,
                    key="target_word_input",
                    label_visibility="hidden", 
                    placeholder="Enter a word or phrase as the search term here."
                )
                st.session_state.target_word = target_word

            with col_expander:
                with st.expander("Add More Context (Optional)"):
                    language_options = ['Auto Detect'] + languages
                    input_language = st.selectbox(
                        "Input Language",
                        language_options,
                        index=language_options.index(st.session_state.input_language) if st.session_state.input_language in language_options else 0,
                        key="input_language_select",
                        help="The language of the word which you inputted. More accurate settings assigned here leads to better synonym and translation results."
                    )
                    st.session_state.input_language = input_language
                    
                    pos_tag = st.selectbox(
                        "Part of Speech", 
                        ['None', 'Noun', 'Adjective', 'Verb', 'Adverb'],
                        index=['None', 'Noun', 'Adjective', 'Verb', 'Adverb'].index(st.session_state.pos_tag),
                        key="pos_tag_select",
                        help="Filter the search term by its grammatical role (e.g., searching 'run' only as a Verb)."
                    )
                    st.session_state.pos_tag = pos_tag
                    st.markdown("<div style='margin-top: 0.65rem;'></div>", unsafe_allow_html=True)

                    
                    context_topics = st.text_input(
                        "Context Topics",
                        value=st.session_state.context_topics,
                        key="context_topics_input",
                        placeholder="e.g., finance, technology",
                        help="A list of words that set the theme or context to narrow the search scope for the main search term (e.g., 'medicine' or '19th century art')."
                    )
                    st.session_state.context_topics = context_topics

            st.subheader("Language and Synonym Settings",anchor = False)
            col_lang, col_synonym_toggle, col_num_synonyms = st.columns([3.5, 1.5, 1]) 
            
            def update_language_state():
                """Reads the current widget value and saves it to session_state."""
                st.session_state['selected_languages'] = st.session_state['lang_select_widget']
            
            with col_lang:
                ALL_LANGUAGES_OPTION = "All Languages"
                options_list = [ALL_LANGUAGES_OPTION] + languages

                if ALL_LANGUAGES_OPTION in st.session_state['selected_languages'] and len(st.session_state['selected_languages']) != len(languages):
                    st.session_state['selected_languages'] = languages

                selected_langs = st.multiselect(
                    "Select Languages", 
                    options_list, 
                    default=st.session_state['selected_languages'], 
                    on_change=update_language_state,
                    key='lang_select_widget',
                    help='Select which languages to be included in the analysis.')
                    

                if ALL_LANGUAGES_OPTION in selected_langs:
                    filter_langs = languages 
                else:
                    filter_langs = [lang for lang in selected_langs if lang != ALL_LANGUAGES_OPTION]
                
                # Store filter_langs in session state for later use
                st.session_state['filter_langs'] = filter_langs

            with col_synonym_toggle:
                #st.write("Include Synonyms?")
                synonyms_choice = st.radio(
                    "Include Synonyms?",
                    ["Yes", "No"],
                    index=0 if st.session_state.synonyms_choice == "Yes" else 1,
                    horizontal=True,
                    #label_visibility="collapsed",
                    key="synonym_radio_input",
                    help='Selecting yes may better capture the various meanings or context of your search term, whereas selecting no results in the singular most direct translation.'
                )
                st.session_state.synonyms_choice = synonyms_choice

            # Conditional Input for Number of Synonyms
            num_synonyms = 0
            if st.session_state.synonyms_choice == "Yes":
                with col_num_synonyms:
                    #st.caption("Synonyms Count") 
                    num_synonyms = st.number_input(
                        "Synonyms Count",
                        min_value=1,
                        max_value=20,
                        value=st.session_state.num_synonyms,
                        step=1,
                        #label_visibility="collapsed",
                        key="num_synonyms_number_input",
                        help="Maximum number of related synonyms to include in the search."
                    )
                    st.session_state.num_synonyms = num_synonyms
            else:
                with col_num_synonyms:
                    st.write("") 

            # Search button (always visible, inside sticky header)
            _,col_btn, _ = st.columns([1, 1, 1])
            with col_btn:
                search_button = st.button(
                    "Run Linguistic Search", 
                    type="primary", 
                    use_container_width=True,
                    key="search_run_button"
                )
        else:
            # When collapsed, set search_button to False
            search_button = False

    target_word = st.session_state.target_word
    input_language = st.session_state.input_language
    pos_tag = st.session_state.pos_tag
    context_topics = st.session_state.context_topics
    filter_langs = st.session_state.get('filter_langs', languages)
    synonyms_choice = st.session_state.synonyms_choice
    num_synonyms = st.session_state.num_synonyms if st.session_state.synonyms_choice == "Yes" else 0

    
    @timeit
    @st.cache_data
    def get_synonyms_and_translations(target_word,num_synonyms,context_topics,pos_tag,input_language,selected_langs,is_phrase):
        target_word = target_word.lower()
        print(f"ABC:{input_language}")
        #If target word is not in english, we just find translation of the word in english then proceed as usual
        if input_language!='en':
            trans_df = get_languages(target_word, input_language, ['en'])
            if not trans_df.empty and 'en' in trans_df['language'].values:
                target_word = trans_df.loc[trans_df['language']=='en', 'word'].iloc[0]
                print(f"Word translated to English: {target_word}")
                if lang_code_to_display[input_language] not in selected_langs:
                    selected_langs.append(lang_code_to_display[input_language])
                input_language = 'en'
            else:
                print("Translation to English failed. Proceeding without synonyms.")



        #If target word is in english, then just find synonyms then do translations of each word
        #Find synonyms of target word
        if synonyms_choice=='Yes' and is_phrase==False:
            synonyms = get_synonyms(target_word,num_synonyms,context_topics,pos_tag)
            print(f"Synonyms: {synonyms}")
        else:
            synonyms = []

        # Find translations in 7 languages for all words and synonyms (no batch translations)
        # all_dfs = []
        # for word in [target_word]+synonyms:
        #     is_synonym_flag = 1 if word != target_word else 0
        #     translations_df = get_translations(word,input_language,[lang_to_lang_translation[i] for i in selected_langs])
        #     translations_df['is_synonym'] = is_synonym_flag
        #     all_dfs.append(translations_df)

        # raw_final_df = pd.concat(all_dfs, ignore_index=True)
        #For batch translations

        word_list = [target_word] + synonyms
        translations_df = get_translations_batch(word_list, input_language, [lang_to_lang_translation[i] for i in selected_langs])
        translations_df['word'] = translations_df['word'].str.lower()
        translations_df['is_synonym'] = translations_df['word'].apply(
            lambda w: 0 if w == target_word else 1
        )
        raw_final_df = translations_df

        dedup_df = raw_final_df.sort_values(by='is_synonym', ascending=True)

        final_df = dedup_df.drop_duplicates(
            subset=['word', 'language', 'year'], 
            keep='first'
        )
        return final_df
    if search_button:
        try:
            st.session_state['search_just_completed'] = True  
            if len(target_word.strip().split(','))>1:
                st.session_state['is_phrase'] = False
                st.session_state['is_comparison'] = True
            elif len(target_word.strip().split(' '))>1:
                st.session_state['is_phrase'] = True
                st.session_state['is_comparison'] = False
            else:
                st.session_state['is_phrase'] = False
                st.session_state['is_comparison'] = False

            #Detect language of input keyword
            if st.session_state['is_comparison']==False:
                if input_language=='Auto Detect':
                    input_language = detect_language(target_word)
                else: 
                    #Convert input language from format "English" to 'en'
                    lang_code_to_display_inverse = {v:k for k,v in lang_code_to_display.items()}
                    input_language = lang_code_to_display_inverse[input_language]
            else:
                input_language = 'en'
            if input_language not in list(lang_code_to_display.keys()):
                input_language = 'en'
            print("Detected Language:" + input_language)

            if st.session_state['is_comparison']==False:
                with st.spinner('Running linguistic search...'):
                    st.session_state['final_data'] = get_synonyms_and_translations(target_word,num_synonyms,context_topics,pos_tag,input_language,filter_langs,st.session_state['is_phrase'])
            else: 
                target_words =  [i.strip() for i in target_word.strip().split(',')]
                with st.spinner('Running linguistic search...'):
                    df = pd.DataFrame()
                    for word in target_words:
                        df = pd.concat([df,get_synonyms_and_translations(word,num_synonyms,None,None,input_language,filter_langs,st.session_state['is_phrase'])],ignore_index=True)
                    st.session_state['final_data'] = df

            st.session_state['search_run'] = True 
            st.rerun()
               
        except ValueError as e:
            st.session_state['search_run'] = False
            st.session_state['search_just_completed'] = False
            st.error(f"Validation Error: {e}")

    if st.session_state['search_run']:
        if st.session_state['is_comparison']==False:
            st.subheader("Historical Date Filter",anchor = False)
            year_range = st.slider(
                "Select Target Year",
                min_value=MIN_YEAR,
                max_value=MAX_YEAR,
                value=2000, 
                step=1,
                help="Select a year for analysis."
            )

            world_map = empty_map.copy(deep=True)

            custom_subheader(f"Interactive World Heatmap for Word Frequencies - Year {year_range}",help_text = world_map_tooltip)

            fig = create_frequency_map_plotly(world_map, st.session_state['final_data'], year_range)
            if fig:
                st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': True})

            col_chart_left, col_chart_right = st.columns([1, 1])

            # --- START BAR CHART INTEGRATION ---
            # 1. Capture all three return values from create_word_cloud
            word_cloud_image_buffer, wc_df, fig_bar = create_word_cloud(st.session_state['final_data'], year_range=year_range)
            # --- END BAR CHART INTEGRATION ---

            with col_chart_left:
                custom_subheader(f"Bar Graph: Frequencies by Language - Year {year_range}",help_text = bar_graph_tooltip)
                # 2. Display the Plotly Bar Chart
                if fig_bar:
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.text("Bar Graph here") # This will now be replaced by the chart if data exists

            with col_chart_right:
                custom_subheader(f"Word Cloud: Words by Frequency - Year {year_range}",help_text = word_cloud_tooltip)
                if word_cloud_image_buffer:
                    st.image(word_cloud_image_buffer, use_container_width=True)
        
       
        # _,col2,_ = st.columns([0.3,0.5,0.05])
        # with col2: 
        custom_subheader(f"Time Series: Word Frequency Over Time",help_text = timeseries_tooltip)
        time_chart = create_timeseries(st.session_state['final_data'])
        st.plotly_chart(time_chart, use_container_width=True)