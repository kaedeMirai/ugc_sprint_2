from locust import HttpUser, task, between


class UserBehavior(HttpUser):
    wait_time = between(1, 5)
    host = "http://0.0.0.0:8282"

    @task
    def get_film_reviews(self):
        film_id = "fff15fb7-c9d5-4ec6-89ef-46d9b60b3af9"
        self.client.get(
            f"/api/v1/activities/get_film_reviews?film_id={film_id}"
            f"&offset=0&limit=10000&sort_keys=user_id&sort_order=1"
        )

    @task(2)
    def post_activity(self):
        activity_payload = {
            "user_id": "75f18eaf-08d0-418a-bb0a-4e03c53e103c",
            "activity_type": "like",
            "created_date": "2024-01-21T11:22:40.851018",
            "entity_id": "fff15fb7-c9d5-4ec6-89ef-46d9b60b3af9",
            "mark": 10
        }

        self.client.post(url="/api/v1/activities/add_activity", json=activity_payload)
