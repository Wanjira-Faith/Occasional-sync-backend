import random
from models import db, Event, User, EventNotification
from faker import Faker
from app import app

fake = Faker()

# Sample event data
event_data = [
    {
        'name': 'Summer Music Festival',
        'description': 'Join us for a weekend of live music, great food, and fun activities at our annual Summer Music Festival.',
        'image_url': 'https://i.pinimg.com/564x/85/4b/55/854b5584101a5d50c1006e63d1ddd500.jpg',
        'notification_message': "Join us for a weekend of live music and fun activities",
    },
    {
        'name': 'Tech Meetup 2023',
        'description': 'Tech enthusiasts, unite! The biggest tech meetup of 2023 is here. Dive into the world of innovation and networking.',
        'image_url': 'https://i.pinimg.com/564x/cd/a6/4b/cda64b3a45b1613ab78aeb057315b207.jpg',
        'notification_message': "Don't miss out on our exciting tech meetup next week!",
    },
    {
        'name': 'Charity Gala Dinner',
        'description': 'Support a good cause while enjoying a glamorous evening. Join us for the Charity Gala Dinner benefiting local charities.',
        'image_url': 'https://i.pinimg.com/564x/ff/2e/cf/ff2ecf5a3d7ccd9cae851ec27e463a62.jpg',
        'notification_message': "Join us for the annual charity gala dinner to make a difference.",
    },
    {
        'name': 'Art Exhibition: Beyond Colors',
        'description': 'Explore the world of art and creativity. Our art exhibition showcases breathtaking works that go "Beyond Colors."',
        'image_url': 'https://i.pinimg.com/564x/47/9c/d7/479cd712af06017c64e3e6c1a682b74c.jpg',
        'notification_message': "Experience art like never before at our 'Beyond Colors' exhibition.",
    },
    {
        'name': 'Fitness Bootcamp Challenge',
        'description': 'Challenge yourself with a fitness bootcamp like no other. Get fit, have fun, and meet new fitness buddies.',
        'image_url': 'https://i.pinimg.com/564x/8c/53/fe/8c53feb9be638a6fe6a8a7ba7c101f2d.jpg',
        'notification_message': "Get ready to challenge yourself at our fitness bootcamp!",
    },
    {
        'name': 'Local Food Festival',
        'description': 'Indulge in the flavors of your local community. Sample delicious dishes and discover hidden culinary gems.',
        'image_url': 'https://i.pinimg.com/564x/e6/5c/9e/e65c9e7ab4ce22db6cb6ae68d0a208f9.jpg',
        'notification_message': "Indulge in delicious local cuisines at our food festival.",
    },
    {
        'name': 'Movie Night Under the Stars',
        'description': 'Bring your blanket and popcorn for a cozy movie night outdoors. Watch your favorite films under the starry sky.',
        'image_url': 'https://i.pinimg.com/564x/4a/49/2a/4a492ada984e4e9c9b76334faa629ea4.jpg',
        'notification_message': "Join us for a movie night under the stars with your friends and family.",
    },
    {
        'name': 'Business Conference: Innovate Today',
        'description': 'Learn from industry experts and connect with fellow entrepreneurs at our business conference: "Innovate Today."',
        'image_url': 'https://i.pinimg.com/564x/8c/7b/5d/8c7b5d17c27b74ae63fd794afd2e328f.jpg',
        'notification_message': "Innovate today at our business conference. See you there!",
    },
    {
        'name': 'Yoga and Meditation Retreat',
        'description': 'Find your inner peace and recharge your spirit at our yoga and meditation retreat. Relaxation and mindfulness await.',
        'image_url': 'https://i.pinimg.com/564x/5d/77/4c/5d774ccb7f6e877f6c1fe837595fa247.jpg',
        'notification_message': "Relax and rejuvenate at our yoga and meditation retreat.",
    },
    {
        'name': 'Cooking Masterclass with Chef Smith',
        'description': 'Become a culinary master with Chef Smith. Join our cooking masterclass and impress your friends with your skills.',
        'image_url': 'https://i.pinimg.com/564x/e3/fe/5f/e3fe5f657d90b48014b647d592c1db6d.jpg',
        'notification_message': "Learn the art of cooking with Chef Smith in our masterclass.",
    },
]

with app.app_context():
    # Clear existing data
    EventNotification.query.delete()
    Event.query.delete()
    User.query.delete()

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
        for i in range(num_events):
            organizer = random.choice(User.query.all())
            event_data_entry = event_data[i]  # Use the event_data in order
            fake_location = fake.city() + ', ' + fake.country()
            
            event = Event(
                organizer_id=organizer.user_id,
                poster=event_data_entry['image_url'],
                name=event_data_entry['name'],
                date=fake.date_time_this_decade(),
                location=fake_location,
                description=event_data_entry['description'],
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
            event_data_entry = event_data[events.index(event)]  # Match event data to events
            notification = EventNotification(
                event_id=event.event_id,
                message=event_data_entry['notification_message'],
            )
            db.session.add(notification)
            notifications.append(notification)

        db.session.commit()
        return notifications

    if __name__ == '__main__':
        num_users = 10
        num_events = len(event_data)  # Use the number of event data entries
        num_organizers = 5
        num_notifications = 10

        # Create users
        create_users(num_users)

        # Create events with organizers
        events = create_events_with_organizers(num_events, num_organizers)

        # Create event notifications
        create_event_notifications(num_notifications, events)

        print("Seed data generated successfully.")

    