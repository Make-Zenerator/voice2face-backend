sudo docker-compose run --rm --entrypoint "\
    certbot certonly \
    -d "makezenerator.site" \
    -d "*.makezenerator.site" \
    --email mz240103@gmail.com \
    --manual --preferred-challenges dns \
    --server https://acme-v02.api.letsencrypt.org/directory \
    --force-renewal" certbot
echo

echo "### Reloading nginx ..."
sudo docker-compose exec nginx nginx -s reload