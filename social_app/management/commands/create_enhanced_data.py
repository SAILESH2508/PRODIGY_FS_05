import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from social_app.models import Post, Comment, Profile, Like, Notification
from social_app.utils import process_post_content, create_notification

class Command(BaseCommand):
    help = 'Creates enhanced mock data with hashtags, mentions, and realistic content'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating enhanced mock data...')

        # Get existing users
        users = list(User.objects.all())
        if len(users) < 5:
            self.stdout.write('Not enough users. Please run populate_db first.')
            return

        # Enhanced post content with hashtags and mentions
        enhanced_posts = [
            "Just finished an amazing #coding session! Working on a new #django project 🚀 #webdevelopment",
            "Beautiful sunset today! 🌅 #photography #nature #peaceful",
            "Coffee and code - the perfect combination ☕ #programming #developer #lifestyle",
            "Excited to share my latest #design project! What do you think? #ui #ux #creative",
            "Learning #python has been such a rewarding journey! 🐍 #learning #tech #growth",
            "Weekend vibes! Time to relax and recharge 😎 #weekend #selfcare #balance",
            "Just deployed my first #react app! Feeling accomplished 💪 #javascript #frontend",
            "Amazing #conference today! So many inspiring speakers #tech #networking #inspiration",
            "Working on some #ai experiments. The future is here! 🤖 #machinelearning #innovation",
            "Grateful for this amazing community! You all inspire me daily ❤️ #community #grateful",
            "New blog post is live! Check it out and let me know your thoughts 📝 #blogging #writing",
            "Debugging can be frustrating but so satisfying when you find the solution! 🐛 #debugging #programming",
            "Just finished reading an amazing book on #productivity. Highly recommend! 📚 #books #learning",
            "Team lunch today! Great to connect with colleagues 🍕 #team #work #culture",
            "Working late but loving every minute of it! #passion #dedication #hustle",
            "Trying out a new #framework today. Always exciting to learn something new! #development #learning",
            "Beautiful weather for a walk in the park 🌳 #nature #health #mindfulness",
            "Just pushed my code to #github. Open source contributions feel great! #opensource #collaboration",
            "Attending a #hackathon this weekend! Can't wait to build something awesome 💻 #innovation #competition",
            "Celebrating small wins today! Progress is progress 🎉 #motivation #success #growth"
        ]

        # Create enhanced posts with hashtags
        created_posts = []
        for i, content in enumerate(enhanced_posts[:15]):  # Create 15 enhanced posts
            user = random.choice(users)
            
            # Add random mentions to some posts
            if random.random() < 0.3:  # 30% chance of mention
                mentioned_user = random.choice([u for u in users if u != user])
                content += f" Thanks @{mentioned_user.username} for the inspiration!"
            
            post = Post.objects.create(user=user, content=content)
            process_post_content(post)  # Process hashtags and mentions
            created_posts.append(post)
            
            # Pin some posts randomly
            if random.random() < 0.2:  # 20% chance to pin
                post.is_pinned = True
                post.save()
            
            self.stdout.write(f'Created enhanced post by {user.username}')

        # Create more realistic comments
        comment_templates = [
            "Great post! Really inspiring 👏",
            "Thanks for sharing this! Very helpful",
            "Love this! Keep up the great work 🔥",
            "Totally agree with you on this",
            "This is exactly what I needed to hear today",
            "Amazing work! How did you get started with this?",
            "So cool! I'm working on something similar",
            "This made my day! Thank you 😊",
            "Incredible! Would love to learn more about this",
            "Fantastic! Any tips for beginners?",
            "This is so motivating! 💪",
            "Wow! This is really impressive",
            "Thanks for the inspiration! 🙏",
            "Love seeing content like this!",
            "This is gold! Saving for later 💎"
        ]

        # Add comments to posts
        for post in created_posts:
            # Random number of comments (0-5)
            num_comments = random.randint(0, 5)
            commenters = random.sample([u for u in users if u != post.user], 
                                     min(num_comments, len(users)-1))
            
            for commenter in commenters:
                comment_text = random.choice(comment_templates)
                comment = Comment.objects.create(
                    post=post,
                    user=commenter,
                    text=comment_text
                )
                
                # Create notification for comment
                create_notification(
                    recipient=post.user,
                    sender=commenter,
                    notification_type='comment',
                    message=f"{commenter.username} commented on your post",
                    post=post,
                    comment=comment
                )
                
                # Add some replies to comments (30% chance)
                if random.random() < 0.3:
                    reply_text = random.choice([
                        "Thanks! Glad you liked it 😊",
                        "Absolutely! Let me know if you have questions",
                        "Thank you for the kind words! 🙏",
                        "Really appreciate the feedback!",
                        "So glad this was helpful!"
                    ])
                    
                    reply = Comment.objects.create(
                        post=post,
                        user=post.user,  # Post author replies
                        text=reply_text,
                        parent=comment
                    )

        # Add likes to posts
        for post in created_posts:
            # Random number of likes (1-8)
            num_likes = random.randint(1, 8)
            likers = random.sample([u for u in users if u != post.user], 
                                 min(num_likes, len(users)-1))
            
            for liker in likers:
                Like.objects.create(user=liker, post=post)
                
                # Create notification for like
                create_notification(
                    recipient=post.user,
                    sender=liker,
                    notification_type='like',
                    message=f"{liker.username} liked your post",
                    post=post
                )

        # Create some follow relationships
        for user in users[:10]:  # First 10 users follow others
            # Each user follows 3-6 random other users
            num_follows = random.randint(3, 6)
            to_follow = random.sample([u for u in users if u != user], 
                                    min(num_follows, len(users)-1))
            
            for target in to_follow:
                user.profile.follows.add(target.profile)
                
                # Create follow notification
                create_notification(
                    recipient=target,
                    sender=user,
                    notification_type='follow',
                    message=f"{user.username} started following you"
                )

        # Update some user profiles with more details
        profile_bios = [
            "Full-stack developer passionate about creating amazing user experiences 💻",
            "Designer who loves clean interfaces and beautiful typography ✨",
            "Coffee enthusiast and code lover ☕ Always learning something new!",
            "Tech entrepreneur building the future 🚀 #innovation #startup",
            "Creative developer with a passion for #webdesign and #ux",
            "Open source contributor | Python enthusiast | Always curious 🐍",
            "Digital nomad exploring the world while coding 🌍 #remotework",
            "AI researcher fascinated by machine learning and data science 🤖",
            "Frontend developer who believes in pixel-perfect designs 🎨",
            "Backend engineer scaling systems and solving complex problems ⚡"
        ]

        locations = [
            "San Francisco, CA", "New York, NY", "London, UK", "Berlin, Germany",
            "Tokyo, Japan", "Sydney, Australia", "Toronto, Canada", "Amsterdam, Netherlands",
            "Barcelona, Spain", "Singapore", "Remote", "Seattle, WA"
        ]

        websites = [
            "https://github.com/developer", "https://portfolio.dev", "https://myblog.com",
            "https://linkedin.com/in/profile", "https://twitter.com/handle", "https://medium.com/@writer"
        ]

        for i, user in enumerate(users[:10]):
            profile = user.profile
            profile.bio = random.choice(profile_bios)
            profile.location = random.choice(locations)
            if random.random() < 0.4:  # 40% have websites
                profile.website = random.choice(websites)
            if random.random() < 0.2:  # 20% are verified
                profile.is_verified = True
            profile.save()

        # Summary
        total_posts = Post.objects.count()
        total_comments = Comment.objects.count()
        total_likes = Like.objects.count()
        total_notifications = Notification.objects.count()
        total_hashtags = len(set(Post.objects.values_list('hashtags__name', flat=True)))

        self.stdout.write(self.style.SUCCESS('Enhanced mock data created successfully!'))
        self.stdout.write(f'📊 Summary:')
        self.stdout.write(f'👥 Users: {User.objects.count()}')
        self.stdout.write(f'📝 Posts: {total_posts}')
        self.stdout.write(f'💬 Comments: {total_comments}')
        self.stdout.write(f'❤️  Likes: {total_likes}')
        self.stdout.write(f'🔔 Notifications: {total_notifications}')
        self.stdout.write(f'#️⃣  Hashtags: {total_hashtags}')
        self.stdout.write('\n🎉 Your social platform is now full of engaging content!')
        self.stdout.write('Visit http://127.0.0.1:8000 to explore!')