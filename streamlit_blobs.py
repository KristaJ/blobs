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
if random_color:
    color=None
if st.button("MAKE MY BLOB!"):
    b=blob.Blob(color=color)
    b.make_blob()
    b.complete()
    svg_string = b.get_svg_string()

    blob = render_svg(svg_string)
    st.write(blob, unsafe_allow_html=True)


