import os

print("Searching for video files...")
print("="*40)

# Search for mp4 files
search_folders = [
    r"C:\Users\ghane\Desktop\Detection_project",
    r"C:\Users\ghane\Desktop\Detection_project\code",
    r"C:\Users\ghane\Desktop",
]

found_videos = []

for folder in search_folders:
    if os.path.exists(folder):
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith('.mp4'):
                    video_path = os.path.join(root, file)
                    found_videos.append(video_path)
                    print(f"✅ Found: {video_path}")

if not found_videos:
    print("❌ No .mp4 files found!")
    print("\nPlease put your video file in one of these folders:")
    print("1. C:\\Users\\ghane\\Desktop\\Detection_project\\videos\\")
    print("2. C:\\Users\\ghane\\Desktop\\Detection_project\\code\\videos\\")