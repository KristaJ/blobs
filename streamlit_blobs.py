import streamlit as st
import base64
from assets import blob
import os

def render_svg(svg):
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    return html


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
if st.button("MAKE MY BLOB!"):
    b=blob.Blob(color=color,
                num_points = num_points,
                opacity = opacity)
    b.make_blob()
    b.complete()
    svg_string = b.get_svg_string()

    blob = render_svg(svg_string)
    st.write(blob, unsafe_allow_html=True)


