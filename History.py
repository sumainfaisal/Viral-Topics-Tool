import streamlit as st
import requests
from datetime import datetime, timedelta

# -----------------------------
# YouTube API Configuration
# -----------------------------
API_KEY = "AIzaSyAx17oU8RXT4TpsUvuAjDz9cH1MVGnDtBI"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# -----------------------------
# Streamlit App UI
# -----------------------------
st.title("YouTube Viral Topics Tool")

days = st.number_input(
    "Enter Days to Search (1–30):",
    min_value=1,
    max_value=30,
    value=5
)

# -----------------------------
# Keywords List (FIXED)
# -----------------------------
keywords = [
    "Dark History",
    "Untold History",
    "Historical Injustice",
    "Real History Stories",
    "True History Documentary",
    "History Documentary",
    "Forgotten Wars",
    "Ancient Civilizations",
    "Medieval History",
    "War Crimes History",
    "History Storytelling",
    "Lost Empires",
    "Fallen Kingdoms",
    "History Facts",
    "World History Explained"
]

# -----------------------------
# Fetch Data Logic
# -----------------------------
if st.button("Fetch Data"):
    try:
        start_date = (
            datetime.utcnow() - timedelta(days=int(days))
        ).isoformat("T") + "Z"

        all_results = []

        for keyword in keywords:
            st.write(f"🔍 Searching for: **{keyword}**")

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

            if "items" not in data or not data["items"]:
                st.warning(f"No videos found for: {keyword}")
                continue

            video_ids = [
                item["id"]["videoId"]
                for item in data["items"]
                if "videoId" in item.get("id", {})
            ]

            channel_ids = [
                item["snippet"]["channelId"]
                for item in data["items"]
                if "channelId" in item.get("snippet", {})
            ]

            if not video_ids or not channel_ids:
                continue

            # Video statistics
            stats_response = requests.get(
                YOUTUBE_VIDEO_URL,
                params={
                    "part": "statistics",
                    "id": ",".join(video_ids),
                    "key": API_KEY,
                },
            )
            stats_data = stats_response.json()

            # Channel statistics
            channel_response = requests.get(
                YOUTUBE_CHANNEL_URL,
                params={
                    "part": "statistics",
                    "id": ",".join(channel_ids),
                    "key": API_KEY,
                },
            )
            channel_data = channel_response.json()

            if "items" not in stats_data or "items" not in channel_data:
                continue

            for video, stat, channel in zip(
                data["items"], stats_data["items"], channel_data["items"]
            ):
                views = int(stat["statistics"].get("viewCount", 0))
                subs = int(channel["statistics"].get("subscriberCount", 0))

                if subs < 3000:
                    all_results.append({
                        "Title": video["snippet"]["title"],
                        "Description": video["snippet"]["description"][:200],
                        "URL": f"https://www.youtube.com/watch?v={video['id']['videoId']}",
                        "Views": views,
                        "Subscribers": subs,
                    })

        # -----------------------------
        # Display Results
        # -----------------------------
        if all_results:
            st.success(f"✅ Found {len(all_results)} viral opportunities!")
            for result in all_results:
                st.markdown(
                    f"""
                    **Title:** {result['Title']}  
                    **Description:** {result['Description']}  
                    **Views:** {result['Views']}  
                    **Subscribers:** {result['Subscribers']}  
                    **URL:** [Watch Video]({result['URL']})
                    ---
                    """
                )
        else:
            st.warning("No results found under 3,000 subscribers.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
