"""Run this to test your Gemini API key"""
import os

# Load .env manually
env_path = ".env"
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, _, val = line.partition("=")
                os.environ[key.strip()] = val.strip()

key = os.environ.get("GEMINI_API_KEY", "")
print(f"API Key found: {'YES — ' + key[:8] + '...' if key else 'NO — key is missing!'}")

if not key:
    print("\nFix: Open your .env file and make sure it has:")
    print("GEMINI_API_KEY=your_actual_key_here")
else:
    import google.generativeai as genai
    genai.configure(api_key=key)
    print("\nTesting available models...")
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f"  ✅ {m.name}")