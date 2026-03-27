import streamlit as st
import requests
from datetime import datetime, timedelta

# YouTube API Key
API_KEY = "YOUR_API_KEY_HERE"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Title
st.title("Ocean Mysteries Viral Topics Tool 🌊")

# Input Fields
days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

# 🔥 ULTRA VIRAL KEYWORDS (EXPANDED LIST)
keywords = [
    # Deep Sea Creatures
    "mysterious deep sea creatures discovered recently",
    "unexplained creatures in the Mariana Trench",
    "deepest ocean discoveries scientists made",
    "unknown animals living in deep ocean",
    "strange creatures caught by deep sea cameras",
    "deep sea creatures found by submarines",
    "scientists exploring the deepest ocean trench",
    "rare deep sea animals caught on camera",
    "unexplained life in the abyssal zone",
    "creatures that live without sunlight",

    # Ocean Mystery
    "unexplained ocean sounds recorded by scientists",
    "mysterious sounds from the deep ocean",
    "strange underwater discoveries scientists cannot explain",
    "ocean mysteries scientists still investigate",
    "secrets hidden in the Mariana Trench",
    "unexplained underwater structures discovered",
    "deep sea mysteries that shocked researchers",
    "ocean anomalies discovered by sonar",
    "strange signals detected in the ocean",
    "mysterious underwater phenomena",

    # Shipwreck Mystery
    "lost shipwrecks discovered in deep ocean",
    "mysterious ghost ships found at sea",
    "ancient shipwrecks discovered by divers",
    "lost submarines discovered underwater",
    "unexplained shipwreck mysteries",
    "deep ocean shipwreck discoveries",
    "historic ships found beneath the ocean",
    "hidden treasure ships underwater",
    "unexplained maritime disappearances",
    "underwater ruins discovered by scientists",

    # Deep Ocean Science
    "hydrothermal vent ecosystems explained",
    "life near underwater volcanoes",
    "animals living near hydrothermal vents",
    "creatures surviving extreme ocean pressure",
    "deep sea exploration technology explained",
    "robotic submarines exploring the ocean",
    "strange organisms discovered by oceanographers",
    "deep ocean food chain explained",
    "abyssal zone creatures documentary",
    "how life survives in deep ocean",

    # Viral Curiosity
    "terrifying deep sea creatures documentary",
    "scariest ocean creatures discovered",
    "mysterious creatures scientists cannot identify",
    "unexplained deep ocean discoveries",
    "alien like creatures from deep sea",
    "hidden worlds beneath the ocean",
    "strange ocean discoveries caught on camera",
    "deep sea mysteries documentary",
    "secrets scientists discovered underwater",
    "unexplained ocean discoveries"
]

# Fetch Data Button
if st.button("Fetch Data"):
    try:
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []

        for keyword in keywords:
            st.write(f"🔍 Searching: {keyword}")

            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": API_KEY,
            }

            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()

            if "items" not in data:
                continue

            video_ids = [v["id"]["videoId"] for v in data["items"] if "videoId" in v["id"]]
            channel_ids = [v["snippet"]["channelId"] for v in data["items"]]

            if not video_ids:
                continue

            stats = requests.get(YOUTUBE_VIDEO_URL, params={
                "part": "statistics",
                "id": ",".join(video_ids),
                "key": API_KEY
            }).json()

            channels = requests.get(YOUTUBE_CHANNEL_URL, params={
                "part": "statistics",
                "id": ",".join(channel_ids),
                "key": API_KEY
            }).json()

            for vid, stat, ch in zip(data["items"], stats.get("items", []), channels.get("items", [])):
                views = int(stat["statistics"].get("viewCount", 0))
                subs = int(ch["statistics"].get("subscriberCount", 0))

                # 🎯 GOLD FILTER
                if subs < 5000 and views > 1000:
                    all_results.append({
                        "Title": vid["snippet"]["title"],
                        "URL": f"https://www.youtube.com/watch?v={vid['id']['videoId']}",
                        "Views": views,
                        "Subscribers": subs
                    })

        if all_results:
            st.success(f"🚀 Found {len(all_results)} Viral Opportunities!")
            for r in all_results:
                st.markdown(
                    f"**{r['Title']}**\n\n"
                    f"👁 Views: {r['Views']} | 👤 Subs: {r['Subscribers']}\n\n"
                    f"[Watch Video]({r['URL']})"
                )
                st.write("---")
        else:
            st.warning("No strong opportunities found.")

    except Exception as e:
        st.error(f"Error: {e}")
