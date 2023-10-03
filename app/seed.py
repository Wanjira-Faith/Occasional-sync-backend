from app import app
import random
from models import db, Event, User, EventNotification
from faker import Faker

fake = Faker()


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

    # Function to create random events with organizers and attendees
    def create_events_with_organizers_and_attendees(num_events, num_organizers, num_attendees):
        events = []
        for _ in range(num_events):
            organizer = random.choice(User.query.all())
            event = Event(
                organizer_id=organizer.user_id,
                poster=fake.image_url(),
                name=fake.catch_phrase(),
                date=fake.date_time_this_decade(),
                location=fake.city(),
                description=fake.paragraph(),
                capacity=fake.random_int(min=10, max=200),
            )
            db.session.add(event)

            # Add attendees to the event
            attendees = random.sample(User.query.all(), num_attendees)
            event.attendees.extend(attendees)

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
                message=fake.sentence(),
            )
            db.session.add(notification)
            notifications.append(notification)
        db.session.commit()
        return notifications

    if __name__ == '__main__':
        num_users = 10
        num_events = 20
        num_organizers = 5
        num_attendees = 10
        num_notifications = 30

        # Create users
        create_users(num_users)

        # Create events with organizers and attendees
        events = create_events_with_organizers_and_attendees(num_events, num_organizers, num_attendees)

        # Create event notifications
        create_event_notifications(num_notifications, events)

        print("Seed data generated successfully.")