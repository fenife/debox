
REGISTRY_HOST = stg-registry.me:8810

REGISTRY_PORT = 8810
REGISTRY_UI_PORT = 8820

docker run -d -p 5000:5000 --restart=always --name registry \
	-v /wine/var/registry:/var/lib/registry \
	registry:2
