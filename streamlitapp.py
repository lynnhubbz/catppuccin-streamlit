"""
Streamlit Kitchen Sink
======================
One app that renders (almost) every Streamlit widget and a few popular add-ons,
so you can eyeball a theme (e.g. Catppuccin) for contrast / styling bugs.

Run:
    pip install -r requirements.txt
    streamlit run app.py

Notes:
- Newer widgets are guarded with hasattr(), so the app still runs on older versions.
- Add-ons are guarded with try/except ImportError and show an install hint if missing.
- Camera / microphone widgets are behind checkboxes so the browser doesn't prompt on load.
"""

import datetime as dt
import io
import time

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Streamlit Kitchen Sink",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

rng = np.random.default_rng(42)


def has(name: str) -> bool:
    """True if this Streamlit version has st.<name>."""
    return hasattr(st, name)


def missing(pkg: str):
    st.warning(f"`{pkg}` not installed → `pip install {pkg}`", icon="📦")


# ---------------------------------------------------------------- sample data
@st.cache_data
def sample_df(n: int = 200) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "x": rng.normal(size=n),
            "y": rng.normal(size=n),
            "group": rng.choice(["A", "B", "C"], size=n),
            "size": rng.uniform(5, 40, size=n),
        }
    )


@st.cache_data
def ts_df(n: int = 60) -> pd.DataFrame:
    idx = pd.date_range("2026-01-01", periods=n, freq="D")
    return pd.DataFrame(
        {
            "alpha": rng.normal(size=n).cumsum(),
            "beta": rng.normal(size=n).cumsum(),
            "gamma": rng.normal(size=n).cumsum(),
        },
        index=idx,
    )


@st.cache_data
def table_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": ["Mocha", "Latte", "Frappé", "Macchiato"],
            "score": [92, 78, 85, 64],
            "ratio": [0.92, 0.78, 0.85, 0.64],
            "trend": [rng.normal(size=12).cumsum().tolist() for _ in range(4)],
            "bars": [rng.integers(1, 10, size=8).tolist() for _ in range(4)],
            "active": [True, False, True, False],
            "link": ["https://streamlit.io"] * 4,
            "when": pd.date_range("2026-10-01", periods=4),
        }
    )


# ---------------------------------------------------------------- session state
st.session_state.setdefault("clicks", 0)

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.title("🧪 Kitchen Sink")
    st.caption(f"Streamlit {st.__version__}")
    st.divider()

    st.subheader("Sidebar widgets")
    st.text_input("Sidebar text", "hello", key="sb_text")
    st.selectbox("Sidebar select", ["one", "two", "three"], key="sb_sel")
    st.slider("Sidebar slider", 0, 100, 40, key="sb_slider")
    st.checkbox("Sidebar checkbox", True, key="sb_chk")
    if st.button("Sidebar button", key="sb_btn", width="stretch"):
        st.session_state.clicks += 1
    st.write(f"Clicks: **{st.session_state.clicks}**")
    st.divider()
    st.info("Theme tip: toggle ⋮ → Settings → Theme to flip light/dark.")

st.title("Streamlit Kitchen Sink")
st.caption("Every widget in one place — use it to check your theme.")

tabs = st.tabs(
    [
        "📝 Text",
        "🎛️ Inputs",
        "📊 Data",
        "📈 Charts",
        "🖼️ Media",
        "🚦 Status",
        "🧱 Layout",
        "💬 Chat",
        "🔌 Add-ons",
    ]
)

# ================================================================ TEXT
with tabs[0]:
    st.header("Header (h2)")
    st.subheader("Subheader (h3)")
    st.title("Title (h1)")
    st.markdown(
        """
**Bold**, *italic*, ~~strike~~, `inline code`, [a link](https://streamlit.io),
:red[red], :orange[orange], :green[green], :blue[blue], :violet[violet], :gray[gray],
:red-background[bg red] :blue-background[bg blue] :rainbow[rainbow] :material/favorite: icon.

> A blockquote — check the left border and text contrast.

- bullet one
  - nested bullet
- bullet two

1. numbered
2. list

- [x] task done
- [ ] task open

| Col A | Col B |
|-------|-------|
| 1     | 2     |
| 3     | 4     |
"""
    )
    st.caption("This is a caption — usually the lowest-contrast text.")
    st.text("Fixed-width text via st.text")
    st.code(
        "def hello(name: str) -> str:\n    return f'Hello, {name}!'  # comment\n\nprint(hello('Catppuccin'))",
        language="python",
        line_numbers=True,
    )
    st.latex(r"\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}")
    st.divider()
    st.write("`st.write` handles many types:", {"a": 1, "b": [1, 2, 3]})
    st.json({"nested": {"list": [1, 2, 3], "bool": True, "none": None, "str": "text"}})
    if has("badge"):
        st.badge("Badge", icon=":material/check:", color="green")
        st.badge("Warning", color="orange")
        st.badge("Error", color="red")
    st.html("<p style='margin:0'>Raw <b>HTML</b> via <code>st.html</code></p>") if has("html") else None

