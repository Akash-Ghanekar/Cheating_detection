import os

print("🔍 Searching for your trained model...")
print("="*50)

# Search in all possible locations
search_folders = [
    r"C:\Users\ghane\Desktop\Detection_project",
    r"C:\Users\ghane\Desktop\Detection_project\code",
    r"C:\Users\ghane\Desktop\Detection_project\runs",
    r"C:\Users\ghane\Desktop\Detection_project\code\runs",
]

found_models = []

for folder in search_folders:
    if os.path.exists(folder):
        for root, dirs, files in os.walk(folder):
            if "best.pt" in files:
                model_path = os.path.join(root, "best.pt")
                found_models.append(model_path)
                print(f"✅ Found: {model_path}")

if found_models:
    print("\n" + "="*50)
    print("📁 COPY THIS PATH for your code:")
    print(found_models[0])
    print("="*50)
else:
    print("\n❌ No model found!")
    print("You need to train first. Run: python main.py")