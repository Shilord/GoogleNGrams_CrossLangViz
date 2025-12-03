import streamlit as st
import time
import base64
import os

# --- DATA ---
images_raw = {
    "fun_facts_Images/1_ts_phones_static.png": "This graph compares how often the phrases 'Blackberry phone' and 'Apple iPhone' appeared in English books over time. Around 2005, both terms emerged together, but Blackberry quickly took the lead, riding high during its golden era. However, by 2010, the iPhone began its steady climb, eventually overtaking Blackberry as smartphones transformed our lives.",
    
    "fun_facts_Images/2_bars_religions_static.png": "This chart compares how often major world religions—Christianity, Islam, Judaism, Hinduism, and Buddhism—appeared in English books in 1800, 1900, and 2020. In 1800, Christianity dominated the conversation, while Buddhism barely registered. By 1900, mentions of Buddhism, Islam, and Judaism surged, reflecting growing global awareness.",
    
    "fun_facts_Images/3_ts_politics_static.png": "This graph shows how often words like communism, socialism, capitalism, nazism, and fascism appeared in English books over time. Notice how socialism and communism surged in popularity during the early 20th century, peaking around the Cold War era. Capitalism steadily climbed and now dominates the conversation.",
    
    "fun_facts_Images/4_heatmap_politics_static.png": "This chart shows the Pearson correlation between mentions of major political ideologies—communism, socialism, capitalism, nazism, and fascism—in English books from 1830 to 2022. The strongest link is between communism and socialism (0.81), which makes sense given their shared roots.",
    
    "fun_facts_Images/5_ts_mohammed_static5.png": "This graph compares how often different spellings of the name Mohammad/ Mohammed/ Muhammad/ Muhammed/ Muhamed appeared in English books from 1850 to 2025. The most common spelling overall is Muhammad, which has consistently led the pack, especially after the mid-20th century.",
    
    "fun_facts_Images/6_ts_sports_static.png": "This graph tracks how often the words football, tennis, and rugby appeared in English books over time. In the early 1800s, rugby dominated the conversation, but by the late 19th century, football started its meteoric rise, eventually becoming the most mentioned sport in literature.",
    
    "fun_facts_Images/7_bars_academic_terms_static.png": "This chart compares how often academic terms appeared in English books across three key years: 1900, 1950, and 2000. In 1900, psychology led the pack, while psychoanalysis barely registered. By 1950, psychology skyrocketed, and psychiatry and psychoanalysis gained traction.",
    
    "fun_facts_Images/8_ts_diets_static.png": "This graph tracks the popularity of dietary terms like vegan, vegetarian, and carnivore in English books from 1960 to the present. Vegetarianism has long held the lead, steadily climbing as plant-based diets moved into the mainstream. However, the real story is the explosive rise of the word 'vegan'.",
    
    "fun_facts_Images/9_bars_cancers_static.png": "This chart shows how mentions of different cancer types in English books evolved over time—1870, 1955, and 2000. In 1870, breast cancer led the conversation, while brain cancer was barely on the radar. By 1955, lung cancer surged to the top, reflecting growing awareness of smoking-related risks."
}

def get_image_as_base64_url(image_path):
    """Convert image to base64 data URL"""
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    ext = os.path.splitext(image_path)[1].lower()
    mime_type = "image/png" if ext == ".png" else "image/jpeg"
    return f"data:{mime_type};base64,{encoded}"

def preload_cards(images):
    cards = []
    for index, imag in enumerate(images):
        card_html = f"""
        <div class="card card-{index}">
            <img src="{imag['path']}" class='img-container'>
            <p style="font-size: 1.4em; margin-bottom: 8px; font-weight: 600; color: #4da6ff;">Fun Fact #{index + 1}</p>
            <hr style="border: 1px solid #4da6ff; margin-top: 0px; margin-bottom: 10px;">
            <div style="border-left: 2px solid #4da6ff; border-right: 2px solid #4da6ff; border-bottom: 2px solid #4da6ff; padding: 15px; background-color: rgba(255, 255, 255, 0.05); border-radius: 0 0 10px 10px;">
                <p style="color: #e0e0e0; line-height: 1.6; text-align: justify;">{imag['desc']}</p>
            </div>   
        </div>
        """
        cards.append(card_html)
    return cards

