import subprocess
from fractions import Fraction
from pathlib import Path
from tkinter import Tk, filedialog

import ffmpeg
from tqdm import tqdm


def browse_file():

    root = Tk()
    root.withdraw()

    filetypes = (
        ("Video files", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
        ("All files", "*.*"),
    )
    
    file_path = filedialog.askopenfilename(
        title = "Select a video file",
        filetypes = filetypes
    )

    root.destroy()
    return file_path


def extract_frames(file_path):
    
    if not file_path:
        print("No video file supplied!")
        return None
    
    path = Path(file_path)
    output_dir = path.parent / f"{path.stem}_frames"
    output_dir.mkdir(parents=True, exist_ok=True)

    probe = ffmpeg.probe(file_path)

    video_stream = None
    for stream in probe["streams"]:
        if stream["codec_type"] == "video":
            video_stream = stream
            break

    if video_stream is None:
        raise ValueError("No video stream found.")

    print("Metadata:")
    print(f"Resolution: {video_stream.get('width')} x {video_stream.get('height')}")
    print(f"Frame rate: {int(Fraction(video_stream.get('avg_frame_rate')))}")
    print(f"Duration (sec): {video_stream.get('duration')}\n")
    
    frames = (
        ffmpeg.input(file_path)
        .output(str(output_dir / "frame_%06d.png"), compression_level=1)
        .overwrite_output()
        .global_args("-progress", "pipe:1", "-nostats", "-loglevel", "quiet")
    )

    process = frames.run_async(
        pipe_stdout=True,
        pipe_stderr=subprocess.DEVNULL 
    )

    with tqdm(desc="Extracting frames", total=int(video_stream.get("nb_frames")), unit="frames") as pbar:
        for line in process.stdout:
            key, _, value = line.decode().strip().partition("=")
            if key == "frame":
                current = int(value)
                pbar.update(current - pbar.n)

    process.wait()
    return output_dir
    
    