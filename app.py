from flask import Flask, render_template, request
import praw

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username='',
                     password='',
                     user_agent='postscroller')


app = Flask(__name__)
app.config['SECRET_KEY'] = "s421akfj16sac72gjalasf251"

def fetch_posts(subreddits, num_posts):
    
    posts = []
    for subreddit in subreddits:
        subreddit = reddit.subreddit(subreddit)
        hot_posts = subreddit.top(limit=num_posts)
        for post in hot_posts:
            if (not post.is_video and post.url.endswith(('jpg', 'jpeg', 'png', 'gif'))) or (post.is_video and post.media and post.media['reddit_video']['fallback_url']):
                posts.append(post)

    return posts

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        subreddits = request.form['subreddits']
        subreddits_list = [subreddit.strip() for subreddit in subreddits.split(',')]
        num_posts = int(request.form.get('num_posts', 100))
        posts = fetch_posts(subreddits_list, num_posts)
    else:
        posts = fetch_posts(['LandscapePhotography'], 50)

    return render_template('home.html', posts=posts)


if __name__ == '__main__':
  app.run(debug=True)