import streamlit as st
import subprocess
import tempfile
import os
import platform
from pathlib import Path


def _subprocess_flags():
    if platform.system() == "Windows":
        return {"creationflags": subprocess.CREATE_NO_WINDOW}
    return {}


def check_ffmpeg():
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True, text=True,
            **_subprocess_flags()
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def output_filename(original_name, pitch):
    p = Path(original_name)
    if abs(pitch) < 0.1:
        tag = "pitch_adjusted"
    elif pitch > 0:
        tag = "higher"
    else:
        tag = "lower"
    return f"{p.stem}_{tag}{p.suffix}"


def format_size(size_bytes):
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def _pitch_decrement():
    st.session_state["pitch_value"] = max(-20, st.session_state["pitch_value"] - 1)


def _pitch_increment():
    st.session_state["pitch_value"] = min(20, st.session_state["pitch_value"] + 1)


def _pitch_reset():
    st.session_state["pitch_value"] = 0


# ── Session state ────────────────────────────────────────────────────────────
for _key, _default in [
    ("pitch_value", 0),
    ("result_bytes", None),
    ("result_filename", None),
    ("result_logs", []),
    ("_last_upload", None),
]:
    if _key not in st.session_state:
        st.session_state[_key] = _default

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nostra - Video Pitch Shifter",
    page_icon="🎵",
    layout="wide",
)

st.title("🎵 Nostra - Video Pitch Shifter")
st.caption(
    "Adjust audio pitch in video files while preserving video sync and duration. — NostradmsX"
)

if not check_ffmpeg():
    st.error(
        "**FFMPEG not found.** Install FFMPEG and make sure it is on your PATH, "
        "then restart the app."
    )
    st.stop()

st.divider()

# ── Two-column layout ────────────────────────────────────────────────────────
controls_col, preview_col = st.columns([1, 1], gap="large")

with controls_col:

    # 1 · Upload ────────────────────────────────────────────────────────────
    st.subheader("1 · Upload")
    uploaded = st.file_uploader(
        "Upload a video file",
        type=["mp4", "mkv", "avi", "mov", "wmv", "flv"],
        help="Supported formats: MP4, MKV, AVI, MOV, WMV, FLV",
        label_visibility="collapsed",
    )

    if uploaded is not None:
        # Clear result when a new file is uploaded
        if uploaded.name != st.session_state["_last_upload"]:
            st.session_state["_last_upload"] = uploaded.name
            st.session_state["result_bytes"] = None
            st.session_state["result_logs"] = []

        size_mb = uploaded.size / (1024 * 1024)
        size_str = format_size(uploaded.size)
        if size_mb > 200:
            st.warning(
                f"Large file ({size_str}) — processing may take several minutes "
                "and could hit memory limits on the free Streamlit Cloud tier."
            )
        elif size_mb > 50:
            st.info(f"**{uploaded.name}** · {size_str}")
        else:
            st.caption(f"{uploaded.name} · {size_str}")

    st.divider()

    # 2 · Pitch ─────────────────────────────────────────────────────────────
    st.subheader("2 · Set Pitch")

    minus_col, slider_col, plus_col = st.columns([1, 10, 1])
    with minus_col:
        st.markdown('<div style="margin-top:28px"></div>', unsafe_allow_html=True)
        st.button("−", use_container_width=True, help="−1 semitone", on_click=_pitch_decrement)
    with slider_col:
        pitch = st.slider(
            "Semitones",
            min_value=-20, max_value=20,
            key="pitch_value",
            label_visibility="collapsed",
            help="Negative = lower pitch · Positive = higher pitch · ±12 = one octave",
        )
    with plus_col:
        st.markdown('<div style="margin-top:28px"></div>', unsafe_allow_html=True)
        st.button("+", use_container_width=True, help="+1 semitone", on_click=_pitch_increment)

    # Value summary + reset
    summary_col, reset_col = st.columns([4, 1])
    with summary_col:
        _references = {
            -12: "one octave lower", -5: "noticeably lower", -1: "slightly lower",
            0: "no change",
            1: "slightly higher", 5: "noticeably higher", 12: "one octave higher",
        }
        if pitch == 0:
            st.caption("No pitch change")
        else:
            _direction = "higher" if pitch > 0 else "lower"
            _label = f"{pitch:+d} semitone{'s' if abs(pitch) != 1 else ''} ({_direction} pitch)"
            _nearest = min(_references, key=lambda k: abs(k - pitch))
            if abs(pitch - _nearest) <= 2 and _nearest != pitch:
                _label += f" · ≈ {_references[_nearest]}"
            st.caption(_label)
    with reset_col:
        st.button("Reset", use_container_width=True, on_click=_pitch_reset)

    st.divider()

    # 3 · Process ────────────────────────────────────────────────────────────
    st.subheader("3 · Process")
    process_clicked = st.button(
        "🎬 Process Video",
        type="primary",
        disabled=uploaded is None,
        use_container_width=True,
    )

