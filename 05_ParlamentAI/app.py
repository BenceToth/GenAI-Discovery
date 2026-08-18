from parlamentai_app_hf import build_ui

# Hugging Face Spaces and other ASGI/WSGI hosts look for a top-level `app` (or `demo`) object.
# Do NOT call `app.launch()` here — the host will run the app for you.
app = build_ui()
