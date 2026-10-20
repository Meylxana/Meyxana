import os
from gtts import gTTS
from moviepy import AudioFileClip, ColorClip

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

AI_CONTENT_POOL = [
    {
        "script": "Did you know? AI can now predict protein structures in minutes, solving 50-year-old biology mysteries.",
        "title": "AI Solves 50-Year-Old Biology Mystery! 🧬 #shorts",
        "description": "Artificial intelligence is changing biology forever by predicting protein structures in minutes.",
        "tags": ["ai", "biology", "shorts", "science"],
    },
    {
        "script": "Neuralink's brain-chip technology is letting people play video games with their mind.",
        "title": "Play Games With Your Mind? Neuralink's New Tech! 🧠 #shorts",
        "description": "Brain-computer interfaces are becoming a reality as people play games using only their thoughts.",
        "tags": ["ai", "tech", "neuralink", "shorts"],
    },
]

def create_and_upload_video():
    print("\n--- GitHub Actions: Yeni video yaratma prosesi başladı ---")
    
    # Sadəlik üçün ilk məzmunu götürürük
    content = AI_CONTENT_POOL[0]
    
    script = content["script"]
    title = content["title"]
    description = content["description"]
    tags = content["tags"]
    
    # 1. Audio yaratmaq (gTTS)
    print("1. Səs faylı yaradılır...")
    tts = gTTS(text=script, lang="en")
    tts.save("voice.mp3")
    
    # 2. Fon videosu yaratmaq
    print("2. Fon videosu yaradılır...")
    audio_clip = AudioFileClip("voice.mp3")
    duration = audio_clip.duration
    
    video_clip = ColorClip(size=(1080, 1920), color=(15, 15, 35), duration=duration)
    
    # 3. Video və səsi birləşdirmək
    print("3. Video və səs birləşdirilir...")
    final_clip = video_clip.with_audio(audio_clip)
    final_clip.write_videofile("final_output.mp4", fps=24, codec="libx264", audio_codec="aac")
    
    # 4. YouTube-a yükləmək
    print("4. YouTube-a yüklənir...")
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    credentials = flow.run_local_server(port=0, open_browser=False)
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "28"
        },
        "status": {
            "privacyStatus": "public"
        }
    }
    
    media = MediaFileUpload("final_output.mp4", chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    api_response = request.execute()
    print(f"Uğurla yükləndi! Video ID: {api_response.get('id')}")
    print("--- Proses tamamlandı ---\n")

if __name__ == "__main__":
    create_and_upload_video()
