
.PHONY: migrate run swag md2html

migrate:
	go run ./cmd/migrate

run: swag
	go run .

swag:
	swag init

md2html:
	#go run ./cmd/md2html_test
	cd ./cmd/md2html_test && go run .

