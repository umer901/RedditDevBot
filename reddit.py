import praw
import re
import os
from main import run_analysis
from utils import upload_to_imgbb
from dotenv import load_dotenv

load_dotenv() 

client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")

reddit = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    username = username,
    password = password,
    user_agent = "<app:DevBot123:1.0>"
)

# Choose subreddits to monitor
# subreddit = reddit.subreddit("all") 
subreddit = reddit.subreddit("testingground4bots")

# Compile command pattern
command_pattern = re.compile(r"!devtrends\s+(\w+)", re.IGNORECASE)


replied_to = set()

for comment in subreddit.stream.comments(skip_existing=True):
    if comment.id in replied_to:
        continue

    match = command_pattern.search(comment.body)
    if match:
        keyword = match.group(1).lower()
        print(f"📡 Detected command for keyword: {keyword}")

        try:
            # Run the trend analysis

            # stats_main, graph_path = run_analysis(keyword)
            # stats_python, _ = run_analysis("python")
            # stats_js, _ = run_analysis("javascript")

            stats_main = run_analysis(keyword)
            # stats_python = run_analysis("python")
            # stats_js = run_analysis("javascript")


            # Upload graph to imgbb
            # image_url = upload_to_imgbb(graph_path)

            # Format reply
            reply = (
                f" **Developer Trends for `{keyword}` (Past 30 Days)**\n\n"
                f"- GitHub Repositories: **{stats_main['github']}**\n"
                f"- Stack Overflow Questions: **{stats_main['stack']}**\n"
                f"- Job Postings: **{stats_main['jobs']}**\n\n"
                # f" Google Trends Graph: [View Graph]({image_url})\n\n"
                f"---\n"
                f"**🔍 Comparison for reference**:\n\n"
                f"**Python**\n"
                f"- GitHub: 62\n"
                f"- Stack Overflow: 2222447\n"
                f"- Jobs: 331\n\n"
                f"**JavaScript**\n"
                f"- GitHub: 46\n"
                f"- Stack Overflow: 2536778\n"
                f"- Jobs: 113\n\n"
                f"---\n"
                f"^(I'm a bot that analyzes developer tech trends `!devtrends rust`, `!devtrends react`, etc. Work in Progress)"
            )

            comment.reply(reply)
            print("Replied to comment")
            replied_to.add(comment.id)

        except Exception as e:
            print(f"Error: {e}")


