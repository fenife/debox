
## docker
打开 /etc/docker/daemon.json，添加：
```bash
{
    "insecure-registries": [
        "register.dev.local:5000"
    ]
}
```
重启docker：
```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## register
打开 /etc/hosts ，添加：
127.0.0.1 register.dev.local




## kubectl
curl -LO "https://dl.k8s.io/release/v1.27.0/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/release/v1.25.8/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo cp kubectl /usr/local/bin
mv kubectl kubectl-v1.25.8

## kind

curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.19.0/kind-linux-amd64
chmod +x ./kind
sudo cp ./kind /usr/local/bin/kind
mv ./kind kind-v0.19.0

## image 
docker pull m.daocloud.io/docker.io/kindest/node:v1.25.3
docker tag m.daocloud.io/docker.io/kindest/node:v1.25.3 kindest/node:v1.25.3

docker pull m.daocloud.io/docker.io/kindest/node:v1.30.0
docker tag m.daocloud.io/docker.io/kindest/node:v1.30.0 kindest/node:v1.30.0

## simple start
kind create cluster --name dev2 --image kindest/node:v1.30.0
kubectl cluster-info --context kind-dev2

## usage
kind create cluster --config=cluster.yaml

kubectl cluster-info --context kind-dev1

kind delete cluster -n dev1


## 参考
- Kubernetes教程(十五)---使用 kind 在本地快速部署一个 k8s集群
    https://www.lixueduan.com/posts/kubernetes/15-kind-kubernetes-in-docker/

