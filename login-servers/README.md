# Login Servers for Kubernetes 

All passwordless. 

Create the namespace:

```console 
$ kubectl create namespace login-servers
```

Add the login servers repo:

```console 
$ helm repo add cloud-native-server https://mike-matera.github.io/cloud-native-server/
$ helm repo update 
```

## CA Key 

Create a secret for the CA key: 

```console 
$ kubectl -n login-servers create secret generic cis-ca-key --from-file=ca_key=./secrets/ca_key --from-file=ca_key_pub=./secrets/ca_key.pub 
```

## Opus 

```console 
$ helm install -n login-servers opus cloud-native-server/cloud-server \
    --set ssh.existingSecret=cis-ca-key \
    --values values-opus.yaml
```

## Arya 

```console 
$ python ./generate-arya.py update
```

