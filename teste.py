import requests

#Necessário atualizar refresh token
header = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY2MTQ5NjE2fQ.aFIeGWtdG9KsZeUCtDR9wXTaiqBWF4mjgDu8pR5xLq8"}

req = requests.get("http://127.0.0.1:8000/auth/refresh",headers=header)
print(req)
print(req.json())