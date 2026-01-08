import random
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from social_app.models import Post, Comment, Profile, Hashtag
from django.core.files import File

class Command(BaseCommand):
    help = 'Populates the database with diverse Indian mock data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating diverse Indian mock data...')

        # Diverse Indian usernames
        usernames = [
            'Arjun_Sharma', 'Priya_Nair', 'Karthik_Rajan', 'Ananya_Verma', 'Siddharth_Mathur',
            'Deepika_Reddy', 'Rahul_Gupta', 'Sneha_Iyer', 'Vikram_Singh', 'Meera_Deshmukh',
            'Aditya_Patel', 'Ishani_Chaudhary', 'Rohan_Malhotra', 'Kavya_Krishnan', 'Manish_Tiwari',
            'Sanjana_Rao', 'Aakash_Mehta', 'Tanvi_Joshi', 'Yash_Vardhan', 'Divya_Bharathi'
        ]
        
        # Indian-themed bios
        bios = [
            "Foodie | Photography | Proud Indian 🇮🇳",
            "Software Engineer by day, Carnatic music lover by night.",
            "Exploring the beauty of Tamil Nadu and beyond. 🏯",
            "Lover of North Indian delicacies and spiritual journeys. ✨",
            "Tech enthusiast & Dosa connoisseur. Living in the moment.",
            "Delhi girl in Bangalore. Missing Sarojini Market but loving the weather!",
            "Aspiring filmmaker interested in South Indian cinema. 🎬",
            "Wanderlust soul exploring the Ghats and the Himalayas. 🏔️",
            "Yoga, Chai, and Code. ☕",
            "Passionate about Indian history and architecture."
        ]

        # Images we copied earlier
        image_mapping = {
            'South Indian Food': 'media/posts/south_indian_food.png',
            'North Indian Cuisine': 'media/posts/north_indian_food.png',
            'Tamil Nadu Heritage': 'media/posts/tamil_nadu.png',
            'Festival of Colors': 'media/posts/holi_celebration.png'
        }

        # Create Users
        users = []
        for i, name in enumerate(usernames):
            username = f"{name}_{random.randint(10, 99)}"
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password='password123')
                # Update Profile
                user.profile.bio = random.choice(bios)
                user.profile.location = random.choice(['Chennai', 'Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Kochi'])
                user.profile.is_verified = random.choice([True, False, False, False])
                user.profile.save()
                users.append(user)
                self.stdout.write(f'Created user: {username}')

        if not users:
            self.stdout.write('No new users created. Using existing users.')
            users = list(User.objects.all())

        # Create Follows
        for user in users:
            potentials = [u for u in users if u != user]
            if potentials:
                to_follow = random.sample(potentials, k=min(len(potentials), random.randint(3, 8)))
                for target in to_follow:
                    user.profile.follows.add(target.profile)

        # Indian Themed Posts
        indian_posts = [
            {"content": "Just had the most amazing Dosa at a local joint in Chennai! The chutneys were fire. 🔥 #SouthIndianFood #TamilNadu #Foodie", "image_key": "South Indian Food"},
            {"content": "Missing the winter vibes of Delhi and the smell of fresh Butter Chicken. 🥘 #NorthIndianFood #DelhiVibes #MissingHome", "image_key": "North Indian Cuisine"},
            {"content": "The intricate carvings at the temples here are mind-blowing. Our heritage is so rich! 🏯 #TamilNadu #IncredibleIndia #Heritage", "image_key": "Tamil Nadu Heritage"},
            {"content": "Happy Holi everyone! Celebrated with colors, sweets, and tons of laughter today. 🌈✨ #Holi2026 #FestivalOfColors #MixedIndia", "image_key": "Festival of Colors"},
            {"content": "Nothing beats a cup of Filter Kaapi on a rainy Bangalore afternoon. ☕🌧️ #BangaloreDiaries #FilterCoffee #SouthIndia"},
            {"content": "Weekend trip to Mahabalipuram was absolutely surreal. The shore temple is a must-visit! #TravelIndia #TamilNaduTourism"},
            {"content": "Trying hands at making Paneer Tikka tonight. Wish me luck! 👨‍🍳 #HomeCooking #DesiFood #Vegetarian"},
            {"content": "Yoga session at sunrise followed by some meditation. Peace is power. 🧘‍♂️✨ #YogaLife #SpiritualIndia #HealthyLiving"},
            {"content": "The diversity of India never ceases to amaze me. From the snow-capped mountains of North to the backwaters of South. 🇮🇳❤️ #UnityInDiversity #ProudIndian"},
            {"content": "Watching the sunset at Marina Beach. There's something magical about this place. 🌅 #Chennai #MarinaBeach #EveningWalk"}
        ]

        for item in indian_posts:
            user = random.choice(users)
            post = Post.objects.create(user=user, content=item['content'])
            
            # Add image if applicable
            image_key = item.get('image_key')
            if image_key and image_key in image_mapping:
                image_path = image_mapping[image_key]
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        post.image.save(os.path.basename(image_path), File(f), save=True)
            
            self.stdout.write(f'Created post by {user.username}')

            # Add Likes & Comments
            potentials = [u for u in users if u != user]
            if potentials:
                likers = random.sample(potentials, k=random.randint(1, len(potentials)//2))
                for liker in likers:
                    post.likes.create(user=liker)

                commenters = random.sample(potentials, k=random.randint(1, 4))
                comments_text = [
                    "Looks delicious!", "Wow, beautiful view.", "Totally missing this!",
                    "Proud of our culture. 🇮🇳", "Absolutely stunning!", "Save some for me!",
                    "Great shot!", "Incredible India indeed.", "Happy holidays!", "Stay blessed!"
                ]
                for commenter in commenters:
                    Comment.objects.create(post=post, user=commenter, text=random.choice(comments_text))

        self.stdout.write(self.style.SUCCESS('Successfully populated database with diverse Indian data!'))

