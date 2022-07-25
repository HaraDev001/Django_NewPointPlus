# Djangoからopen apiを出力する

python manage.py spectacular \
--file schema_shop.yml \
--settings open_api.settings_shop

python manage.py spectacular \
--file schema_console.yml \
--settings open_api.settings_console

python manage.py spectacular \
--file schema_card.yml \
--settings open_api.settings_card

python manage.py spectacular \
--file schema_terminal.yml \
--settings open_api.settings_terminal
