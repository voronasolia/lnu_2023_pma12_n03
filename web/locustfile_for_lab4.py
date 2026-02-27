from locust import HttpUser, task, between

class APIPerformanceTest(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def simple_endpoint_test(self):
        self.client.post("/api/login", json={"username": "test", "password": "123"})

    @task(2)
    def complex_scenario_test(self):
        login_response = self.client.post("/api/login", json={"username": "admin", "password": "secret123"})
        if login_response.status_code == 200:
            token = login_response.json().get("token")
            with self.client.get(f"/api/data/{token}", catch_response=True) as data_response:
                if data_response.status_code == 200:
                    data_response.success()
                else:
                    data_response.failure(f"Failed. Status: {data_response.status_code}")