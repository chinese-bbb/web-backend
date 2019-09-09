# Mysql operation notes

### flask migration usage

Schema change should be made through flask migrations. To evolve dev mysql schema:

0. use the correct `DATABASE_URL` environment variable
1. change Models which manages the source of truth schema, e.g, app/models.py
2. `flask db migrate -m "add flask_user required field" -d migration-dev`
3. `flask db upgrade -d migration-dev`
