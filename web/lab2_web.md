curl -X 'GET' \
  'http://127.0.0.1:8000/tokens/?skip=0&limit=10' \
  -H 'accept: application/json'

http://127.0.0.1:8000/tokens/?skip=0&limit=10

[
  {
    "symbol": "ETH",
    "blockchain_id": 1,
    "id": 1
  },
  {
    "symbol": "UNI",
    "blockchain_id": 1,
    "id": 2
  },
  {
    "symbol": "SOL",
    "blockchain_id": 2,
    "id": 3
  }
]

 content-length: 127 
 content-type: application/json 
 date: Thu,26 Feb 2026 16:41:53 GMT 
 server: uvicorn 

 [
  {
    "symbol": "string",
    "blockchain_id": 0,
    "id": 0
  }
]

{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string",
      "input": "string",
      "ctx": {}
    }
  ]
}