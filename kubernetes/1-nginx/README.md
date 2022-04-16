## Example 1: Nginx

> **ReplicaSet**
>
> ReplicaSet is a kubernetes abstraction used to manage multiple **pods** at once. It manages the pods to meet a a replication criteria, creating or deleting pods as necessary. That behavior means replicaset pods are ephemeral, hence they are not adequate for running stateful containers.
>
> Just like **Pod** configurations, replicasets are (almost) immutable, it is not possible to apply changes to most of a replicaset properties.

[0-replicaset.yaml](./0-replicaset.yaml) describes a configuration to deploy a replicaset of nginx servers.

```shell
$ kubectl apply --filename 0-replicaset.yaml
replicaset.apps/nginx-replicaset created

$ kubectl delete --filename 0-replicaset.yaml
replicaset.apps "nginx-replicaset" deleted
```

Making changes to the replicaset containers and re-applying the configuration file will not trigger any changes.

> **Deployment**
>
> A deployment is another an extra abstraction layer around replicasets. Deployments are used to gracefully apply changes to replicasets. Whenever new changes are applied, a deployment creates a new replicaset, starts phasing in the new pods, while at the same time phasing out the pods from the old replicaset, which is deleted at the end of the process.
>
> Deployment configuration files are identical to replicasets' except for the `kind` property.

[1-deployment.yaml](./1-deployment.yaml) and [1-deployment.yaml](./1-deployment-updated.yaml) describes the configuration of a deployment of nginx servers.

```shell
$ kubectl apply --filename 1-deployment.yaml
deployment.apps/nginx-deployment created

$ # making change to exposed port
$ sed 's/containerPort: 80/containerPort: 8080/' 1-deployment.yaml > 1-deployment-updated.yaml

$ # re-applying update deployment configuration
$ kubectl apply --filename 1-deployment-updated.yaml
deployment.apps/nginx-deployment configured
```

It is possible to watch the pods changing using the `kubectl get pods` subcommand:

```shell
$ kubectl get pods --watch
# <- first apply command
NAME                              READY   STATUS    RESTARTS   AGE
nginx-deployment-9fbb7d78-tnlsx   0/1     Pending   0          0s
nginx-deployment-9fbb7d78-7f2ld   0/1     Pending   0          0s
nginx-deployment-9fbb7d78-tnlsx   0/1     Pending   0          0s
nginx-deployment-9fbb7d78-7f2ld   0/1     Pending   0          0s
nginx-deployment-9fbb7d78-tnlsx   0/1     ContainerCreating   0          0s
nginx-deployment-9fbb7d78-7f2ld   0/1     ContainerCreating   0          0s
nginx-deployment-9fbb7d78-7f2ld   1/1     Running             0          9s
nginx-deployment-9fbb7d78-tnlsx   1/1     Running             0          10s
# <- second apply command
nginx-deployment-77f8d88b9d-hx6q6   0/1     Pending             0          1s
nginx-deployment-77f8d88b9d-hx6q6   0/1     Pending             0          1s
nginx-deployment-77f8d88b9d-hx6q6   0/1     ContainerCreating   0          1s
nginx-deployment-77f8d88b9d-hx6q6   1/1     Running             0          6s
nginx-deployment-9fbb7d78-tnlsx     1/1     Terminating         0          31s
nginx-deployment-77f8d88b9d-qwtgw   0/1     Pending             0          1s
nginx-deployment-77f8d88b9d-qwtgw   0/1     Pending             0          1s
nginx-deployment-77f8d88b9d-qwtgw   0/1     ContainerCreating   0          1s
nginx-deployment-9fbb7d78-tnlsx     0/1     Terminating         0          36s
nginx-deployment-9fbb7d78-tnlsx     0/1     Terminating         0          36s
nginx-deployment-9fbb7d78-tnlsx     0/1     Terminating         0          37s
nginx-deployment-77f8d88b9d-qwtgw   1/1     Running             0          9s
nginx-deployment-9fbb7d78-7f2ld     1/1     Terminating         0          40s
nginx-deployment-9fbb7d78-7f2ld     0/1     Terminating         0          44s
nginx-deployment-9fbb7d78-7f2ld     0/1     Terminating         0          45s
nginx-deployment-9fbb7d78-7f2ld     0/1     Terminating         0          45s
```

