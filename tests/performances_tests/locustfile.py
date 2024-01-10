from locust import HttpUser
from locust import task
from locust import between


class ProjectPerformanceTest(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(1, 2)

    @task
    def load_club_main_page(self):
        self.client.get("/club-points")