# ── Preview column ───────────────────────────────────────────────────────────
with preview_col:
    st.subheader("Preview")

    if uploaded is None:
        st.info("Upload a video on the left to see a preview here.")
    elif st.session_state["result_bytes"] is not None:
        before_tab, after_tab = st.tabs(["Original", "✅ Result"])
        with before_tab:
            st.video(uploaded)
        with after_tab:
            st.video(st.session_state["result_bytes"])
            st.download_button(
                label=f"⬇ Download  {st.session_state['result_filename']}",
                data=st.session_state["result_bytes"],
                file_name=st.session_state["result_filename"],
                mime="video/mp4",
                use_container_width=True,
            )
            with st.expander("Processing log"):
                st.text("\n".join(st.session_state["result_logs"]))
    else:
        st.video(uploaded)

# ── Processing ───────────────────────────────────────────────────────────────
if process_clicked:
    flags = _subprocess_flags()
    logs = []
    result_bytes = None

    with tempfile.TemporaryDirectory() as tmp:
        ext = Path(uploaded.name).suffix
        in_path = os.path.join(tmp, f"input{ext}")
        temp_audio = os.path.join(tmp, "extracted_audio.wav")
        temp_pitched = os.path.join(tmp, "pitched_audio.wav")
        out_name = output_filename(uploaded.name, pitch)
        out_path = os.path.join(tmp, out_name)

        with open(in_path, "wb") as f:
            f.write(uploaded.getbuffer())

        with st.status("Processing video…", expanded=True) as status:
            try:
                # Step 1: extract audio
                st.write("Step 1: Extracting audio from video…")
                r = subprocess.run(
                    ["ffmpeg", "-i", in_path,
                     "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2",
                     temp_audio, "-y"],
                    capture_output=True, text=True, **flags,
                )
                if r.returncode != 0:
                    raise RuntimeError(f"Audio extraction failed:\n{r.stderr}")
                logs.append("Audio extraction complete.")
                st.write("✅ Audio extracted.")

                # Step 2: pitch shift
                if abs(pitch) > 0.01:
                    st.write(f"Step 2: Adjusting pitch by {pitch:+.1f} semitones…")
                    pitch_ratio = 2 ** (pitch / 12.0)

                    r = subprocess.run(
                        ["ffmpeg", "-i", temp_audio,
                         "-af", f"rubberband=pitch={pitch_ratio}",
                         temp_pitched, "-y"],
                        capture_output=True, text=True, **flags,
                    )
                    if r.returncode != 0:
                        st.write("⚠️ Rubberband filter unavailable, using fallback method…")
                        logs.append("Using atempo fallback (rubberband unavailable).")
                        tempo_ratio = 1.0 / pitch_ratio
                        r = subprocess.run(
                            ["ffmpeg", "-i", temp_audio,
                             "-af", f"asetrate=44100*{pitch_ratio},aresample=44100,atempo={tempo_ratio}",
                             temp_pitched, "-y"],
                            capture_output=True, text=True, **flags,
                        )
                        if r.returncode != 0:
                            raise RuntimeError(f"Pitch adjustment failed:\n{r.stderr}")
                    else:
                        logs.append("Using rubberband filter.")

                    logs.append("Pitch adjustment complete (duration preserved).")
                    st.write("✅ Pitch adjusted.")
                    audio_to_merge = temp_pitched
                else:
                    st.write("Step 2: Skipped (0 semitones — no pitch change needed).")
                    logs.append("Step 2: Skipped (0 semitones).")
                    audio_to_merge = temp_audio

                # Step 3: merge
                st.write("Step 3: Merging audio back with video…")
                r = subprocess.run(
                    ["ffmpeg", "-i", in_path, "-i", audio_to_merge,
                     "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                     "-map", "0:v:0", "-map", "1:a:0",
                     out_path, "-y"],
                    capture_output=True, text=True, **flags,
                )
                if r.returncode != 0:
                    raise RuntimeError(f"Video merge failed:\n{r.stderr}")

                logs.append("Merge complete. Done!")
                st.write("✅ Done!")
                status.update(label="Processing complete!", state="complete")

                with open(out_path, "rb") as f:
                    result_bytes = f.read()

            except RuntimeError as e:
                st.error(str(e))
                status.update(label="Processing failed.", state="error")

    if result_bytes is not None:
        st.session_state["result_bytes"] = result_bytes
        st.session_state["result_filename"] = out_name
        st.session_state["result_logs"] = logs
        st.rerun()
