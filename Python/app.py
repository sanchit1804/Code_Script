import instaloader

# Create an instance
loader = instaloader.Instaloader()

# Login if needed (for private accounts you follow)
# loader.login("your_username", "your_password")

# Download a single post by URL
post_url = "https://www.instagram.com/p/POST_ID/"
post = instaloader.Post.from_shortcode(loader.context, post_url.split("/")[-2])

loader.download_post(post, target="downloaded_photos")

print("Photo downloaded successfully!")
