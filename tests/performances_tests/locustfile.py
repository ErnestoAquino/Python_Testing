from locust import HttpUser
from locust import task
from locust import between
from locust import TaskSet

from random import choice


class ClubUserBehavior(TaskSet):
    # List of competition names for random selection
    competition_names = [
        "Test Championship",
        "Summer Sprint",
        "Autumn Open",
        "Winter Games",
        "Spring Challenge"
    ]

    # List of club names for random selection
    club_names = [
        "High Flyers",
        "Sky Divers",
        "Mountain Climbers",
        "Sea Surfers",
        "Desert Runners"
    ]

    # List of club emails for random selection
    club_emails = [
        "contact@highflyers.com",
        "info@skydivers.com",
        "support@mountainclimbers.com",
        "contact@seasurfers.com",
        "hello@desertrunners.com"
    ]

    @task
    def view_table_club_points(self):
        # View the club points table
        self.client.get("/club-points")

    @task
    def load_main_page(self):
        # Load the main page of the website
        self.client.get("/")

    @task
    def show_summary(self):
        # Show summary for a randomly selected club email
        selected_email_club = choice(self.club_emails)
        self.client.post("/show-summary", {"email": selected_email_club})

    @task
    def book_competition(self):
        # Task to book a competition for a randomly selected club
        selected_club = choice(self.club_names)
        selected_competition = choice(self.competition_names)
        self.client.get(f"/book/{selected_competition}/{selected_club}")

    @task
    def purchase_places(self):
        # Task to randomly purchase places for a selected competition and club
        selected_club = choice(self.club_names)
        selected_competition = choice(self.competition_names)
        places_to_book = choice(range(1, 5))
        self.client.post("/purchase-places", {
            "competition": selected_competition,
            "club": selected_club,
            "places": str(places_to_book)
        })

    @task
    def logout(self):
        # Task to simulate user logout
        self.client.get("/logout")


# Defines the behavior for a website user
class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:5000"  # The host URL where the Flask application is running
    tasks = [ClubUserBehavior]  # Assigning the defined user behavior
    wait_time = between(1, 5)   # Setting a random wait time between tasks
