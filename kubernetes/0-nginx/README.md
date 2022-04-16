## Example 0: Nginx

> **Pod**
>
> In kubernetes, the smallest deployable unit is a **Pod**. A pod is a group of one or more containers with shared storage and network. Usually a single container is instantiated per pod.

[0-pod-single-container.yaml](./0-pod-single-container.yaml) describes a configuration for starting a pod called _nginx-pod-single-container_ containing a single container called _nginx_.

The following command can be used to apply the configuration. Applying an existing configuration will cause it to be automatically updated.

```shell
$ kubectl apply --filename 0-pod-single-container.yaml
pod/nginx-pod-single-container created
...
$ # a short filename option is available:
$ # kubectl apply -f 0-pod-single-container.yaml
```

To delete the pod:

```shell
$ kubectl delete --filename 0-pod-single-container.yaml
pod "nginx-pod-single-container" deleted
```

A single pod could be instantiated as well only via command line:

```shell
$ # crate new pod called nginx-pod-cli
$ kubectl run nginx-pod-cli --image nginx
...

$ # delete the pod
$ kubectl delete pods nginx-pod-cli
...
```

Most, if not all kubernetes components can be deployed without configuration files, but the amount options that need to be specified makes it impractical. Therefore, these notes will only use configuration files for instantiating resources in the kubernetes cluster.

> **(Almost) Immutable Pod Configuration**
>
> It is important to notice that most of the pod properties are immutable, meaning it is not possible to re-apply the configuration after some changes are made.
>
> Few pods properties are mutable, such as the container's image. Most other property changes will likely require deleting and applying the configuration again.

[1-pod-multi-container.yaml](./1-pod-multi-container.yaml) describes a configuration for starting a pod called _nginx-pod-multi-container_ containing two containers called _nginx_ and _python_.

Containers inside a pod share the network, that means they access each other using `localhost`, but cannot use the same ports. Doing so is likely to cause processes that try binding already used ports to crash.

### Interacting with pods

We can list all running pods to check their status and other properties:

```shell
$ # assuming we keep the previous pods running
$ kubectl get pods
NAME                         READY   STATUS    RESTARTS   AGE
nginx-pod-cli                1/1     Running   0          2m51s
nginx-pod-multi-container    2/2     Running   0          3m13s
nginx-pod-single-container   1/1     Running   0          3m18s


$ # there are multiple output types such as 'name', 'wide', 'json, 'yaml' and so on
$ # wide output is useful for checking a pod's ip address.
$ kubectl get pods --output wide
NAME                         READY   STATUS    RESTARTS   AGE     IP            NODE           NOMINATED NODE   READINESS GATES
nginx-pod-cli                1/1     Running   0          3m14s   10.244.1.10   minikube-m02   <none>           <none>
nginx-pod-multi-container    2/2     Running   0          3m36s   10.244.2.22   minikube-m03   <none>           <none>
nginx-pod-single-container   1/1     Running   0          3m41s   10.244.1.9    minikube-m02   <none>           <none>
```

We can also describe a single pods properties:

```shell
$ # ...=> suppressed output
$ kubectl describe pods nginx-pod-multi-container
Name:         nginx-pod-multi-container
Namespace:    default
Priority:     0
Node:         minikube-m03/192.168.49.4
...
Status:       Running
IP:           10.244.2.22
IPs:
  IP:  10.244.2.22
Containers:
  nginx:
    ...
    Port:           80/TCP
    ...
    State:          Running
      ...
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      ...
  python:
    ...
    Port:          8001/TCP
    ...
    Command:
      python
    Args:
      -m
      http.server
      $(SERVER_PORT)
    State:          Running
      ...
    Ready:          True
    Restart Count:  0
    Environment:
      SERVER_PORT:  8001
    Mounts:
      ...
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  ...
...
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  7m41s  default-scheduler  Successfully assigned default/nginx-pod-multi-container to minikube-m03
  Normal  Pulling    7m35s  kubelet            Pulling image "nginx"
  Normal  Pulled     7m33s  kubelet            Successfully pulled image "nginx" in 2.173799487s
  Normal  Created    7m32s  kubelet            Created container nginx
  Normal  Started    7m31s  kubelet            Started container nginx
  Normal  Pulled     7m31s  kubelet            Container image "python:alpine" already present on machine
  Normal  Created    7m29s  kubelet            Created container python
  Normal  Started    7m28s  kubelet            Started container python
```

The _Events_ section of the describe command is useful for debugging issues when containers do not start, causing multiple container restarts.

In order to access a pod's containers we need to forward their ports:

```shell
$ kubectl port-forward nginx-pod-multi-container 8001
Forwarding from 127.0.0.1:8001 -> 8001
Forwarding from [::1]:8001 -> 8001
Handling connection for 8001
...

$ # a different host port can be used
$ kubectl port-forward nginx-pod-single-container 8000:80
Forwarding from 127.0.0.1:8000 -> 80
Forwarding from [::1]:8000 -> 80
Handling connection for 8000
...
```

The `kubectl port-forward` command start a proxy service, so it will only work if the command is kept running.

After interacting with the pods, we can check their logs:

```shell
$ # ...=> suppressed output
$ kubectl logs nginx-pod-single-container
[pedro@pedro-laptop 0-nginx]$ kubectl logs nginx-pod-single-container
...
18:31:07 [notice] 1#1: nginx/1.21.6
18:31:07 [notice] 1#1: built by gcc 10.2.1 20210110 (Debian 10.2.1-6)
18:31:07 [notice] 1#1: OS: Linux 5.17.3-arch1-1
18:31:07 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
18:31:07 [notice] 1#1: start worker processes
...

$ # for multi container pods, the container must be specified
$ kubectl logs nginx-pod-multi-container --container python
127.0.0.1 - - [18:50:07] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [18:50:07] code 404, message File not found
127.0.0.1 - - [18:50:07] "GET /favicon.ico HTTP/1.1" 404 -
```

Lastly, we can execute commands inside a container using the `kubectl exec` subcommand.

```shell
$ kubectl exec -it nginx-pod-single-container -- sh
# # shell on nginx-pod-single-container.nginx container
...

$ # on multi container pods, one of the container is used
$ kubectl exec -it nginx-pod-multi-container -- sh
Defaulted container "nginx" out of: nginx, python
# # shell on nginx-pod-single-container.nginx container
...

$ # a container can be chose with the --container option
$ kubectl exec -it nginx-pod-multi-container --container python -- sh
# # shell on nginx-pod-single-container.python container
# # accessing nginx-pod-single-container.python through local network
# wget -O - localhost
Connecting to localhost (127.0.0.1:80)
writing to stdout
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>
...
</body>
</html>
-                    100% |*********************|   615  0:00:00 ETA
written to stdout
```
