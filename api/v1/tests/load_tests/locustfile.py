from locust import HttpUser, task, between, tag


class SpaceMissionUser(HttpUser):
    wait_time = between(1, 3)

    @tag("health")
    @task(3)
    def health_endpoint(self):
        self.client.get("/health")

    @tag("detailed")
    @task(1)
    def health_detailed_endpoint(self):
        self.client.get("/health/detailed")
