import streamlit as st
from utils import *
from typing import Literal


MARGINS = {
    "top": "3.73rem",
    "bottom": "0",
}

STICKY_CONTAINER_HTML = """
<style>
div[data-testid="stVerticalBlock"] div:has(div.fixed-header-{i}) {{
    position: sticky;
    {position}: {margin};
    background-color: #0d1118;
    z-index: 999;
}}
</style>
<div class='fixed-header-{i}'/>
""".strip()

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

    container = st.container(height=height, border=border)
    container.markdown(html_code, unsafe_allow_html=True)
    return container

# Define the images and initial state for the carousel
# NOTE: Replace these with actual image paths or URLs you want to display!
LOADING_IMAGES = [
    "Loader_images/1.png", 
    "Loaser_images/2.png", 
]

def image_carousel_during_load():
    """Displays a single image with navigation buttons during the loading screen."""
    
    # Use st.empty to create a container that can be dynamically updated inside the spinner
    carousel_container = st.empty()
    
    with carousel_container.container():
        st.caption("Fascinating facts about language while you wait...")
        
        # Determine the image to show
        current_index = st.session_state.current_loading_image_index
        
        if not LOADING_IMAGES:
            st.info("Loading...")
            return carousel_container

        image_to_show = LOADING_IMAGES[current_index]
        
        # Display the image
        st.image(image_to_show, use_column_width=True, caption=f"Image {current_index + 1} of {len(LOADING_IMAGES)}")
        
        # Navigation buttons
        col_back, col_next = st.columns([1, 1])
        
        with col_back:
            if st.button("⬅️ Back"):
                # Rerunning immediately updates the index
                st.session_state.current_loading_image_index = (current_index - 1) % len(LOADING_IMAGES)
                st.experimental_rerun()
        
        with col_next:
            if st.button("Next ➡️"):
                # Rerunning immediately updates the index
                st.session_state.current_loading_image_index = (current_index + 1) % len(LOADING_IMAGES)
                st.experimental_rerun()
        
        return carousel_container


