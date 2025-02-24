import streamlit as st
import base64
from assets import blob
import os

def render_svg(svg):
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    return html


def activate_download():
    print("ACTIVATE")
    st.session_state.download_disabled = False
    print(st.session_state.download_disabled)


if 'svg_string' not in st.session_state:
    st.session_state.svg_string = ''
if 'download_disabled' not in st.session_state:
    st.session_state.download_disabled = True

print(st.session_state.download_disabled)

st.title('Make my Blob')
random_color = st.sidebar.checkbox("random color?", value=True)
color=st.sidebar.color_picker("Choose the color for your blob", disabled=random_color)
random_num_points = st.sidebar.checkbox("random number of points?", value=True)
num_points = int(st.sidebar.slider('How many points should your blob have?', min_value=3,
                               max_value=12, step=1, disabled=random_num_points))
random_opacity = st.sidebar.checkbox("random opacity?", value=True)
opacity = st.sidebar.slider('How opague should your blob be?', min_value=0.0,
                            max_value=1.0, step=.01, disabled=random_opacity)




if random_color:
    color=None
if random_num_points:
    num_points = None
if random_opacity:
    opacity = None
if st.button("MAKE MY BLOB!", on_click=activate_download):
    print("CLICK")
    print(st.session_state.download_disabled)
    b=blob.Blob(color=color,
                num_points = num_points,
                opacity = opacity)
    b.make_blob()
    b.complete()
    svg_string = b.get_svg_string()
    st.session_state.svg_string = svg_string


if len(st.session_state.svg_string)>10:
    blob = render_svg(st.session_state.svg_string)
    st.write(blob, unsafe_allow_html=True)


dlb = st.sidebar.download_button(
                label="Download Blob",
                data=st.session_state.svg_string,
                file_name='blob.svg',
                disabled=st.session_state.download_disabled
            )