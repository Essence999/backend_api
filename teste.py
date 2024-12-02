import httpx

with httpx.Client(verify=False) as c:
    response = c.get('https://shura.bb.com.br:8000/versoes')

print(response.headers)
