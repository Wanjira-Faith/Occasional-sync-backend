# EvenTick Project(backend readme}

EventHub Seed Data Generation
EventHub Seed Data Generation is a Python script that populates your EventHub application with sample data. This script is designed to create random users, events, and event notifications to help you test and showcase your event management application.

## Getting Started
Usage
Customization
Contributing
License
Introduction
EventHub Seed Data Generation is a Python script that can be used to generate seed data for your EventHub application. It creates random users, events with organizers, and event notifications, providing you with a starting point for testing and demonstrating your application.

## Prerequisites
Before using the script, ensure you have the following dependencies installed:

Python 3
Flask
SQLAlchemy
Faker
You should also have your EventHub application set up and configured correctly.

## Getting Started
Clone or download this repository to your local machine.

bash
Copy code
git clone https://github.com/your-username/eventhub-seed-data.git
Navigate to the project directory.

bash
Copy code
cd eventhub-seed-data
Install the required Python packages.

bash
Copy code
pip install -r requirements.txt
Open the app.py file in your preferred code editor.

Update the event_data list with your own event data. Each entry in the list should include event name, description, image URL, and notification message.

Run the script.

bash
Copy code
python app.py
The script will create random users, events, and event notifications based on the provided data.

Usage
The script is designed to generate seed data for your EventHub application. It performs the following actions:

Create Random Users: You can specify the number of random users to generate. These users will be added to your database and can be used for testing and demonstration.

Create Events with Organizers: The script randomly assigns organizers (users) to events, using the event data you provided. Events include details such as name, date, location, description, capacity, and an image URL.

Create Event Notifications: Event notifications are associated with specific events and include a notification message. The script randomly assigns notifications to events.

The generated data will be inserted into your database, helping you showcase your application's functionality.

## Customization
You can customize the script by updating the event_data list with your own event data. Each entry in the list should follow this structure:

python
Copy code
{
    'name': 'Event Name',
    'description': 'Event Description',
    'image_url': 'Event Image URL',
    'notification_message': 'Event Notification Message',
}
Feel free to modify the script to suit your specific needs or to generate more or less data.

# Group Members
1. Faith Wanjira
2. Letia Kiok
4. Mark Kimani
