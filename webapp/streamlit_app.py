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


def process_video(input_path, output_path, pitch_change):
    """Run the three-step ffmpeg pipeline. Returns a list of log lines."""
    logs = []
    flags = _subprocess_flags()

    with tempfile.TemporaryDirectory() as tmp:
        temp_audio = os.path.join(tmp, "extracted_audio.wav")
        temp_pitched = os.path.join(tmp, "pitched_audio.wav")

        logs.append(f"Pitch adjustment: {pitch_change:.1f} semitones")

        # Step 1: extract audio
        logs.append("Step 1: Extracting audio from video...")
        r = subprocess.run(
            ["ffmpeg", "-i", input_path,
             "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2",
             temp_audio, "-y"],
            capture_output=True, text=True, **flags
        )
        if r.returncode != 0:
            raise RuntimeError(f"Audio extraction failed:\n{r.stderr}")
        logs.append("Audio extraction complete.")

        # Step 2: pitch shift
        if abs(pitch_change) > 0.01:
            logs.append(f"Step 2: Adjusting pitch by {pitch_change:.1f} semitones...")
            pitch_ratio = 2 ** (pitch_change / 12.0)

            r = subprocess.run(
                ["ffmpeg", "-i", temp_audio,
                 "-af", f"rubberband=pitch={pitch_ratio}",
                 temp_pitched, "-y"],
                capture_output=True, text=True, **flags
            )
            if r.returncode != 0:
                logs.append("Rubberband unavailable, falling back to atempo method...")
                tempo_ratio = 1.0 / pitch_ratio
                r = subprocess.run(
                    ["ffmpeg", "-i", temp_audio,
                     "-af", f"asetrate=44100*{pitch_ratio},aresample=44100,atempo={tempo_ratio}",
                     temp_pitched, "-y"],
                    capture_output=True, text=True, **flags
                )
                if r.returncode != 0:
                    raise RuntimeError(f"Pitch adjustment failed:\n{r.stderr}")
            else:
                logs.append("Using rubberband filter.")

            logs.append("Pitch adjustment complete (duration preserved).")
            audio_to_merge = temp_pitched
        else:
            logs.append("Step 2: Skipped (0 semitones).")
            audio_to_merge = temp_audio

        # Step 3: merge back
        logs.append("Step 3: Merging audio back with video...")
        r = subprocess.run(
            ["ffmpeg", "-i", input_path, "-i", audio_to_merge,
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
             "-map", "0:v:0", "-map", "1:a:0",
             output_path, "-y"],
            capture_output=True, text=True, **flags
        )
        if r.returncode != 0:
            raise RuntimeError(f"Video merge failed:\n{r.stderr}")

        logs.append("Merge complete.")
        logs.append("Done!")

    return logs


def output_filename(original_name, pitch):
    p = Path(original_name)
    if abs(pitch) < 0.1:
        tag = "pitch_adjusted"
    elif pitch > 0:
        tag = "higher"
    else:
        tag = "lower"
    return f"{p.stem}_{tag}{p.suffix}"


# ── Session state defaults ──────────────────────────────────────────────────
if "pitch_value" not in st.session_state:
    st.session_state["pitch_value"] = 0
if "result_bytes" not in st.session_state:
    st.session_state["result_bytes"] = None
if "result_filename" not in st.session_state:
    st.session_state["result_filename"] = None
if "result_logs" not in st.session_state:
    st.session_state["result_logs"] = []

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nostra - Video Pitch Shifter",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 Video Pitch Adjuster")
st.caption("Adjust audio pitch in video files while preserving video sync and duration.")

if not check_ffmpeg():
    st.error(
        "**FFMPEG not found.** Install FFMPEG and make sure it is on your PATH, "
        "then restart the app."
    )
    st.stop()

st.divider()

# ── Upload ───────────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "Upload a video file",
    type=["mp4", "mkv", "avi", "mov", "wmv", "flv"],
    help="Supported: MP4, MKV, AVI, MOV, WMV, FLV",
)

# Clear previous result when a new file is uploaded
if uploaded is not None and uploaded.name != st.session_state.get("_last_upload"):
    st.session_state["_last_upload"] = uploaded.name
    st.session_state["result_bytes"] = None

st.divider()

# ── Pitch controls ───────────────────────────────────────────────────────────
st.subheader("Pitch Adjustment")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("−1 semitone", use_container_width=True):
        st.session_state["pitch_value"] = max(-20, st.session_state["pitch_value"] - 1)
with col2:
    if st.button("Reset (0)", use_container_width=True):
        st.session_state["pitch_value"] = 0
with col3:
    if st.button("+1 semitone", use_container_width=True):
        st.session_state["pitch_value"] = min(20, st.session_state["pitch_value"] + 1)

pitch = st.slider(
    "Semitones",
    min_value=-20, max_value=20,
    key="pitch_value",
    help="Negative = lower pitch · Positive = higher pitch · ±12 = one octave",
)

references = {-12: "one octave lower", -5: "noticeably lower", -1: "slightly lower",
               0: "no change", 1: "slightly higher", 5: "noticeably higher", 12: "one octave higher"}
nearest = min(references, key=lambda k: abs(k - pitch))
if abs(pitch - nearest) <= 2:
    st.caption(f"Reference: {pitch} semitones ≈ {references[nearest]}")

st.divider()

# ── Process ──────────────────────────────────────────────────────────────────
if st.button(
    "Process Video",
    type="primary",
    disabled=uploaded is None,
    use_container_width=True,
):
    with tempfile.TemporaryDirectory() as tmp:
        ext = Path(uploaded.name).suffix
        in_path = os.path.join(tmp, f"input{ext}")
        out_name = output_filename(uploaded.name, pitch)
        out_path = os.path.join(tmp, out_name)

        with open(in_path, "wb") as f:
            f.write(uploaded.getbuffer())

        with st.spinner("Processing… this may take a minute for large files."):
            try:
                logs = process_video(in_path, out_path, pitch)
                with open(out_path, "rb") as f:
                    st.session_state["result_bytes"] = f.read()
                st.session_state["result_filename"] = out_name
                st.session_state["result_logs"] = logs
            except RuntimeError as e:
                st.error(str(e))
                st.session_state["result_bytes"] = None

# ── Download ─────────────────────────────────────────────────────────────────
if st.session_state["result_bytes"] is not None:
    st.success("Processing complete — your file is ready.")

    with st.expander("Processing log"):
        st.text("\n".join(st.session_state["result_logs"]))

    st.download_button(
        label=f"Download  {st.session_state['result_filename']}",
        data=st.session_state["result_bytes"],
        file_name=st.session_state["result_filename"],
        mime="video/mp4",
        use_container_width=True,
    )
