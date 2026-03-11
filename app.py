import streamlit as st
import matplotlib.pyplot as plt
import re

# -------------------------------
# Page Setup
# -------------------------------

st.set_page_config(
    page_title="Ask Jesse – HVAC Fabricator Tool",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# Demo Users
# -------------------------------

USERS = {
    "jesse": "hvac123",
    "admin": "admin123",
    "apprentice": "learn123"
}

# -------------------------------
# Session State
# -------------------------------

defaults = {
    "logged_in": False,
    "username": "",
    "page": "Home",
    "step_index": 0,
    "selected_fabrication": "End Cap",
    "ai_prompt": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------------------
# Styling (Mobile Friendly)
# -------------------------------

st.markdown("""
<style>

.main {
    background-color:#f5f7fb;
}

button {
    height:60px;
    font-size:18px;
}

.block-container {
    padding-top:1rem;
}

.app-header {
    background: linear-gradient(135deg,#8b0000,#c1121f);
    padding:16px;
    border-radius:12px;
    color:white;
    text-align:center;
}

.panel {
    background:white;
    padding:14px;
    border-radius:12px;
    margin-bottom:12px;
    border:1px solid #e6e6e6;
}

.big-number {
    font-size:24px;
    font-weight:700;
}

.step-chip{
    background:#ffe4e4;
    padding:6px 12px;
    border-radius:20px;
    font-weight:600;
    color:#9b0000;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Helper Functions
# -------------------------------

def login(username, password):
    return USERS.get(username) == password


def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.page = "Home"
    st.session_state.step_index = 0


def next_step():
    if st.session_state.step_index < 5:
        st.session_state.step_index += 1


def prev_step():
    if st.session_state.step_index > 0:
        st.session_state.step_index -= 1


def reset_build():
    st.session_state.step_index = 0


def open_fabrication(name):
    st.session_state.selected_fabrication = name
    st.session_state.page = "Tool"
    st.session_state.step_index = 0


# -------------------------------
# AI Prompt Parser
# -------------------------------

def parse_ai_prompt(prompt):

    text = prompt.lower()

    result = {
        "fabrication": "End Cap",
        "width": 20,
        "height": 12
    }

    if "tap" in text:
        result["fabrication"] = "Tap-In"

    if "collar" in text:
        result["fabrication"] = "Starting Collar"

    if "offset" in text:
        result["fabrication"] = "Offset"

    nums = re.findall(r'\d+', text)

    if len(nums) >= 2:
        result["width"] = float(nums[0])
        result["height"] = float(nums[1])

    return result


# -------------------------------
# Login Screen
# -------------------------------

if not st.session_state.logged_in:

    st.markdown("""
    <div class="app-header">
    <h2>Ask Jesse – HVAC Fabricator Tool</h2>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):

        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()

        else:
            st.error("Invalid login")

    st.stop()


# -------------------------------
# Top Header
# -------------------------------

st.markdown("""
<div class="app-header">
<h2>Ask Jesse HVAC Fabrication Tool</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.write(f"Logged in: **{st.session_state.username}**")

with col2:
    if st.button("Logout"):
        logout()
        st.rerun()


# -------------------------------
# Home Page
# -------------------------------

if st.session_state.page == "Home":

    st.subheader("Fabrication Library")

    if st.button("End Cap", use_container_width=True):
        open_fabrication("End Cap")
        st.rerun()

    if st.button("Starting Collar", use_container_width=True):
        open_fabrication("Starting Collar")
        st.rerun()

    if st.button("Tap-In", use_container_width=True):
        open_fabrication("Tap-In")
        st.rerun()

    st.markdown("---")

    st.subheader("Ask Jesse AI")

    ai_prompt = st.text_area(
        "Describe your fabrication",
        placeholder="Example: build a 16x10 end cap"
    )

    if st.button("Analyze Request", use_container_width=True):

        parsed = parse_ai_prompt(ai_prompt)

        st.session_state.selected_fabrication = parsed["fabrication"]
        st.session_state.page = "Tool"

        st.success(
            f"Detected {parsed['fabrication']} {parsed['width']} x {parsed['height']}"
        )

        st.rerun()


# -------------------------------
# End Cap Tool
# -------------------------------

if st.session_state.page == "Tool":

    st.subheader(st.session_state.selected_fabrication)

    width = st.number_input("Width (inches)", value=20.0)
    height = st.number_input("Height (inches)", value=12.0)

    flange = 1
    scribe = 1
    cross_break_threshold = 14

    blank_length = width + (2 * flange)
    blank_width = height + (2 * flange)

    cross_break = width > cross_break_threshold or height > cross_break_threshold

    st.markdown("""
    <div class="panel">
    <b>Blank Size</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<div class='big-number'>{blank_length} x {blank_width}</div>",
        unsafe_allow_html=True
    )

    if cross_break:
        st.info("Cross Break Required")

    steps = [
        "Cut Blank",
        "Scribe Lines",
        "Cut Corner Notches",
        "Cross Break",
        "Bend Flanges",
        "Install"
    ]

    instructions = [
        f"Cut sheet metal blank {blank_length} x {blank_width}",
        "Scribe 1 inch on all sides",
        "Cut 45° corner notches",
        "Add cross break if larger than 14 inches",
        "Bend all flanges to 90 degrees",
        "Install end cap"
    ]

    step = st.session_state.step_index

    st.markdown(
        f"<div class='step-chip'>Step {step+1} of {len(steps)}</div>",
        unsafe_allow_html=True
    )

    st.subheader(steps[step])

    st.info(instructions[step])

    # -------------------------------
    # Drawing
    # -------------------------------

    fig, ax = plt.subplots()

    ax.plot(
        [0, blank_length, blank_length, 0, 0],
        [0, 0, blank_width, blank_width, 0]
    )

    if step >= 1:
        ax.plot([1, blank_length-1],[1,1],'r--')
        ax.plot([1, blank_length-1],[blank_width-1,blank_width-1],'r--')
        ax.plot([1,1],[1,blank_width-1],'r--')
        ax.plot([blank_length-1,blank_length-1],[1,blank_width-1],'r--')

    if step >= 3 and cross_break:
        ax.plot([0,blank_length],[0,blank_width],'g--')
        ax.plot([0,blank_length],[blank_width,0],'g--')

    ax.set_aspect('equal')
    ax.axis("off")

    st.pyplot(fig)

    # -------------------------------
    # Navigation
    # -------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("⬅ Back", on_click=prev_step, use_container_width=True)

    with col2:
        st.button("Reset", on_click=reset_build, use_container_width=True)

    with col3:
        st.button("Next ➡", on_click=next_step, use_container_width=True)

    st.progress((step+1)/len(steps))
