# Login Servers for Kubernetes 

All passwordless. 

Create the namespace:

```console 
$ kubectl create namespace opus
$ kubectl create namespace arya
```

Add the login servers repo:

```console 
$ helm repo add cloud-native-server https://mike-matera.github.io/cloud-native-server/
$ helm repo update 
```

## CA Key 

Create a secret for the CA key: 

```console 
$ kubectl -n opus create secret generic cis-ca-key --from-file=ca_key=./secrets/ca_key --from-file=ca_key.pub=./secrets/ca_key.pub 
$ kubectl -n arya create secret generic cis-ca-key --from-file=ca_key=./secrets/ca_key --from-file=ca_key.pub=./secrets/ca_key.pub 
```

## Opus 

```console 
$ helm install -n opus opus cloud-native-server/cloud-server \
    --set ssh.existingSecret=cis-ca-key \
    --values values-opus.yaml
```

## Sun Hwa

Practice: 

```console 
$ helm install -n opus sun-hwa-p1 cloud-native-server/cloud-server \
    --set ssh.existingSecret=cis-ca-key \
    --values values-practice-m1.yaml
```

Midterm 1: 

```console 
$ helm install -n opus sun-hwa-m1 cloud-native-server/cloud-server \
    --set ssh.existingSecret=cis-ca-key \
    --values values-midterm1.yaml
```

## Certificate Signing App 

This app enables certificate signing and works as an HTTP server for opus:

```console
$ kubectl apply -f ./signer-app.yaml
``` 

## Arya 

```console 
$ python ./generate-arya.py update
```

