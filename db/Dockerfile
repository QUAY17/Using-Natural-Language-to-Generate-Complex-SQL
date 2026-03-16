FROM mysql

CMD ["--max-allowed-packet=1024M", "--max_connections=10000"]

# Pass credentials at runtime: docker run -e MYSQL_ROOT_PASSWORD=... -e MYSQL_USER=... -e MYSQL_PASSWORD=... -e MYSQL_DATABASE=...