import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_blog.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Post

# Create a superuser if it doesn't exist
try:
    user = User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("Created admin user")
except:
    user = User.objects.get(username='admin')
    print("Admin user already exists")

# Create categories
categories_data = [
    {'name': 'Machine Learning', 'description': 'Posts about machine learning algorithms and techniques'},
    {'name': 'Deep Learning', 'description': 'Posts about neural networks and deep learning'},
    {'name': 'Natural Language Processing', 'description': 'Posts about NLP and text processing'},
    {'name': 'Computer Vision', 'description': 'Posts about image processing and computer vision'},
    {'name': 'AI Ethics', 'description': 'Posts about ethical considerations in AI'},
]

categories = []
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    categories.append(category)
    if created:
        print(f"Created category: {category.name}")

# Create sample posts
posts_data = [
    {
        'title': 'Introduction to Machine Learning',
        'content': '<p>Machine learning is a subset of artificial intelligence that focuses on algorithms and statistical models...</p>',
        'excerpt': 'An introduction to the fundamental concepts of machine learning.',
        'category': categories[0],
        'author': user,
        'status': 'published'
    },
    {
        'title': 'Understanding Neural Networks',
        'content': '<p>Neural networks are computing systems inspired by the human brain...</p>',
        'excerpt': 'A deep dive into how neural networks work and their applications.',
        'category': categories[1],
        'author': user,
        'status': 'published'
    },
    {
        'title': 'Natural Language Processing Techniques',
        'content': '<p>Natural Language Processing (NLP) combines computational linguistics with machine learning...</p>',
        'excerpt': 'Exploring the latest techniques in natural language processing.',
        'category': categories[2],
        'author': user,
        'status': 'published'
    },
    {
        'title': 'Computer Vision Applications',
        'content': '<p>Computer vision enables machines to identify and process visual information...</p>',
        'excerpt': 'Real-world applications of computer vision technology.',
        'category': categories[3],
        'author': user,
        'status': 'published'
    },
    {
        'title': 'Ethical Considerations in AI',
        'content': '<p>As AI becomes more prevalent, ethical considerations become increasingly important...</p>',
        'excerpt': 'Examining the ethical challenges and responsibilities in AI development.',
        'category': categories[4],
        'author': user,
        'status': 'published'
    },
]

for post_data in posts_data:
    post, created = Post.objects.get_or_create(
        title=post_data['title'],
        defaults={
            'content': post_data['content'],
            'excerpt': post_data['excerpt'],
            'category': post_data['category'],
            'author': post_data['author'],
            'status': post_data['status']
        }
    )
    if created:
        print(f"Created post: {post.title}")

print("Data population completed!")
