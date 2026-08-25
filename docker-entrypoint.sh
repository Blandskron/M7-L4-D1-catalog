#!/bin/sh
set -eu

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ['DJANGO_SUPERUSER_USERNAME']
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=os.environ['DJANGO_SUPERUSER_PASSWORD'])
    print('Superusuario creado.')
else:
    print('El superusuario ya existe.')
"
else
    echo "Superusuario no creado: defina DJANGO_SUPERUSER_USERNAME y DJANGO_SUPERUSER_PASSWORD."
fi

exec "$@"
