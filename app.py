import streamlit as st
import matplotlib.pyplot as plt

# -------------------------------
# Page Setup
# -------------------------------
st.set_page_config(
    page_title="Ask Jesse – HVAC Fabricator Tool",
    layout="wide",
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
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "step_index" not in st.session_state:
    st.session_state.step_index = 0
if "selected_fabrication" not in st.session_state:
    st.session_state.selected_fabrication = "End Cap"
if "ai_prompt" not in st.session_state:
    st.session_state.ai_prompt = ""

# -------------------------------
# Helpers
# -------------------------------
def login(username: str, password: str) -> bool:
    return USERS.get(username) == password

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.page = "Home"
    st.session_state.step_index = 0
    st.session_state.selected_fabrication = "End Cap"
    st.session_state.ai_prompt = ""

def next_step():
    if st.session_state.step_index < 5:
        st.session_state.step_index += 1

def prev_step():
    if st.session_state.step_index > 0:
        st.session_state.step_index -= 1

def open_fabrication(name: str):
    st.session_state.selected_fabrication = name
    st.session_state.page = "End Cap Tool"
    st.session_state.step_index = 0

def parse_ai_prompt(prompt: str):
    """Very simple parser for demo use."""
    text = prompt.lower().strip()
    result = {
        "fabrication": "End Cap",
        "width": 20.0,
        "height": 12.0,
        "message": ""
    }

    if "tap" in text:
        result["fabrication"] = "Tap-In"
    elif "collar" in text:
        result["fabrication"] = "Starting Collar"
    elif "offset" in text or "dogleg" in text:
        result["fabrication"] = "Offset / Dogleg"
    elif "transition" in text:
        result["fabrication"] = "Transition"
    elif "elbow" in text:
        result["fabrication"] = "Elbow"

    nums = []
    cleaned = text.replace('x', ' x ').replace('"', ' ')
    for token in cleaned.split():
        try:
            nums.append(float(token))
        except ValueError:
            pass

    if len(nums) >= 2:
        result["width"] = nums[0]
        result["height"] = nums[1]
        result["message"] = f"Detected {result['fabrication']} with approximate size {nums[0]:.0f} x {nums[1]:.0f}."
    else:
        result["message"] = f"Detected {result['fabrication']}. Using default size 20 x 12."

    return result

# -------------------------------
# Styling
# -------------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 0.8rem;
        padding-bottom: 1.2rem;
        max-width: 1450px;
    }
    .main {
        background-color: #f6f8fb;
    }
    .app-header {
        background: linear-gradient(135deg, #8b0000, #c1121f);
        color: white;
        padding: 16px 20px;
        border-radius: 14px;
        margin-bottom: 12px;
    }
    .panel {
        background: grey;
        padding: 14px 16px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }
    .small-label {
        font-size: 0.85rem;
        color: #6b7280;
        margin-bottom: 4px;
    }
    .big-value {
        font-size: 1.15rem;
        font-weight: 700;
        color: #111827;
    }
    .step-chip {
        display: inline-block;
        background: #fee2e2;
        color: #b91c1c;
        padding: 5px 10px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .login-wrap {
        max-width: 460px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Login Screen
# -------------------------------
if not st.session_state.logged_in:
    st.markdown("""
    <div class="app-header">
        <h1 style="margin:0; color:white;">Ask Jesse – HVAC Fabricator Tool</h1>
        <p style="margin:6px 0 0 0;">Step-by-step fabrication guidance for shop teams and apprentices.</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        st.image("stafford_logo.png", width=220)
    except Exception:
        pass

    st.subheader("Login")

    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.markdown("**Demo logins**")
    st.code("")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# -------------------------------
# Top Nav
# -------------------------------
nav_left, nav_mid, nav_right = st.columns([2.3, 1.5, 1])

with nav_left:
    logo_col, title_col = st.columns([1, 4])
    with logo_col:
        try:
            st.image("stafford_logo.png", width=110)
        except Exception:
            st.empty()
    with title_col:
        st.markdown("""
        <div class="app-header">
            <h2 style="margin:0; color:white;">Ask Jesse – HVAC Fabricator Tool</h2>
            <p style="margin:6px 0 0 0;">Stafford Mechanical Services</p>
        </div>
        """, unsafe_allow_html=True)

with nav_mid:
    st.markdown(f"""
    <div class="panel">
        <div class="small-label">Logged in as</div>
        <div class="big-value">{st.session_state.username.title()}</div>
    </div>
    """, unsafe_allow_html=True)

with nav_right:
    page = st.selectbox(
        "Page",
        ["Home", "End Cap Tool"],
        index=0 if st.session_state.page == "Home" else 1
    )
    st.session_state.page = page
    if st.button("Logout", use_container_width=True):
        logout()
        st.rerun()

# -------------------------------
# Home Page
# -------------------------------
if st.session_state.page == "Home":
    home1, home2 = st.columns([1.2, 1])

    with home1:
        st.markdown("""
        <div class="panel">
            <h3 style="margin-top:0;">Welcome</h3>
            <p>This tool helps HVAC shops standardize fabrication steps, train apprentices faster, and reduce layout guesswork.</p>
            <p><strong>Current Tool:</strong> End Cap Fabrication</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="panel">
            <h3 style="margin-top:0;">Fabrication Library</h3>
            <p>Select a fabrication to open the tool workspace.</p>
        </div>
        """, unsafe_allow_html=True)

        lib1, lib2 = st.columns(2)
        with lib1:
            if st.button("End Cap", use_container_width=True):
                open_fabrication("End Cap")
                st.rerun()
            if st.button("Starting Collar", use_container_width=True):
                open_fabrication("Starting Collar")
                st.rerun()
            if st.button("Transition", use_container_width=True):
                open_fabrication("Transition")
                st.rerun()
        with lib2:
            if st.button("Tap-In", use_container_width=True):
                open_fabrication("Tap-In")
                st.rerun()
            if st.button("Offset / Dogleg", use_container_width=True):
                open_fabrication("Offset / Dogleg")
                st.rerun()
            if st.button("Elbow", use_container_width=True):
                open_fabrication("Elbow")
                st.rerun()

    with home2:
        st.markdown("""
        <div class="panel">
            <h3 style="margin-top:0;">Ask Jesse AI</h3>
            <p>Type what you want to build and let the tool suggest a fabrication and size.</p>
        </div>
        """, unsafe_allow_html=True)

        ai_prompt = st.text_area(
            "Describe what you need",
            value=st.session_state.ai_prompt,
            placeholder='Example: How do I build a 16 x 10 end cap?'
        )
        st.session_state.ai_prompt = ai_prompt

        if st.button("Analyze Request", use_container_width=True):
            parsed = parse_ai_prompt(ai_prompt)
            st.session_state.selected_fabrication = parsed["fabrication"]
            st.session_state.page = "End Cap Tool"
            st.session_state.step_index = 0
            st.success(parsed["message"])
            st.rerun()

        st.markdown("""
        <div class="panel">
            <h3 style="margin-top:0;">Planned Tools</h3>
            <p>• Plasma-ready exports</p>
            <p>• PDF shop prints</p>
            <p>• More fabrication calculators</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------
# End Cap Tool
# -------------------------------
elif st.session_state.page == "End Cap Tool":
    flange = 1.0
    scribe = 1.0
    cross_break_threshold = 14.0

    left, center, right = st.columns([1.0, 2.15, 1.1], gap="medium")

    # -------------------------------
    # Left Panel
    # -------------------------------
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top:0;">Inputs</h3>', unsafe_allow_html=True)
        st.write(f"**Selected Fabrication:** {st.session_state.selected_fabrication}")

        width = st.number_input("Width (inches)", min_value=1.0, max_value=120.0, value=20.0, step=1.0)
        height = st.number_input("Height (inches)", min_value=1.0, max_value=120.0, value=12.0, step=1.0)
        gauge = st.selectbox("Metal Gauge", ["26 ga", "24 ga", "22 ga", "20 ga"], index=0)

        st.markdown('</div>', unsafe_allow_html=True)

        blank_length = width + 2 * flange
        blank_width = height + 2 * flange
        cross_break_needed = width > cross_break_threshold or height > cross_break_threshold

        st.markdown(f"""
        <div class="panel">
            <h3 style="margin-top:0;">Quick Summary</h3>
            <div class="small-label">Finished Size</div>
            <div class="big-value">{width:.2f}" × {height:.2f}"</div>
            <br>
            <div class="small-label">Blank Size</div>
            <div class="big-value">{blank_length:.2f}" × {blank_width:.2f}"</div>
            <br>
            <div><strong>Gauge:</strong> {gauge}</div>
            <div><strong>Cross Break:</strong> {"Yes" if cross_break_needed else "No"}</div>
            <div><strong>Flange:</strong> {flange:.1f}" all around</div>
            <div><strong>Scribe:</strong> {scribe:.1f}"</div>
        </div>
        """, unsafe_allow_html=True)

    steps = [
        'Cut Sheet Metal Blank (+1" Flanges)',
        'Scribe 1" on All Edges',
        'Cut Corner Notches (Triangle 45°)',
        'Add Cross Break if Needed (>14")',
        'Bend Flanges 90°',
        'Install End Cap'
    ]

    instructions = [
        f'Cut sheet metal blank to **{blank_length:.2f}" x {blank_width:.2f}"** (+1" flange all around).',
        'Scribe **1"** from all four edges.',
        'Cut triangle corner notches from the scribe corners outward at 45°.',
        'If width or height is over **14"**, add a cross break in an X pattern corner to corner.',
        'Bend all four flanges **90° on the scribe lines**.',
        'Install end cap securely to duct opening.'
    ]

    def draw_endcap(step: int) -> None:
        fig, ax = plt.subplots(figsize=(8.0, 4.8))

        ax.plot(
            [0, blank_length, blank_length, 0, 0],
            [0, 0, blank_width, blank_width, 0],
            color="black",
            linewidth=2.5
        )

        if step >= 1:
            ax.plot([scribe, blank_length - scribe], [scribe, scribe], "r:", linewidth=2.2)
            ax.plot([scribe, blank_length - scribe], [blank_width - scribe, blank_width - scribe], "r:", linewidth=2.2)
            ax.plot([scribe, scribe], [scribe, blank_width - scribe], "r:", linewidth=2.2)
            ax.plot([blank_length - scribe, blank_length - scribe], [scribe, blank_width - scribe], "r:", linewidth=2.2)

            ax.annotate(
                f'{scribe}" Scribe',
                xy=(blank_length / 2, scribe),
                xytext=(blank_length / 2, scribe - 2.0),
                arrowprops=dict(arrowstyle="->", color="red", lw=1.8),
                ha="center",
                color="red",
                fontsize=11
            )

        if step >= 2:
            notch_size = scribe
            offset = 0.5

            ax.plot([scribe, scribe - notch_size], [scribe, scribe + offset], color="orange", linewidth=3)
            ax.plot([scribe, scribe + offset], [scribe, scribe - notch_size], color="orange", linewidth=3)

            ax.plot(
                [blank_length - scribe, blank_length - scribe + notch_size],
                [scribe, scribe + offset],
                color="orange",
                linewidth=3
            )
            ax.plot(
                [blank_length - scribe, blank_length - scribe - offset],
                [scribe, scribe - notch_size],
                color="orange",
                linewidth=3
            )

            ax.plot(
                [scribe, scribe - notch_size],
                [blank_width - scribe, blank_width - scribe - offset],
                color="orange",
                linewidth=3
            )
            ax.plot(
                [scribe, scribe + offset],
                [blank_width - scribe, blank_width - scribe + notch_size],
                color="orange",
                linewidth=3
            )

            ax.plot(
                [blank_length - scribe, blank_length - scribe + notch_size],
                [blank_width - scribe, blank_width - scribe - offset],
                color="orange",
                linewidth=3
            )
            ax.plot(
                [blank_length - scribe, blank_length - scribe - offset],
                [blank_width - scribe, blank_width - scribe + notch_size],
                color="orange",
                linewidth=3
            )

        if step >= 3 and cross_break_needed:
            ax.plot([0, blank_length], [0, blank_width], linestyle="--", color="purple", linewidth=3)
            ax.plot([0, blank_length], [blank_width, 0], linestyle="--", color="purple", linewidth=3)

        if step >= 4:
            ax.plot([scribe, blank_length - scribe], [scribe, scribe], "b--", linewidth=3)
            ax.plot([scribe, blank_length - scribe], [blank_width - scribe, blank_width - scribe], "b--", linewidth=3)
            ax.plot([scribe, scribe], [scribe, blank_width - scribe], "b--", linewidth=3)
            ax.plot([blank_length - scribe, blank_length - scribe], [scribe, blank_width - scribe], "b--", linewidth=3)

            ax.annotate(
                "Flange Bend Line",
                xy=(blank_length - scribe, blank_width / 2),
                xytext=(blank_length - scribe + 2.4, blank_width / 2),
                arrowprops=dict(arrowstyle="->", color="blue", lw=1.8),
                va="center",
                color="blue",
                fontsize=11
            )

        ax.set_xlim(-1.5, blank_length + 4.0)
        ax.set_ylim(-1.5, blank_width + 1.8)
        ax.set_aspect("equal")
        ax.axis("off")
        st.pyplot(fig, use_container_width=True)

    with center:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="step-chip">Step {st.session_state.step_index + 1} of {len(steps)}</div>', unsafe_allow_html=True)
        st.markdown(f"### {steps[st.session_state.step_index]}")

        draw_endcap(st.session_state.step_index)

        btn1, btn2, btn3 = st.columns([1, 1, 1])
        with btn1:
            st.button("⬅ Previous", on_click=prev_step, use_container_width=True, key="compact_prev")
        with btn2:
            if st.button("Print Layout", use_container_width=True, key="layout_print"):
                st.info("Use your browser print command: Cmd + P")
        with btn3:
            st.button("Next ➡", on_click=next_step, use_container_width=True, key="compact_next")

        st.progress((st.session_state.step_index + 1) / len(steps))
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="panel">
            <h3 style="margin-top:0;">Legend</h3>
            <p><strong style="color:black;">Black Solid</strong> = Cut Edge</p>
            <p><strong style="color:red;">Red Dotted</strong> = 1" Scribe Line</p>
            <p><strong style="color:orange;">Orange</strong> = Corner Notches (45°)</p>
            <p><strong style="color:blue;">Blue Dashed</strong> = Flange Bend Line</p>
            <p><strong style="color:purple;">Purple Dashed</strong> = Cross Break X</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="panel">
            <h3 style="margin-top:0;">Current Step</h3>
        </div>
        """, unsafe_allow_html=True)
        st.info(instructions[st.session_state.step_index])

        with st.expander("Shop Notes"):
            st.write(f'- Standard flange allowance: **{flange:.1f}"**')
            st.write(f'- Standard scribe offset: **{scribe:.1f}"**')
            st.write(f'- Cross break shown when width or height is over **{cross_break_threshold:.0f}"**')
            st.write(f'- Selected fabrication: **{st.session_state.selected_fabrication}**')
            st.write('- Current build is focused on end caps only.')
