from moviepy.editor import VideoFileClip, AudioFileClip

def merge_audio_video(video_path, audio_path, output_path):
    # Load the video clip
    video_clip = VideoFileClip(video_path)
    
    # Load the audio clip
    audio_clip = AudioFileClip(audio_path)
    
    # Set the audio of the video clip
    final_clip = video_clip.set_audio(audio_clip)
    
    # Write the result to the output path
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

# Example usage
video_path = "/2024-10-05_14-23-19/output_video1.mp4"  # Replace with your MP4 file path
audio_path = "/2024-10-05_13-42-39/ElevenLabs_2024-10-05T08_24_17_Brian_pre_s50_sb75_se0_m2.mp3"  # Replace with your MP3 file path
output_path = "/2024-10-05_14-23-19/output_video_with_audio1.mp4"  # Replace with your desired output file path

merge_audio_video(video_path, audio_path, output_path)
