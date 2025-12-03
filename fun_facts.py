import streamlit as st
from st_ant_carousel import st_ant_carousel
from utils import *

# --- DATA ---
images_raw = {
    "fun_facts_Images/1_ts_phones_static.png": "This graph compares how often the phrases 'Blackberry phone' and 'Apple iPhone' appeared in English books over time.<br><br>Around 2005, both terms emerged together, but Blackberry quickly took the lead, riding high during its golden era. However, by 2010, the iPhone began its steady climb, eventually overtaking Blackberry as smartphones transformed our lives.<br><br>Today, iPhone dominates the conversation, while Blackberry's mentions have dwindled—almost like a tech time capsule! This chart perfectly captures the rise and fall of two iconic devices and how our words reflect shifting technology trends.",
    
    "fun_facts_Images/2_bars_religions_static.png":"This chart compares how often major world religions—Christianity, Islam, Judaism, Hinduism, and Buddhism—appeared in English books in 1800, 1900, and 2000.<br><br>In 1800, Christianity dominated the conversation, while Buddhism barely registered. By 1900, mentions of Buddhism, Islam, and Judaism surged, reflecting growing global awareness and cultural exchange.<br><br>Fast forward to 2000, and Islam nearly matches Christianity, while all other religions maintain strong visibility. It's fascinating how literature mirrors our expanding worldview—our books tell the story of shifting spiritual landscapes across centuries!",
    
    "fun_facts_Images/3_ts_politics_static.png":"This graph shows how often words like communism, socialism, capitalism, nazism, and fascism appeared in English books over time.<br><br>Notice how socialism and communism surged in popularity during the early 20th century, peaking around the Cold War era. Capitalism steadily climbed and now dominates the conversation, reflecting modern economic focus.<br><br>Meanwhile, nazism and fascism spiked sharply during World War II but declined afterward, though they never disappeared completely. It's fascinating how historical events leave fingerprints in language—our books literally tell the story of ideological battles across centuries!",
    
    "fun_facts_Images/4_heatmap_politics_static.png": "This chart shows the Pearson correlation between mentions of major political ideologies—communism, socialism, capitalism, nazism, and fascism—in English books from 1830 to 2022.<br><br>The strongest link is between communism and socialism (0.81), which makes sense given their shared roots. Capitalism correlates highly with fascism (0.79), reflecting how discussions of opposing systems often appear together.<br><br>Interestingly, nazism and fascism are strongly connected (0.71), while capitalism and nazism show the weakest tie (0.34). This heatmap reveals how ideological debates cluster in literature—our books don't just tell stories, they map the battles of ideas!",
    
    "fun_facts_Images/5_ts_mohammed_static5.png":"This graph compares how often different spellings of the name Mohammad/ Mohammed/ Muhammad/ Muhammed/ Muhamed appeared in English books from 1850 to 2025.<br><br>The most common spelling overall is Muhammad, which has consistently led the pack, especially after the mid-20th century. Variants like Mohammed and Mohamed also maintain strong visibility, while others such as Muhammed and Muhamed remain less frequent.<br><br>It's fascinating how a single name can have so many variations—and how cultural, linguistic, and historical influences shape their usage over time. Our books tell the story of global diversity, one spelling at a time!",
    
    "fun_facts_Images/6_ts_sports_static.png":"This graph tracks how often the words football, tennis, and rugby appeared in English books over time.<br><br>In the early 1800s, rugby dominated the conversation, but by the late 19th century, football started its meteoric rise, eventually becoming the most mentioned sport in literature. Tennis held steady for decades, peaking around the mid-20th century when it became a global pastime.<br><br>Interestingly, rugby's popularity in books declined after 1900, while football surged ahead and stayed on top. It's amazing how the evolution of sports culture is reflected in the words we write—our books tell the story of changing passions!",
    
    "fun_facts_Images/7_bars_academic_terms_static.png":"This chart compares how often academic terms appeared in English books across three key years: 1900, 1950, and 2000.<br><br>In 1900, psychology led the pack, while psychoanalysis barely registered. By 1950, psychology skyrocketed, and psychiatry and psychoanalysis gained traction—reflecting the mid-century fascination with the mind.<br><br>Fast forward to 2000, and psychology still dominates, but neuroscience makes a big leap, signaling the rise of brain-based research. It's fascinating to see how intellectual trends shift over time—our books reveal the journey from Freud's couch to cutting-edge brain scans!",
    
    "fun_facts_Images/8_ts_diets_static.png":"This graph tracks the popularity of dietary terms like vegan, vegetarian, and carnivore in English books from 1960 to the present.<br><br>Vegetarianism has long held the lead, steadily climbing as plant-based diets moved into the mainstream. However, the real story is the explosive rise of the word 'vegan'—barely mentioned in the 1960s, it skyrocketed after the year 2000 and is now nearly catching up to vegetarianism!<br><br>Meanwhile, 'carnivore' has seen a modest increase but remains much less common in literature. It's fascinating how our changing relationship with food is reflected in print—our books really do tell the story of a shifting global palate!",
    
    "fun_facts_Images/9_bars_cancers_static.png":"This chart shows how mentions of different cancer types in English books evolved over time—1870, 1955, and 2000.<br><br>In 1870, breast cancer led the conversation, while brain cancer was barely on the radar. By 1955, lung cancer surged to the top, reflecting growing awareness of smoking-related risks, while breast cancer remained significant.<br><br>Fast forward to 2000, and breast cancer dominates again, followed by lung cancer and colon cancer, as medical research and public health campaigns shaped the narrative. It's fascinating how literature mirrors our shifting battles against disease—our books tell the story of science and survival!"
}

