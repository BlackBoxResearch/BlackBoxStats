from streamlit_extras.stylable_container import stylable_container
import streamlit as st

primary_background = '#111111'
secondary_background = '#171717'
dark_text_color = '#171717'
light_text_color = '#E8E8E8'
color_1 = '#5A85F3' #Blue
color_2 = '#CDFFD8' #Green
border_color = '#3c3c3c'
caption_color = '#878884'


def SystemsPage():
    with st.container(border=False):    
        st.subheader("Systems", anchor=False)

        with stylable_container(
            key="image_container", 
            css_styles=f"""
                background-image: linear-gradient(to right, #141e30, #243b55); 
                background-size: cover;
                background-position: center;
                border: 1px solid {border_color};
                border-radius: 0.5rem;
                padding: calc(1em - 1px);
                color: {light_text_color};
                display: flex;
                align-items: center;
                justify-content: space-between;
                """
            ):
            with st.container(border=False, height=100):
                st.markdown("### Save with cryptocurrency")
                st.markdown("**Permanently discounted prices**")

if __name__ == "__main__":
    SystemsPage()

        #                /* background-image: url('static/container_background.png'); /*