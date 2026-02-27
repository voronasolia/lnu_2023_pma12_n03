import sys
import os
import pytest
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.testclient import TestClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = FastAPI()

class UserLogin(BaseModel):
    username: str
    password: str

USERS = {"admin": "secret123"}
DATA = {"admin": "Важливі дані користувача"}

@app.post("/api/login")
def login(user: UserLogin):
    if USERS.get(user.username) == user.password:
        return {"token": f"token_for_{user.username}"}
    raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/api/data/{token}")
def get_data(token: str):
    if token == "token_for_admin":
        return {"data": DATA["admin"]}
    raise HTTPException(status_code=403, detail="Forbidden")

client = TestClient(app)

def test_login_success():
    response = client.post("/api/login", json={"username": "admin", "password": "secret123"})
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_failure():
    response = client.post("/api/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401

def test_full_user_flow():
    login_response = client.post("/api/login", json={"username": "admin", "password": "secret123"})
    assert login_response.status_code == 200
    token = login_response.json()["token"]
    
    data_response = client.get(f"/api/data/{token}")
    assert data_response.status_code == 200
    assert data_response.json()["data"] == "Важливі дані користувача"

def run_scraper():
    print("Запуск браузера...")
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get("http://quotes.toscrape.com/login")
        driver.find_element(By.ID, "username").send_keys("test_user")
        driver.find_element(By.ID, "password").send_keys("test_password")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "quote"))
        )

        quotes = driver.find_elements(By.CLASS_NAME, "text")[:3]
        authors = driver.find_elements(By.CLASS_NAME, "author")[:3]

        print("\n--- Результати скрапінгу ---")
        for q, a in zip(quotes, authors):
            print(f"Цитата: {q.text}\nАвтор: {a.text}\n")
    finally:
        driver.quit()
        print("Браузер закрито.")

if __name__ == "__main__":
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    module_name = os.path.splitext(os.path.basename(current_file_path))[0]
    
    os.chdir(current_dir)

    print("\nВиберіть, що ви хочете запустити:")
    print("1 - Запустити API сервер (FastAPI)")
    print("2 - Виконати Unit/Integration тести та звіт про покриття (>30%)")
    print("3 - Запустити Performance тести (Locust)")
    print("4 - Виконати Selenium скрапінг")
    print("0 - Вийти")
    
    choice = input("\nВаш вибір: ")

    if choice == "1":
        print("Запуск сервера на http://127.0.0.1:8000 ...")
        uvicorn.run(app, host="127.0.0.1", port=8000)
        
    elif choice == "2":
        print("Запуск тестів та генерація звіту про покриття...")
        pytest.main(["-v", current_file_path, f"--cov={module_name}", "--cov-report=term-missing"])
        
    elif choice == "3":
        print("Запуск Locust... Перейдіть за адресою http://localhost:8089 у браузері.")
        print("У полі 'Host' вкажіть: http://127.0.0.1:8000 (Сервер має бути запущений паралельно!)")
        os.system(f'"{sys.executable}" -m locust -f locustfile.py')
        
    elif choice == "4":
        run_scraper()
        
    elif choice == "0":
        sys.exit()
        
    else:
        print("Невірний вибір!")