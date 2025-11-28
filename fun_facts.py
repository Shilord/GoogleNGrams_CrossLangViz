import streamlit as st

images = [
    "https://placebear.com/803/601",
    "https://placedog.net/800/600",
    "https://placebear.com/800/600",
    "https://placebear.com/801/601",
    "https://placedog.net/801/601",
    "https://placebear.com/801/601",
    "https://placebear.com/802/601",
]
captions = [f"Image {i+1}" for i in range(len(images))]

def show_fun_facts():
    if 'gallery_index' not in st.session_state:
        st.session_state.gallery_index = 0

    def update_index(new_index):
        st.session_state.gallery_index = new_index

    current_idx = st.session_state.gallery_index
    total_images = len(images)

    indices = [
        (current_idx - 2) % total_images, # Left 2
        (current_idx - 1) % total_images, # Left 1
        current_idx,                      # Center (Active)
        (current_idx + 1) % total_images, # Right 1
        (current_idx + 2) % total_images  # Right 2
    ]

    # --- UI LAYOUT ---

    st.title("Fun Facts Gallery")

    # A. Main "Spotlight" Image
    main_col, _ = st.columns([1, 0.01]) # Centered feel
    with main_col:
        st.image(
            images[current_idx], 
            caption=captions[current_idx], 
            use_container_width=True
        )
    cols = st.columns([1, 1, 1, 1, 1])

    for i, col in enumerate(cols):
        img_idx = indices[i]
        is_center = (i == 2) # The 3rd column is the center/active one
        
        with col:
            # Visual indicator for the active item
            if is_center:
                st.markdown(f"**Current**")
            else:
                st.write("&nbsp;") # Spacer
                
            # Display the thumbnail
            st.image(images[img_idx], use_container_width=True)

    # Optional: Add Previous/Next big buttons
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("⬅️ Previous Image", use_container_width=True):
            update_index((current_idx - 1) % total_images)
    with col_next:
        if st.button("Next Image ➡️", use_container_width=True):
            update_index((current_idx + 1) % total_images)