
.PHONY: migrate run swag md2html

migrate:
	go run ./cmd/migrate

swag:
	swag init

run: swag
	go run .