We can also use the describe command to check a deployment or replicaset:

```shell
$ kubectl describe deployments nginx-deployment
Name:                   nginx-deployment
Namespace:              default
CreationTimestamp:      ...
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx
Replicas:               2 desired | 2 updated | 2 total | 2 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx:alpine
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   nginx-deployment-9fbb7d78 (2/2 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  34m   deployment-controller  Scaled up replica set nginx-deployment-9fbb7d78 to 2
```

## Networking

So far, we could only access our pods by `kubectl port-forward`ing their open ports. Containers inside a pod can easily access each other through localhost because they use the same network. However, pods are nonpermanent, and have dynamically assigned IPs each time they are created, so it is not possible to know ahead of time with IP address a pod is going to use. Another issue is that when using replicasets or deployments, multiple pods may be created, and we will want to split requests among them.

To solve all these problems, kubernetes provides **Services**.

> **Service**
>
> A Service is a networking abstraction that allows a set of pods to be exposed as a single network service. In order to achieve that, services have their own IP address and DNS names inside a kubernetes cluster. All requests that arrive on the service will be distributed (using a load balancer) to the pods that match a service's selector rules.
>
> When used together with _deployments_, services allow _rolling updates_ to be applied.

[2-service.yaml](./2-service.yaml) describes a service configuration. The `ports` section describe all ports that are going to be mapped from the service to pods <port:service> -> <targetPort:pod>.

The `selector` section describes the rules used to match which pods are going to be part of the service. Selectors are a list of key-value pairs that matches pods `metadata.labels` values. All service rules need to match in order to a pod to become part of the service.

Just like deployments, service configuration can be applied with the `kubectl apply` command.

```shell
$ kubectl apply --filename 2-service.yaml
service/nginx created

$ # services are mutable, meaning we can easily re-apply changed configurations
$ # making change to exposed port
$ sed 's/port: 8000/port: 8080/' 2-service.yaml > 2-service-updated.yaml

$ # re-applying update deployment configuration
$ kubectl apply --filename 2-service-updated.yaml
service/nginx configured
```

At this point a pod can easily access set of pods by using their service. The service is still not exposed externally, so we can only test it from inside the cluster. Unfortunately, pods from given service cannot access themselves through that service, so we need to create a new test pod.

```shell
$ # the creation order of services and deployments does not matter
$ # create or update our deployment
$ kubectl apply --filename 1-deployment.yaml
deployment.apps/nginx-deployment created

$ # create or update our service
$ kubectl apply --filename 2-service.yaml
service/nginx unchanged

$ # create a pod for testing
$ # the sleep command is initially set so the pod does not terminate
$ kubectl run test-pod --image alpine --command -- sh -c "sleep 1d"
pod/test-pod created

$ # open a shell in the test pod and access nginx pods through service
$ kubectl exec -it test-pod -- sh
# # shell on nginx-deployment-9fbb7d78-8gndt.nginx container
# wget -O - http://nginx:8000
Connecting to nginx:8000 (10.100.243.28:8000)
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

The service name is used as the domain name as well, so we can access the service pods by through (if using http) `http://<service-name>:<service-port>` -> `http://nginx:8000`. That behavior changes slightly when using _namespaces_. Namespaces were not introduced yet, but just for coverage purposes, when a service is part of a namespace the service url must also contain the namespace name:

We can list all services with the following command: `http://<service-name>.<namespace-name>:<service-port>`.

```shell
$ kubectl get services
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP    35m
nginx        ClusterIP   10.100.243.28   <none>        8080/TCP   8m33s

$ # by setting output to wide, se can see the services' selectors
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE   SELECTOR
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP    39m   <none>
nginx        ClusterIP   10.100.243.28   <none>        8080/TCP   12m   app=nginx
```

Describing a service will also provide some extra information:

```shell
$ kubectl describe services nginx
Name:              nginx
Namespace:         default
Labels:            <none>
Annotations:       <none>
Selector:          app=nginx
Type:              ClusterIP
IP Family Policy:  SingleStack
IP Families:       IPv4
IP:                10.100.243.28
IPs:               10.100.243.28
Port:              <unset>  8080/TCP
TargetPort:        80/TCP
Endpoints:         172.17.0.3:80,172.17.0.4:80
Session Affinity:  None
Events:            <none>
```
