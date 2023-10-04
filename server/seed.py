import random
from models import db, Event, User, EventNotification
from faker import Faker
from app import app

fake = Faker()

# Sample data for event names
event_names = [
    'Summer Music Festival',
    'Tech Meetup 2023',
    'Charity Gala Dinner',
    'Art Exhibition: Beyond Colors',
    'Fitness Bootcamp Challenge',
    'Local Food Festival',
    'Movie Night Under the Stars',
    'Business Conference: Innovate Today',
    'Yoga and Meditation Retreat',
    'Cooking Masterclass with Chef Smith',
]

# Sample data for event descriptions
event_descriptions = [
    'Join us for a weekend of live music, great food, and fun activities at our annual Summer Music Festival.',
    'Tech enthusiasts, unite! The biggest tech meetup of 2023 is here. Dive into the world of innovation and networking.',
    'Support a good cause while enjoying a glamorous evening. Join us for the Charity Gala Dinner benefiting local charities.',
    'Explore the world of art and creativity. Our art exhibition showcases breathtaking works that go "Beyond Colors."',
    'Challenge yourself with a fitness bootcamp like no other. Get fit, have fun, and meet new fitness buddies.',
    'Indulge in the flavors of your local community. Sample delicious dishes and discover hidden culinary gems.',
    'Bring your blanket and popcorn for a cozy movie night outdoors. Watch your favorite films under the starry sky.',
    'Learn from industry experts and connect with fellow entrepreneurs at our business conference: "Innovate Today."',
    'Find your inner peace and recharge your spirit at our yoga and meditation retreat. Relaxation and mindfulness await.',
    'Become a culinary master with Chef Smith. Join our cooking masterclass and impress your friends with your skills.',
]

# Sample data for event image URLs
event_image_urls = [
    'https://i.pinimg.com/564x/85/4b/55/854b5584101a5d50c1006e63d1ddd500.jpg',
    'https://i.pinimg.com/564x/cd/a6/4b/cda64b3a45b1613ab78aeb057315b207.jpg',
    'https://i.pinimg.com/564x/ff/2e/cf/ff2ecf5a3d7ccd9cae851ec27e463a62.jpg',
    'https://i.pinimg.com/564x/47/9c/d7/479cd712af06017c64e3e6c1a682b74c.jpg',
    'https://i.pinimg.com/564x/8c/53/fe/8c53feb9be638a6fe6a8a7ba7c101f2d.jpg',
    'https://i.pinimg.com/564x/e6/5c/9e/e65c9e7ab4ce22db6cb6ae68d0a208f9.jpg',
    'https://i.pinimg.com/564x/4a/49/2a/4a492ada984e4e9c9b76334faa629ea4.jpg',
    'https://i.pinimg.com/564x/8c/7b/5d/8c7b5d17c27b74ae63fd794afd2e328f.jpg',
    'https://i.pinimg.com/564x/5d/77/4c/5d774ccb7f6e877f6c1fe837595fa247.jpg',
    'https://i.pinimg.com/564x/e3/fe/5f/e3fe5f657d90b48014b647d592c1db6d.jpg',
]

# Sample data for event notification messages
event_notification_messages = [
    "Don't miss out on our exciting tech meetup next week!",
    "Join us for the annual charity gala dinner to make a difference.",
    "Experience art like never before at our 'Beyond Colors' exhibition.",
    "Get ready to challenge yourself at our fitness bootcamp!",
    "Indulge in delicious local cuisines at our food festival.",
    "Join us for a movie night under the stars with your friends and family.",
    "Innovate today at our business conference. See you there!",
    "Relax and rejuvenate at our yoga and meditation retreat.",
    "Learn the art of cooking with Chef Smith in our masterclass.",
]

with app.app_context():

    # Clear existing data
    Event.query.delete()
    User.query.delete()
    EventNotification.query.delete()

    # Function to create random users
    def create_users(num_users):
        users = []
        for _ in range(num_users):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
            )
            users.append(user)
            db.session.add(user)
        db.session.commit()
        return users

    # Function to create random events with organizers
    def create_events_with_organizers(num_events, num_organizers):
        events = []
        for _ in range(num_events):
            organizer = random.choice(User.query.all())
            event = Event(
                organizer_id=organizer.user_id,
                poster=random.choice(event_image_urls),
                name=random.choice(event_names),
                date=fake.date_time_this_decade(),
                location=fake.city(),
                description=random.choice(event_descriptions),
                capacity=fake.random_int(min=10, max=200),
            )
            db.session.add(event)
            events.append(event)

        db.session.commit()
        return events

    # Function to create random event notifications
    def create_event_notifications(num_notifications, events):
        notifications = []
        for _ in range(num_notifications):
            event = random.choice(events)
            notification = EventNotification(
                event_id=event.event_id,
                message=random.choice(event_notification_messages),
            )
            db.session.add(notification)
            notifications.append(notification)

        db.session.commit()
        return notifications

    if __name__ == '__main__':
        num_users = 10
        num_events = 10
        num_organizers = 5
        num_notifications = 10

        # Create users
        create_users(num_users)

        # Create events with organizers
        events = create_events_with_organizers(num_events, num_organizers)

        # Create event notifications
        create_event_notifications(num_notifications, events)

        print("Seed data generated successfully.")