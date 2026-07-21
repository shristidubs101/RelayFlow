from app.services.signing import generate_signature

payload = {"role":"editor","email":"alex.morgan@example.com","profile":{"last_name":"Morgan","time_zone":"America/New_York","first_name":"Alex"},"user_id":"usr_9923841a","created_at":"2026-07-21T18:25:00Z"}

secret = "honey"

signature = generate_signature(payload, secret)

print(signature)