def show_dashboard():
    languages = ['English', 'Chinese', 'French', 'German', 'Italian', 'Russian', 'Spanish']

    input_language = None
    
    # --- FIX 1: Initialize the carousel index at the start of the function ---
    if 'current_loading_image_index' not in st.session_state:
        st.session_state.current_loading_image_index = 0
    # --- END FIX 1 ---


    if 'app_initialized' not in st.session_state:
        default_df = pd.read_csv("example_data.csv") 
        st.session_state['final_data'] = default_df
        st.session_state['search_run'] = True 
        st.session_state.target_word = "example" 
        st.session_state.input_language = "English"
        st.session_state.selected_languages = ['English', 'Chinese', 'French', 'German', 'Italian', 'Russian', 'Spanish']
        st.session_state.synonyms_choice = "Yes"
        st.session_state.num_synonyms = 3
        st.session_state.pos_tag = "Noun"
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

    with sticky_container(mode="top", border=True):
        # Header with toggle button
        col_header, col_toggle = st.columns([0.9, 0.1])
        with col_header:
            st.subheader("Search Controls")
            
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
                    placeholder="Enter Keyword"
                )
                st.session_state.target_word = target_word

            with col_expander:
                with st.expander("Add More Context (Optional)"):
                    input_language = st.selectbox(
                        "Input Language",
                        languages,
                        index=languages.index(st.session_state.input_language) if st.session_state.input_language in languages else 0,
                        key="input_language_select",
                        help="The language of the word which you inputted. More accurate settings assigned here leads to better synonym and translation results."
                    )
                    st.session_state.input_language = input_language
                    
                    pos_tag = st.selectbox(
                        "Part of Speech", 
                        ['None', 'Noun', 'Adjective', 'Verb', 'Adverb'],
                        index=['None', 'Noun', 'Adjective', 'Verb', 'Adverb'].index(st.session_state.pos_tag),
                        key="pos_tag_select",
                        help="Filter the keyword by its grammatical role in the corpus (e.g., searching 'run' only as a Verb)."
                    )
                    st.session_state.pos_tag = pos_tag
                    
                    context_topics = st.text_input(
                        "Context Topics",
                        value=st.session_state.context_topics,
                        key="context_topics_input",
                        placeholder="e.g., finance, technology",
                        help="A list of words that set the theme or context to narrow the search scope for the main keyword (e.g., 'medicine' or '19th century art')."
                    )
                    st.session_state.context_topics = context_topics

            st.subheader("Language and Synonym Settings")
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
                    key='lang_select_widget')

                if ALL_LANGUAGES_OPTION in selected_langs:
                    filter_langs = languages 
                else:
                    filter_langs = [lang for lang in selected_langs if lang != ALL_LANGUAGES_OPTION]
                
                # Store filter_langs in session state for later use
                st.session_state['filter_langs'] = filter_langs

            with col_synonym_toggle:
                st.write("Include Synonyms?")
                synonyms_choice = st.radio(
                    "Synonyms",
                    ["Yes", "No"],
                    index=0 if st.session_state.synonyms_choice == "Yes" else 1,
                    horizontal=True,
                    label_visibility="collapsed",
                    key="synonym_radio_input"
                )
                st.session_state.synonyms_choice = synonyms_choice

            # Conditional Input for Number of Synonyms
            num_synonyms = 0
            if st.session_state.synonyms_choice == "Yes":
                with col_num_synonyms:
                    st.caption("Synonyms Count") 
                    num_synonyms = st.number_input(
                        "Synonyms Count",
                        min_value=1,
                        max_value=20,
                        value=st.session_state.num_synonyms,
                        step=1,
                        label_visibility="collapsed",
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
                if input_language==None:
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
                # --- START LOADING BLOCK WITH CAROUSEL ---
                with st.spinner('Running linguistic search...'):
                    # 1. Start the image carousel immediately
                    carousel_placeholder = image_carousel_during_load()
                    
                    # 2. Run the heavy API task
                    st.session_state['final_data'] = get_synonyms_and_translations(target_word,num_synonyms,context_topics,pos_tag,input_language,filter_langs,st.session_state['is_phrase'])
                
                # 3. Once the 'with st.spinner' block exits (data loaded), clear the carousel.
                carousel_placeholder.empty()
                # --- END LOADING BLOCK ---

            else: 
                target_words =  [i.strip() for i in target_word.strip().split(',')]
                # --- START COMPARISON LOADING BLOCK WITH CAROUSEL ---
                with st.spinner('Running linguistic search...'):
                    # Display carousel for comparison load as well
                    carousel_placeholder = image_carousel_during_load()

                    df = pd.DataFrame()
                    for word in target_words:
                        df = pd.concat([df,get_synonyms_and_translations(word,num_synonyms,None,None,input_language,filter_langs,st.session_state['is_phrase'])],ignore_index=True)
                    st.session_state['final_data'] = df
                    
                carousel_placeholder.empty()
                # --- END COMPARISON LOADING BLOCK ---

            st.session_state['search_run'] = True      
        except ValueError as e:
            st.session_state['search_run'] = False
            st.error(f"Validation Error: {e}")

    if st.session_state['search_run']:
        if st.session_state['is_comparison']==False:
            st.subheader("Historical Date Filter")
            year_range = st.slider(
                "Select Target Year",
                min_value=MIN_YEAR,
                max_value=MAX_YEAR,
                value=2000, 
                step=1,
                help="Select a single specific year for the corpus analysis."
            )
            # world_map = empty_map.copy(deep=True)
            # create_frequency_map(world_map, st.session_state['final_data'], year_range)

            world_map = empty_map.copy(deep=True)
            _,col1,_ = st.columns([0.3,0.6,0.1])
            with col1: 
                st.subheader(f"World Map Ngram Frequency - Year {year_range}",help = """
                            Explore how your search term varies across countries and languages 
            
        1. What you're seeing:
        This map shows how frequently your search term (and its translations and synonyms) appear in books from different countries, based on each country's primary language.
        
        2. Color Intensity:
        - Darker colors = Your word appears LESS frequently in that language
        - Lighter colors = Your word appears MORE frequently
        - Grey countries = Language not currently supported in our analysis
        
        3. How to interact:
        - Hover over any country** to see:
        - The country name and primary language
        - All translated words/synonyms for that language
        - Exact frequency values
        - Use the year slider above to see how word usage changes over time
        
        Pro tip: Countries with the same primary language will have the same 
        color. For example, all Spanish-speaking countries share the same frequency 
        data for Spanish translations of your word.
        
        What is Relative Frequency?
        This is the number of times your word appears per million words in books 
        from that language during the selected year.
        """ )
            fig = create_frequency_map_plotly(world_map, st.session_state['final_data'], year_range)
            if fig:
                st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False})

            col_chart_left, col_chart_right = st.columns([1, 1])

            # --- START BAR CHART INTEGRATION ---
            # 1. Capture all three return values from create_word_cloud
            word_cloud_image_buffer, wc_df, fig_bar = create_word_cloud(st.session_state['final_data'], year_range=year_range)
            # --- END BAR CHART INTEGRATION ---

            with col_chart_left:
                st.subheader(f"Top Words by Language - Year {year_range}", help = """
                            Compare which translation or synonym is most popular in each language
        What you're seeing:
        This chart ranks the most frequently used words across all languages for the selected year. Each bar represents one word in one language.
        
        The bars show:
        - Height = How frequently the word appears (higher = more common)
        - Color = Which language the word belongs to
        - Label = The actual word and its language
        
        Why this matters:
        - See which languages use your concept most frequently
        - Discover if synonyms are more popular than direct translations
        - Compare cultural differences in word usage
        
        How to use it:
        - Hover over bars to see exact frequency values
        - Look for patterns: Do certain languages favor this word?
        - Compare with the map to see regional patterns
                            """ )
                # 2. Display the Plotly Bar Chart
                if fig_bar:
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.text("Bar Graph here") # This will now be replaced by the chart if data exists

            with col_chart_right:
                st.subheader(f"Word Cloud: Top Terms by Frequency - Year {year_range}", help = """
                            Visual snapshot of the most popular words and their languages
        What you're seeing:
        A visual representation of words, where size and color tell you about each word's importance and language.
        
        Size matters:
        - Bigger words = Used MORE frequently in books
        - Smaller words = Used less frequently
        - Only shows words that appeared at least once in the selected year
        
        Colors represent languages:
        - 🟡 Yellow = English
        - 🔴 Red = Spanish
        - 🔵 Blue = French
        - 🟣 Purple = German
        - 🟠 Orange = Italian
        - 🔷 Cyan = Russian
        - 🟢 Green = Chinese
        
        What you can learn:
        - Which words dominate? The biggest words are cultural favorites
        - Language diversity: Many colors = your concept translates well
        - Synonym popularity: If you included synonyms, see which alternatives are most common
        
        Why words appear multiple times:
        If you included synonyms, you might see related words (like "happy," 
        joyful," "cheerful") all displayed together.

                            """ )
                if word_cloud_image_buffer:
                    st.image(word_cloud_image_buffer, use_container_width=True)
        
        _,col2,_ = st.columns([0.3,0.6,0.1])
        with col2: 
            st.subheader(f"Word Frequency Over Time (smoothed)",help = """
                         Track how word usage has evolved across centuries and languages
        
    What you're seeing:
    This graph shows how frequently your search term appears in books 
    over 422 years (1600-2022), with a separate line for each language 
    and word variation.
    
    The lines represent:
    - Solid lines = Your original search term in each language
    - Dotted lines = Synonym variations (if you included them)
    - Line color = Language (matches the legend and word cloud colors)
    - Height (Y-axis) = Frequency (higher = more common)
    
    The data is smoothed:
    We use a 5-year moving average to reduce noise and show clearer 
    trends. This makes it easier to spot real patterns versus random spikes.
    
    Interactive features:
    - Hover over lines** to see exact year and frequency
    - Click legend items** to show/hide specific words
    - Use the language filter dropdown to focus on one language
    - Drag the range slider at the bottom to zoom into specific time periods
    - Click and drag on the chart to pan left and right
    
    Pro tips:
    - Compare synonyms to see if one term dominated over time
    - Look for when different languages "discovered" the same concept
    - Use the range slider to focus on specific historical periods
    - Notice how books published in different eras preferred different terms
    """ )
        time_chart = create_timeseries(st.session_state['final_data'])
        st.plotly_chart(time_chart, use_container_width=True)