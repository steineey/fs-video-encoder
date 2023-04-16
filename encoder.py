import subprocess

def mp4_encode(file_input, file_output, width=1920, preset="medium", stdout=None):
    cmd = [
        "ffmpeg", 
        "-i", file_input, 
        "-c:v", "libx265", 
        "-crf", "32",
        "-vf", f"scale={str(width)}:-2",
        "-preset", preset,  # use "veryslow" for best compression
        "-tag:v", "hvc1",
        "-movflags", "faststart",
        file_output
    ]
    cp = subprocess.run(cmd, stdout=stdout, stderr=subprocess.STDOUT)
    return cp.returncode

def webm_encode(file_input, file_output, width=1920, deadline="good", stdout=None):
    cmd = [
        "ffmpeg",
        "-i", file_input,
        "-c:v", "libvpx-vp9",
        "-crf", "40",
        "-vf", f"scale={str(width)}:-2",
        "-deadline", deadline,  # use "best" for best compression
        file_output
    ]
    cp = subprocess.run(cmd, stdout=stdout, stderr=subprocess.STDOUT)
    return cp.returncode