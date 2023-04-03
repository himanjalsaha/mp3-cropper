from moviepy.editor import *
audioclip = AudioFileClip("website/upload/music (4).mp3")

audio_clip=audioclip.subclip("00:00:13","00:00:15")
audio_clip.write_audiofile("sound.mp3")
