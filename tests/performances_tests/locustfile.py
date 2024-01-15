from locust import HttpUser
from locust import task
from locust import between
from locust import TaskSet


class ClubUserBehavior(TaskSet):
    @task
    def view_table_club_points(self):
        self.client.get("/club-points")

    @task
    def load_main_page(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/show-summary", {"email": "contact@highflyers.com"})

    @task
    def book_competition(self):
        self.client.get("/book/Test Championship/High Flyers")

    @task
    def purchase_places(self):
        self.client.post("/purchase-places", {
            "competition": "Test Championship",
            "club": "High Flyers",
            "places": "1"
        })

    @task
    def logout(self):
        self.client.get("/logout")


# Defines the behavior for a website user
class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:5000"  # The host URL where the Flask application is running
    tasks = [ClubUserBehavior]  # Assigning the defined user behavior
    wait_time = between(1, 5)   # Setting a random wait time between tasks
