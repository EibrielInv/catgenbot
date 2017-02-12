# catgenbot
Telegram bot for David Revoy's Cat Avatar generator

## Deploying Telegram Bot
Ubuntu 16.04 with Flask and Nginx

```
mkdir /var/www/catgenbot/
cd /var/www/catgenbot/
git clone https://github.com/Eibriel/catgenbot.git
apt-get install virtualenv
virtualenv -p python3 venv

. venv/bin/activate
pip install gunicorn flask
pip install -r requirements.txt

cd /var/www/catgenbot/catgenbot/
gunicorn --bind 0.0.0.0:5000 catgenbot:app
deactivate
```

Create Nginx site
```
vim /etc/nginx/sites-available/catgenbot-bot.conf
```

Create certificate

```
letsencrypt certonly --rsa-key-size 4096 --webroot -w /var/www/catgenbot/catgenbot/ -d address.to.bot
```

With the following content:

```
server {
    listen              443 ssl http2;
    listen              [::]:443 ssl http2;

    server_name         address.to.bot;

    ssl_certificate     /etc/letsencrypt/live/address.to.bot/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/address.to.bot/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    # modern configuration. tweak to your needs.
    ssl_protocols TLSv1.2;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256';
    ssl_prefer_server_ciphers on;

    # HSTS (ngx_http_headers_module is required) (15768000 seconds = 6 months)
    add_header Strict-Transport-Security max-age=15768000;

    # OCSP Stapling ---
    # fetch OCSP records from URL in ssl_certificate and cache them
    ssl_stapling on;
    ssl_stapling_verify on;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/catgenbot/catgenbot/catgenbot.sock;
    }
}
```

Enable Nginx site
```
sudo ln -s /etc/nginx/sites-available/catgenbot-bot.conf /etc/nginx/sites-enabled
```

On the file `/etc/systemd/system/catgenbot.service` enter the following info:
```
[Unit]
Description=Gunicorn instance to serve ourbot
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/catgenbot/catgenbot
Environment="PATH=/var/www/catgenbot/venv/bin"
ExecStart=/var/www/ourbot/venv/bin/gunicorn --workers 40 --bind unix:catgenbot.sock -m 007 catgenbot:app

[Install]
WantedBy=multi-user.target
```

Start and enable
```
systemctl start catgenbot
systemctl enable catgenbot
```

Reload and restart

```
systemctl daemon-reload
systemctl restart catgenbot
```

Tell Telegram Bot API to use our WebHook

`curl -F "url=https://address.to.bot" https://api.telegram.org/botTOKEN/setWebhook`
