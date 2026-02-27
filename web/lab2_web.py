from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel
import uvicorn
from typing import List, Optional

app = FastAPI(title="Token Analysis API", description="REST API для аналізу токенів та блокчейнів")

# ==========================================
# 1. СУТНОСТІ (Pydantic Моделі для валідації)
# ==========================================

class Blockchain(BaseModel):
    id: int
    name: str

class TokenCreate(BaseModel):
    symbol: str
    blockchain_id: int

class Token(TokenCreate):
    id: int

class LaunchMetric(BaseModel):
    id: int
    roi: float
    community_allocation: float
    token_id: int

# ==========================================
# Імітація Бази Даних (in-memory)
# ==========================================
blockchains_db = [
    {"id": 1, "name": "Ethereum"},
    {"id": 2, "name": "Solana"}
]

tokens_db = [
    {"id": 1, "symbol": "ETH", "blockchain_id": 1},
    {"id": 2, "symbol": "UNI", "blockchain_id": 1},
    {"id": 3, "symbol": "SOL", "blockchain_id": 2}
]

metrics_db = [
    {"id": 1, "roi": 150.5, "community_allocation": 15.0, "token_id": 1},
    {"id": 2, "roi": 300.0, "community_allocation": 5.0, "token_id": 2}
]

# ==========================================
# 2. CRUD ОПЕРАЦІЇ ДЛЯ СУТНОСТІ "TOKEN"
# ==========================================

# CREATE (POST) - Створення нового токена
@app.post("/tokens/", response_model=Token, status_code=status.HTTP_201_CREATED)
def create_token(token: TokenCreate):
    new_id = max([t["id"] for t in tokens_db]) + 1 if tokens_db else 1
    new_token = {"id": new_id, **token.dict()}
    tokens_db.append(new_token)
    return new_token

# READ (GET) - Отримання списку токенів з пагінацією, сортуванням та фільтрацією
@app.get("/tokens/", response_model=List[Token], status_code=status.HTTP_200_OK)
def get_tokens(
    skip: int = Query(0, description="Пропустити вказану кількість записів (Пагінація)"),
    limit: int = Query(10, description="Максимальна кількість записів (Пагінація)"),
    sort_by: Optional[str] = Query(None, description="Поле для сортування (наприклад: symbol)"),
    symbol_filter: Optional[str] = Query(None, description="Фільтр за символом токена")
):
    result = tokens_db

    # 1. Фільтрація (Filtering)
    if symbol_filter:
        result = [t for t in result if symbol_filter.lower() in t["symbol"].lower()]

    # 2. Сортування (Sorting)
    if sort_by and result and sort_by in result[0].keys():
        result = sorted(result, key=lambda x: x[sort_by])

    # 3. Пагінація (Pagination)
    return result[skip : skip + limit]

# READ (GET) - Отримання одного токена за ID з вкладеними даними
@app.get("/tokens/{token_id}", status_code=status.HTTP_200_OK)
def get_token(token_id: int):
    token = next((t for t in tokens_db if t["id"] == token_id), None)
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Токен не знайдено")
    
    # Додавання вкладених зв'язків (Nested Relations)
    token_metrics = [m for m in metrics_db if m["token_id"] == token_id]
    return {"token": token, "metrics": token_metrics}

# UPDATE (PUT) - Оновлення даних існуючого токена
@app.put("/tokens/{token_id}", response_model=Token, status_code=status.HTTP_200_OK)
def update_token(token_id: int, updated_token: TokenCreate):
    for i, token in enumerate(tokens_db):
        if token["id"] == token_id:
            tokens_db[i] = {"id": token_id, **updated_token.dict()}
            return tokens_db[i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Токен не знайдено")

# DELETE (DELETE) - Видалення токена
@app.delete("/tokens/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_token(token_id: int):
    global tokens_db
    token_exists = any(t["id"] == token_id for t in tokens_db)
    if not token_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Токен не знайдено")
    
    tokens_db = [t for t in tokens_db if t["id"] != token_id]
    return # 204 No Content не повертає тіло відповіді
if __name__ == "__main__":
    uvicorn.run("lab2_web:app", host="127.0.0.1", port=8000, reload=True)