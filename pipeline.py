from data.sfm import reconstruct
from data.video import browse_file, extract_frames


def run_pipeline():
    video_path = browse_file()
    if not video_path:
        return None

    frames_dir = extract_frames(video_path)
    colmap_reconstruction = reconstruct(frames_dir)

    return colmap_reconstruction