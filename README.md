# DreamForge VR

DreamForge VR is an AR/VR web app prototype that lets homeowners visualise their house in 3D before construction, swap materials instantly, and get live cost estimates in INR.

## Local Run

Requires Python 3 and `pip install flask flask-cors requests`.

1. **Start the backend server:**
   ```bash
   python server.py
   ```
2. **Access local preview:**
   Simply open `index.html` in your browser. (The backend runs on `localhost:8000`).

## Deployment (GitHub Pages)

Achieve a live build in under a minute without zero build steps:
1. Commit this entire folder to a GitHub repository.
2. Go to `Settings -> Pages`.
3. Set the source branch to `main` and root directory.
4. Open your live GitHub pages deployment URL!
5. Update the URL input box in your `dashboard.html` to generate an accurate QR code.

## Environment Variables
- `OPENAI_API_KEY`: Required for the Flask server to parse new blueprints via `POST /parse-blueprint` route using GPT-4o. 
*(If no API key is provided, the app continues to work seamlessly with the pre-built `house.json` fallback).*

## Demo Flow
Open `dashboard.html` → scan QR with mobile device → hand phone to the user (or judge) → they immediately experience the 3D property in AR via WebXR. Watch costs update live as they modify room finishes!

# AR Demo on Phone (Hackathon Day)
AR requires HTTPS. Use ngrok for local testing:

Step 1: Install ngrok → https://ngrok.com/download
Step 2: In terminal 1 → python server.py
Step 3: In terminal 2 → ngrok http 5000
Step 4: Copy the HTTPS URL from ngrok (e.g. https://abc123.ngrok.io)
Step 5: Open that URL on your Android phone in Chrome
Step 6: Tap "AR Mode" → point camera at floor → rooms appear
Step 7: Tap any room → swap material → judges see cost update on laptop dashboard

Note: GitHub Pages deployment is HTTPS by default — no ngrok needed after deploy.