images = []
for img in list(images_raw.keys()):
    if img.startswith('http://') or img.startswith('https://'):
        images.append(img)  # Keep URLs as-is
    else:
        images.append(get_image_as_base64(img)) 

captions = [f"Fun Fact {i+1}" for i in range(len(images))]

# The fun facts list must be synchronized with the image list
fun_facts = list(images_raw.values())
# --- END DATA ---



def show_fun_facts():
    st.title("Fun Facts Gallery")
    
    
    # Define dark colors based on your request
    PLOTLY_DARK = "#1f2127"
    GREYISH_NAVIGATOR = "#343a40"

    # 1. Prepare the content list required by st-ant-carousel
    carousel_content = []

    # Iterate through all three lists (images, captions, fun_facts)
    for i, (url, caption, fact) in enumerate(zip(images, captions, fun_facts)):
        
        # We use HTML/CSS Flexbox (display: flex) to place the image and text side-by-side
        html_code = f"""
            <div style="
                display: flex; 
                align-items: flex-start; 
                justify-content: space-between; 
                height: 100%; 
                padding: 30px;
                background-color: {PLOTLY_DARK}; 
                gap: 30px;
            ">
                
                <div style="flex: 0 0 65%; max-width: 65%; display: flex; flex-direction: column; justify-content: center;">
                    <img src="{url}" style="
                        width: 100%;
                        height: auto;
                        max-height: 600px;
                        border-radius: 10px; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.4);
                        object-fit: contain;
                    ">
                </div>

                <div style="
                    flex: 0 0 32%; 
                    max-width: 32%; 
                    display: flex; 
                    flex-direction: column;
                    justify-content: center;
                    padding: 20px;
                    background-color: rgba(255, 255, 255, 0.05);
                    border-radius: 10px;
                    border-left: 4px solid #4da6ff;
                ">
                    <h2 style="
                        color: #4da6ff; 
                        margin-bottom: 20px;
                        font-size: 28px;
                        font-weight: 600;
                        letter-spacing: 0.5px;
                    ">Fun Fact #{i + 1}</h2>
                    <p style="
                        color: #e0e0e0; 
                        font-size: 16px; 
                        line-height: 1.7;
                        text-align: justify;
                        margin: 0;
                    ">
                        {fact}
                    </p>
                </div>
            </div>
        """
        
        carousel_content.append({
            "content": html_code,
            "style": {"background": PLOTLY_DARK} 
        })

    # 2. Define global carousel styling (container background and navigator)
    carousel_style = {
        "backgroundColor": PLOTLY_DARK,
        "borderRadius": "15px",
        "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.4)",
        "padding": "10px",
        # Set the navigator (dots) background color to greyish
        "dotBackgroundColor": GREYISH_NAVIGATOR 
    }

    # 3. Render the carousel
    st_ant_carousel(
        content=carousel_content, 
        carousel_style=carousel_style,
        height=700,         
        autoplay=True,
        autoplaySpeed=8000,  # Increased to 8 seconds for more reading time
        animationSpeed=1000,
        dotPosition="bottom"
    )

if __name__ == "__main__":
    show_fun_facts()