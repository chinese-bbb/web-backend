# App Debug Notes

## Steps to Verify API

1. Login

```sh
curl -b cookies.txt -c cookies.txt -H "Content-Type: application/json" -X POST 'http://localhost:5000/api/auth/login' -d '{"phone_num":"az", "password":"az"}'
```

2. Whether a phone number exists

```sh
curl -H "Content-Type: application/json" -X GET 'http://localhost:5000/api/phone_exist/17782583329'
```

3. Register

```sh
curl -H "Content-Type: application/json" -X POST 'http://localhost:5000/api/register' -d '{"phone_num": "133", "password":"133", "sex":"female"}'
```

4. fuzzy Qichacha query

```sh
curl -b cookies.txt -c cookies.txt -H "Content-Type: application/json" -X POST 'http://localhost:5000/api/fuzzy_query' -d '{"keyword": "baidu"}'
```
