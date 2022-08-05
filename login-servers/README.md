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

## Opus 

```console 
$ helm install -n login-servers opus cloud-native-server/cloud-server \
    --set-file ssh.ca_key=./secrets/ca_key,ssh.ca_key_pub=./secrets/ca_key.pub \
    --values values-opus.yaml
```

## Arya 

```console 
$ python ./generate-arya.py update
```

