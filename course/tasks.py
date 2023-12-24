from celery import shared_task
import moviepy.editor

@shared_task
def audio_to_transcript(module, video_url):
    video = moviepy.editor.VideoFileClip(video_url)
    audio = video.audio
    if audio is not None:
        audio.write_audiofile("sample.mp3")
    else:
        print("The video file does not have an audio track")
        