def show_fun_facts():
    _,col,_ = st.columns([0.4,0.5,0.1])
    with col:
        st.title("Fun Facts Gallery",anchor = False)
    
    # Load CSS
    st.markdown("""
    <style>
    @keyframes slideInFromRight {
        0% { transform: translateX(10%); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutToLeft {
        0% { transform: translateX(0); opacity: 1; }
        100% { transform: translateX(-100%); opacity: 0; }
    }
    
    @keyframes slideInFromLeft {
        0% { transform: translateX(-10%); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutToRight {
        0% { transform: translateX(0); opacity: 1; }
        100% { transform: translateX(100%); opacity: 0; }
    }
    
    @keyframes slideLeft {
        0% { transform: translateX(0); }
        100% { transform: translateX(-104.5%); }
    }
    
    @keyframes slideRight {
        0% { transform: translateX(0); }
        100% { transform: translateX(104.5%); }
    }
    
    .card-slide-in-from-right { animation: slideInFromRight 0.4s ease-in-out forwards; }
    .card-slide-out-to-left { animation: slideOutToLeft 0.5s ease-in-out forwards; }
    .card-slide-in-from-left { animation: slideInFromLeft 0.4s ease-in-out forwards; }
    .card-slide-out-to-right { animation: slideOutToRight 0.5s ease-in-out forwards; }
    .card-slide-left { animation: slideLeft 0.5s ease-in-out forwards; }
    .card-slide-right { animation: slideRight 0.5s ease-in-out forwards; }
    
    .card {
        background-color: #0d1118;
        border: 2px solid #2962FF;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 4px 10px rgba(77, 166, 255, 0.3);
        transition: all 0.3s ease-in-out;
        height: 650px;
        padding: 15px;
        overflow: hidden;
    }
    
    .card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(77, 166, 255, 0.5);
    }
    
    .img-container {
        width: 100%;
        height: 400px;
        object-fit: contain;
        border-radius: 8px;
        margin-bottom: 5px;
        background-color: #0d1118;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Prepare images data
    images = []
    for i, (img_path, fact_text) in enumerate(images_raw.items(), 1):
        img_url = get_image_as_base64_url(img_path)
        images.append({
            'path': img_url,
            'title': f'Fun Fact #{i}',
            'desc': fact_text
        })
    
    # Initialize session state
    if 'cards' not in st.session_state:
        st.session_state.cards = preload_cards(images)
    
    if 'start_index' not in st.session_state:
        st.session_state.start_index = 0
    
    if 'animation_class' not in st.session_state:
        st.session_state.animation_class = [""] * len(st.session_state.cards)
    
    if 'direction' not in st.session_state:
        st.session_state.direction = ''
    
    def update_animation_classes(direction):
        if direction == 'left':
            st.session_state.animation_class = ["card-slide-left"] * len(st.session_state.cards)
            st.session_state.animation_class[(st.session_state.start_index)] = 'card-slide-out-to-left'
            st.session_state.animation_class[(st.session_state.start_index + 3) % len(st.session_state.cards)] = 'card-slide-in-from-right'
        elif direction == 'right':
            st.session_state.animation_class = ["card-slide-right"] * len(st.session_state.cards)
            st.session_state.animation_class[(st.session_state.start_index + 3) % len(st.session_state.cards)] = 'card-slide-in-from-left'
            st.session_state.animation_class[(st.session_state.start_index+2)% len(st.session_state.cards)] = 'card-slide-out-to-right'
    
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        left = st.button('◀ Previous', use_container_width=True)
        if left:
            update_animation_classes('right')
            st.session_state.start_index = (st.session_state.start_index) % len(st.session_state.cards)
            st.session_state.direction = 'right'
    
    with col2:
        right = st.button('Next ▶', use_container_width=True)
        if right:
            update_animation_classes('left')
            st.session_state.direction = 'left'
    
    # Number of cards to display at once
    CARDS_TO_SHOW = 1
    
    # Handle animations
    if st.session_state.direction == 'left':
        cols = st.columns(CARDS_TO_SHOW)
        placeholders = [col.empty() for col in cols]
        
        for i in range(CARDS_TO_SHOW):
            card_index = (st.session_state.start_index + i) % len(st.session_state.cards)
            card_class = st.session_state.animation_class[card_index]
            placeholders[i].markdown(f'<div class="{card_class}">{st.session_state.cards[card_index]}</div>', unsafe_allow_html=True)
        time.sleep(0.5)
        
        st.session_state.start_index = (st.session_state.start_index + 1) % len(st.session_state.cards)
        
        for i in range(CARDS_TO_SHOW):
            card_index = (st.session_state.start_index + i) % len(st.session_state.cards)
            card_class = st.session_state.animation_class[card_index]
            if card_class == "card-slide-left":
                card_class = ""
            placeholders[i].markdown(f'<div class="{card_class}">{st.session_state.cards[card_index]}</div>', unsafe_allow_html=True)
        st.session_state.direction = ''
        st.session_state.animation_class = [""] * len(st.session_state.cards)
    
    elif st.session_state.direction == 'right':
        cols = st.columns(CARDS_TO_SHOW)
        placeholders = [col.empty() for col in cols]
        
        for i in range(CARDS_TO_SHOW):
            card_index = (st.session_state.start_index + i) % len(st.session_state.cards)
            card_class = st.session_state.animation_class[card_index]
            placeholders[i].markdown(f'<div class="{card_class}">{st.session_state.cards[card_index]}</div>', unsafe_allow_html=True)
        time.sleep(0.5)
        
        st.session_state.start_index = (st.session_state.start_index - 1) % len(st.session_state.cards)
        
        for i in range(CARDS_TO_SHOW):
            card_index = (st.session_state.start_index + i) % len(st.session_state.cards)
            card_class = st.session_state.animation_class[card_index]
            if card_class == "card-slide-right":
                card_class = ""
            placeholders[i].markdown(f'<div class="{card_class}">{st.session_state.cards[card_index]}</div>', unsafe_allow_html=True)
        st.session_state.direction = ''
        st.session_state.animation_class = [""] * len(st.session_state.cards)
    
    else:
        cols = st.columns(CARDS_TO_SHOW)
        for i in range(CARDS_TO_SHOW):
            card_index = (st.session_state.start_index + i) % len(st.session_state.cards)
            card_class = st.session_state.animation_class[card_index]
            with cols[i]:
                st.markdown(f'<div class="{card_class}">{st.session_state.cards[card_index]}</div>', unsafe_allow_html=True)
    
    # Show pagination indicator
    st.markdown(f"<center style='color: #4da6ff; margin-top: 20px; font-size: 1.2em;'>Card {st.session_state.start_index + 1} of {len(st.session_state.cards)}</center>", unsafe_allow_html=True)

if __name__ == "__main__":
    show_fun_facts()