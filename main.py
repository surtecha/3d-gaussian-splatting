from data import video

frames = video.browse_file()
path = video.extract_frames(frames)

print(path)