# ================================================================ INPUTS
with tabs[1]:
    st.header("Input widgets")

    st.subheader("Buttons")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Default"):
            st.toast("Default clicked")
    with c2:
        if st.button("Primary", type="primary"):
            st.toast("Primary clicked")
    with c3:
        st.button("Secondary", type="secondary", icon=":material/save:")
    with c4:
        st.button("Disabled", disabled=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("Download CSV", sample_df().to_csv(index=False), "sample.csv", "text/csv")
    with c2:
        st.link_button("Link button", "https://streamlit.io")
    with c3:
        st.button("Tertiary", type="tertiary")

    st.subheader("Toggles & choices")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.checkbox("Checkbox", value=True)
        st.checkbox("Checkbox (unchecked)")
        st.checkbox("Checkbox (disabled)", disabled=True)
        st.toggle("Toggle", value=True)
        st.toggle("Toggle (off)")
    with c2:
        st.radio("Radio", ["Latte", "Mocha", "Frappé", "Macchiato"])
        st.radio("Radio (horizontal)", ["A", "B", "C"], horizontal=True)
    with c3:
        st.selectbox("Selectbox", ["Latte", "Mocha", "Frappé", "Macchiato"])
        st.multiselect("Multiselect", ["Latte", "Mocha", "Frappé", "Macchiato"], default=["Mocha", "Latte"])
        st.selectbox("Selectbox (disabled)", ["x"], disabled=True)

    c1, c2 = st.columns(2)
    with c1:
        if has("pills"):
            st.pills("Pills", ["Red", "Green", "Blue"], selection_mode="multi", default=["Green"])
    with c2:
        if has("segmented_control"):
            st.segmented_control("Segmented control", ["Day", "Week", "Month"], default="Week")

    st.subheader("Sliders & numbers")
    c1, c2 = st.columns(2)
    with c1:
        st.slider("Slider", 0, 100, 35)
        st.slider("Range slider", 0.0, 1.0, (0.25, 0.75))
        st.select_slider("Select slider", options=["XS", "S", "M", "L", "XL"], value="M")
        st.slider("Date slider", dt.date(2026, 1, 1), dt.date(2026, 12, 31), dt.date(2026, 6, 15))
    with c2:
        st.number_input("Number input", 0, 100, 42)
        st.number_input("Float input", 0.0, 1.0, 0.5, step=0.05)
        if has("feedback"):
            st.write("Feedback (stars)")
            st.feedback("stars")
            st.write("Feedback (thumbs)")
            st.feedback("thumbs")

    st.subheader("Text input")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Text input", "Some text", help="This is a help tooltip")
        st.text_input("Password", type="password", value="hunter2")
        st.text_input("With placeholder", placeholder="Type here…")
        st.text_input("Disabled", "can't touch this", disabled=True)
    with c2:
        st.text_area("Text area", "Multi-line\ntext here", height=130)

    st.subheader("Date / time / colour")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.date_input("Date", dt.date(2026, 10, 12))
    with c2:
        st.time_input("Time", dt.time(19, 52))
    with c3:
        st.color_picker("Colour", "#cba6f7")
    with c4:
        if has("datetime_input"):
            st.datetime_input("Datetime", dt.datetime(2026, 10, 12, 19, 52))
    st.date_input("Date range", (dt.date(2026, 10, 1), dt.date(2026, 10, 12)))

    st.subheader("Uploads & capture")
    st.file_uploader("File uploader", accept_multiple_files=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.checkbox("Enable camera input (asks for permission)"):
            st.camera_input("Camera")
    with c2:
        if has("audio_input") and st.checkbox("Enable audio input (asks for permission)"):
            st.audio_input("Record audio")

    st.subheader("Forms")
    with st.form("demo_form"):
        st.text_input("Name", key="form_name")
        st.slider("Level", 0, 10, 5, key="form_level")
        submitted = st.form_submit_button("Submit form", type="primary")
    if submitted:
        st.success(f"Submitted: {st.session_state.form_name} @ {st.session_state.form_level}")

# ================================================================ DATA
with tabs[2]:
    st.header("Data display")

    st.subheader("st.dataframe")
    st.dataframe(sample_df().head(15), width="stretch")

    st.subheader("Styled dataframe (pandas Styler)")
    st.dataframe(
        sample_df().head(8).style.background_gradient(cmap="viridis").format(precision=2),
        width="stretch",
    )

    st.subheader("column_config")
    st.dataframe(
        table_df(),
        width="stretch",
        column_config={
            "name": st.column_config.TextColumn("Name", help="Text column"),
            "score": st.column_config.NumberColumn("Score", format="%d ⭐"),
            "ratio": st.column_config.ProgressColumn("Ratio", min_value=0, max_value=1),
            "trend": st.column_config.LineChartColumn("Trend"),
            "bars": st.column_config.BarChartColumn("Bars"),
            "active": st.column_config.CheckboxColumn("Active"),
            "link": st.column_config.LinkColumn("Link"),
            "when": st.column_config.DateColumn("When", format="YYYY-MM-DD"),
        },
        hide_index=True,
    )

    st.subheader("st.data_editor")
    edited = st.data_editor(
        pd.DataFrame(
            {"item": ["a", "b", "c"], "qty": [1, 2, 3], "ok": [True, False, True]}
        ),
        num_rows="dynamic",
        width="stretch",
        key="editor",
    )

    st.subheader("st.table (static)")
    st.table(sample_df().head(4).round(2))

    st.subheader("Metrics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temperature", "24 °C", "1.2 °C")
    c2.metric("Humidity", "61 %", "-3 %")
    c3.metric("Power", "118 W", "0 W", delta_color="off")
    c4.metric("Errors", "7", "+2", delta_color="inverse")
    try:
        c1, c2 = st.columns(2)
        c1.metric("With sparkline", "1,204", "+8%", chart_data=ts_df()["alpha"].tolist(), chart_type="line", border=True)
        c2.metric("With bars", "311", "-4%", chart_data=ts_df()["beta"].tolist(), chart_type="bar", border=True)
    except TypeError:
        st.caption("(metric sparklines need a newer Streamlit)")

# ================================================================ CHARTS
with tabs[3]:
    st.header("Charts")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("line_chart")
        st.line_chart(ts_df())
        st.subheader("bar_chart")
        st.bar_chart(ts_df().tail(10))
    with c2:
        st.subheader("area_chart")
        st.area_chart(ts_df())
        st.subheader("scatter_chart")
        st.scatter_chart(sample_df(), x="x", y="y", color="group", size="size")

    st.subheader("map")
    st.map(
        pd.DataFrame(
            {
                "lat": -6.2 + rng.normal(scale=0.05, size=100),
                "lon": 106.8 + rng.normal(scale=0.05, size=100),
            }
        )
    )

    st.subheader("Altair (Vega-Lite)")
    chart = (
        alt.Chart(sample_df())
        .mark_circle(opacity=0.7)
        .encode(x="x", y="y", color="group", size="size", tooltip=["x", "y", "group"])
        .interactive()
    )
    st.altair_chart(chart, width="stretch")

    st.subheader("Graphviz")
    st.graphviz_chart(
        """
        digraph {
            rankdir=LR;
            ESP32 -> MQTT -> Broker;
            Broker -> Grafana;
            Broker -> Streamlit;
            Sensor -> ESP32;
        }
        """
    )

    st.subheader("Vega-Lite (raw spec)")
    st.vega_lite_chart(
        sample_df(),
        {"mark": {"type": "point", "tooltip": True}, "encoding": {"x": {"field": "x", "type": "quantitative"}, "y": {"field": "y", "type": "quantitative"}, "color": {"field": "group", "type": "nominal"}}},
        width="stretch",
    )

    st.subheader("Optional: Matplotlib / Plotly")
    c1, c2 = st.columns(2)
    with c1:
        try:
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots()
            ax.plot(ts_df().index, ts_df()["alpha"], label="alpha")
            ax.plot(ts_df().index, ts_df()["beta"], label="beta")
            ax.legend()
            ax.set_title("Matplotlib")
            st.pyplot(fig)
            st.caption("Matplotlib ignores the Streamlit theme unless you style it yourself.")
        except ImportError:
            missing("matplotlib")
    with c2:
        try:
            import plotly.express as px

            st.plotly_chart(px.scatter(sample_df(), x="x", y="y", color="group", title="Plotly"), width="stretch")
        except ImportError:
            missing("plotly")

# ================================================================ MEDIA
with tabs[4]:
    st.header("Media")

    st.subheader("Image")
    img = np.zeros((120, 360, 3), dtype=np.uint8)
    img[..., 0] = np.linspace(0, 255, 360, dtype=np.uint8)[None, :]
    img[..., 1] = np.linspace(255, 0, 120, dtype=np.uint8)[:, None]
    img[..., 2] = 160
    st.image(img, caption="Generated gradient (st.image)")

    st.subheader("Audio (generated 440 Hz sine)")
    sr = 22050
    t = np.linspace(0, 1.5, int(sr * 1.5), endpoint=False)
    st.audio(np.sin(2 * np.pi * 440 * t).astype(np.float32) * 0.3, sample_rate=sr)

    st.subheader("Video (remote sample)")
    st.caption("Needs internet — remove if offline.")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

    if has("pdf"):
        st.caption("`st.pdf` exists in this version (needs `streamlit[pdf]` + a file).")

# ================================================================ STATUS
with tabs[5]:
    st.header("Status & feedback")

    st.success("Success message", icon="✅")
    st.info("Info message", icon="ℹ️")
    st.warning("Warning message", icon="⚠️")
    st.error("Error message", icon="🚨")
    st.exception(ValueError("Example exception (rendered, not raised)"))

    st.subheader("Progress")
    st.progress(65, text="Static progress 65%")
    if st.button("Run progress bar"):
        bar = st.progress(0, text="Working…")
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1, text=f"Working… {i + 1}%")
        bar.empty()
        st.success("Done")

    st.subheader("Spinner / status / toast / effects")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Spinner"):
            with st.spinner("Thinking…"):
                time.sleep(1.2)
            st.success("Spinner finished")
    with c2:
        if st.button("Toast"):
            st.toast("Hello from a toast!", icon="🎉")
    with c3:
        if st.button("Balloons"):
            st.balloons()
    with c4:
        if st.button("Snow"):
            st.snow()

    if st.button("Run status container"):
        with st.status("Running pipeline…", expanded=True) as status:
            st.write("Loading data")
            time.sleep(0.5)
            st.write("Training")
            time.sleep(0.5)
            st.write("Exporting")
            time.sleep(0.5)
            status.update(label="Pipeline complete", state="complete", expanded=False)

# ================================================================ LAYOUT
with tabs[6]:
    st.header("Layout & containers")

    st.subheader("Columns")
    a, b, c = st.columns([1, 2, 1])
    a.write("Narrow")
    b.write("Wide")
    c.write("Narrow")

    st.subheader("Container (bordered)")
    with st.container(border=True):
        st.write("Inside a bordered container")
        st.button("Button inside", key="in_container")

    st.subheader("Expander")
    with st.expander("Click to expand", expanded=False):
        st.write("Hidden content.")
        st.code("print('hi')")

    st.subheader("Popover")
    with st.popover("Open popover"):
        st.write("Popover content")
        st.checkbox("A checkbox in a popover")
        st.text_input("Input in popover", key="pop_in")

    st.subheader("Nested tabs")
    t1, t2 = st.tabs(["Inner A", "Inner B"])
    t1.write("Tab A content")
    t2.write("Tab B content")

    if has("dialog"):
        st.subheader("Dialog (modal)")

        @st.dialog("Example dialog")
        def show_dialog():
            st.write("Modal content — check the overlay and card colours.")
            st.text_input("Inside dialog", key="dlg_in")
            if st.button("Close", key="dlg_close"):
                st.rerun()

        if st.button("Open dialog"):
            show_dialog()

    st.subheader("Fragment (partial rerun)")

    @st.fragment
    def counter():
        st.session_state.setdefault("frag", 0)
        if st.button("Increment (fragment only)", key="frag_btn"):
            st.session_state.frag += 1
        st.write(f"Fragment count: **{st.session_state.frag}**")

    counter()

    st.subheader("Empty placeholder")
    ph = st.empty()
    if st.button("Fill placeholder"):
        ph.info(f"Filled at {dt.datetime.now():%H:%M:%S}")

# ================================================================ CHAT
with tabs[7]:
    st.header("Chat elements")

    with st.chat_message("user"):
        st.write("Hello 👋")
    with st.chat_message("assistant"):
        st.write("Hi! Here's a chart inside a chat message:")
        st.line_chart(ts_df()[["alpha"]].tail(20), height=150)
    with st.chat_message("assistant", avatar="🤖"):
        st.write("Custom avatar message")

    prompt = st.chat_input("Say something (chat_input)")
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            def gen():
                for w in f"You said: {prompt}. This is a streamed reply.".split():
                    yield w + " "
                    time.sleep(0.05)

            st.write_stream(gen)

# ================================================================ ADD-ONS
with tabs[8]:
    st.header("Third-party add-ons")
    st.caption("Each block is guarded — missing packages just show an install hint.")

    # ---- streamlit-extras
    st.subheader("streamlit-extras")
    try:
        from streamlit_extras.metric_cards import style_metric_cards
        from streamlit_extras.stoggle import stoggle
        from streamlit_extras.badges import badge

        stoggle("Click me!", "🥷 Surprise! Extra hidden content.")
        badge(type="github", name="streamlit/streamlit")
        c1, c2, c3 = st.columns(3)
        c1.metric("Metric A", "1.2k", "+5%")
        c2.metric("Metric B", "340", "-2%")
        c3.metric("Metric C", "99%", "+1%")
        style_metric_cards()
    except ImportError:
        missing("streamlit-extras")
    except Exception as e:  # extras occasionally break on new Streamlit versions
        st.error(f"streamlit-extras error: {e}")

    # ---- st-aggrid
    st.subheader("streamlit-aggrid")
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder

        gb = GridOptionsBuilder.from_dataframe(sample_df().head(30))
        gb.configure_pagination(paginationPageSize=8)
        gb.configure_side_bar()
        gb.configure_default_column(filter=True, sortable=True, resizable=True)
        gb.configure_selection("multiple", use_checkbox=True)
        AgGrid(sample_df().head(30), gridOptions=gb.build(), height=350, theme="streamlit")
    except ImportError:
        missing("streamlit-aggrid")
    except Exception as e:
        st.error(f"aggrid error: {e}")

    # ---- lottie
    st.subheader("streamlit-lottie")
    try:
        import requests
        from streamlit_lottie import st_lottie

        @st.cache_data(show_spinner=False)
        def load_lottie(url: str):
            r = requests.get(url, timeout=5)
            return r.json() if r.status_code == 200 else None

        anim = load_lottie("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")
        if anim:
            st_lottie(anim, height=180, key="lottie")
        else:
            st.caption("Couldn't fetch the Lottie JSON (offline?).")
    except ImportError:
        missing("streamlit-lottie requests")
    except Exception as e:
        st.caption(f"lottie skipped: {e}")

    # ---- agraph
    st.subheader("streamlit-agraph")
    try:
        from streamlit_agraph import Config, Edge, Node, agraph

        nodes = [Node(id=i, label=i, size=20) for i in ["ESP32", "MQTT", "Broker", "Grafana", "Streamlit"]]
        edges = [
            Edge(source="ESP32", target="MQTT"),
            Edge(source="MQTT", target="Broker"),
            Edge(source="Broker", target="Grafana"),
            Edge(source="Broker", target="Streamlit"),
        ]
        agraph(nodes=nodes, edges=edges, config=Config(width=600, height=250, directed=True))
    except ImportError:
        missing("streamlit-agraph")
    except Exception as e:
        st.error(f"agraph error: {e}")

    # ---- option menu
    st.subheader("streamlit-option-menu")
    try:
        from streamlit_option_menu import option_menu

        option_menu(
            None,
            ["Home", "Data", "Settings"],
            icons=["house", "table", "gear"],
            orientation="horizontal",
            key="opt_menu",
        )
    except ImportError:
        missing("streamlit-option-menu")
    except Exception as e:
        st.error(f"option-menu error: {e}")

    # ---- more
    st.subheader("More worth trying")
    st.markdown(
        "- [`streamlit-authenticator`](https://pypi.org/project/streamlit-authenticator/) — login\n"
        "- [`streamlit-folium`](https://pypi.org/project/streamlit-folium/) — Folium maps\n"
        "- [`streamlit-drawable-canvas`](https://pypi.org/project/streamlit-drawable-canvas/) — draw on canvas\n"
        "- [`streamlit-webrtc`](https://pypi.org/project/streamlit-webrtc/) — live video/audio\n"
        "- [`streamlit-elements`](https://pypi.org/project/streamlit-elements/) — Material UI + Nivo\n"
        "- [Component gallery](https://streamlit.io/components) — 200+ more"
    )

st.divider()
st.caption(f"Rendered {dt.datetime.now():%Y-%m-%d %H:%M:%S}")
