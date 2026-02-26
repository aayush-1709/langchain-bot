import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY") or "AIzaSyB0ocbA6WPKLoH37uSayWxJSh54voAemdM")

models = list(genai.list_models())

print("\n======= AVAILABLE MODELS =======\n")

for i, model in enumerate(models, start=1):
    print(f"{i}. {model.name}")

    if hasattr(model, "supported_generation_methods"):
        print("   Methods:", model.supported_generation_methods)

print(f"\nTotal models available: {len(models)}")

# Explicit check for gemini-2.5-flash
target = "gemini-2.5-flash"
found = False

print("\n======= CHECKING gemini-2.5-flash =======\n")

for model in models:
    if target in model.name:
        found = True
        print("FOUND:", model.name)
        print("Supported methods:", model.supported_generation_methods)

if not found:
    print("❌ gemini-2.5-flash is NOT available on your API key.")

print("\nDone.")