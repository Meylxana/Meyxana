import os
import google.auth.transport.requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def create_and_upload_video():
    creds = None
    if os.path.exists('token.json'):
        creds = google.oauth2.credentials.Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    youtube = build('youtube', 'v3', credentials=creds)

    body = {
        "snippet": {
            "title": "Meyxana Shorts #shorts",
            "description": "Avtomatik yüklənmiş meyxana videosu.",
            "tags": ["meyxana", "shorts"],
            "categoryId": "24"
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
    print("--- Proses tamamlandı ---")

if __name__ == '__main__':
    create_and_upload_video()
