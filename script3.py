import subprocess
import openai
from openai import OpenAI
from moviepy.editor import VideoFileClip
import json


# Initialize the OpenAI client with API key
client = OpenAI(api_key="")

def convert_mp4_to_mp3(mp4_file_path, mp3_file_path):
    try:
        video_clip = VideoFileClip(mp4_file_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(mp3_file_path)
        video_clip.close()
        audio_clip.close()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def mp3_to_srt(mp3_file_path):
    with open(mp3_file_path, 'rb') as audio_file:
        transcript_response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="srt"
        )
    srt_file_path = mp3_file_path.rsplit('.', 1)[0] + '.srt'
    with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
        srt_file.write(transcript_response)
    return srt_file_path

def add_subtitles_to_video(input_video_path, output_video_path, srt_path):
    ffmpeg_command = [
        "ffmpeg",
        "-i", input_video_path,
        "-vf", f"subtitles={srt_path}",
        "-c:a", "copy",
        output_video_path
    ]
    subprocess.run(ffmpeg_command, shell=False)

# Paths for your video, audio, and output
input_video_path = "output_video_with_audio1.mp4"  # Replace with your input video path
mp3_file_path = "output_video_with_audio.mp3"    # Replace with your output MP3 path
output_video_path = "output_video_with_audio1_and_subs.mp4"  # Replace with your output video path

# Convert MP4 to MP3
conversion_success = convert_mp4_to_mp3(input_video_path, mp3_file_path)
if conversion_success:
    # Convert MP3 to SRT
    srt_path = mp3_to_srt(mp3_file_path)
    # Add subtitles to video
    add_subtitles_to_video(input_video_path, output_video_path, srt_path)
    print("Subtitles added to the video successfully!")
else:
    print("Failed to convert MP4 to MP3.")
