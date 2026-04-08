import os
import json

VIDEO_EXTS = {".mp4", ".mkv", ".mov", ".wmv", ".flv", ".m4v", ".webm"}


def play_local_video(query=None, internet_tools=None):
    """
    Play a video file from the local video directory.
    Use this ONLY when the user wants to PLAY or WATCH a video.
    For listing, finding or browsing video files use file_explorer instead.
    """

    json_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "music.json"))
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            video_dir = data.get("video_dir", r"D:\Videos")
    except Exception:
        video_dir = r"D:\Videos"

    if not os.path.isdir(video_dir):
        return f"Video directory not found: {video_dir}"

    all_files = []
    for root, _, files in os.walk(video_dir):
        for f in files:
            if os.path.splitext(f)[1].lower() in VIDEO_EXTS:
                all_files.append(os.path.join(root, f))

    if not all_files:
        return f"No video files found in {video_dir}"

    matches = all_files

    if query:
        terms = query.lower().split()

        stop = {"mp4", "mkv", "mov", "play", "the", "a", "an", "some",
                "video", "film", "movie", "clip", "watch", "star", "trek",
                "wars", "of", "to", "and", "in", "from", "with", "for"}
        terms = [t for t in terms if t not in stop]

        if terms:
            scored = []
            for f in all_files:
                name = os.path.basename(f).lower()
                score = sum(len(t) for t in terms if t in name)
                if score > 0:
                    scored.append((score, f))

            scored.sort(key=lambda x: x[0], reverse=True)

            if scored:
                top_score = scored[0][0]
                matches = [f for s, f in scored if s == top_score]
            else:
                matches = []

    if not matches:
        return f"No video found matching: {query}"

    chosen = matches[0]
    os.startfile(chosen)
    msg = f"Playing: {os.path.basename(chosen)}\n[VIDEO:{chosen}]"

    if len(matches) > 1:
        others = "\n".join(os.path.basename(m) for m in matches[1:4])
        msg += f"\n\nOther close matches:\n{others}"

    return msg