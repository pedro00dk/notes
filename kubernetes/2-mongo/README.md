## Example 2: Mongo

> **ConfigMap**
>
> ConfigMaps are used to store a non-confidential set of key-value properties that can be accessed by pods through environment variables.
>
> ConfigMaps can be mounted as both environment variables or as files in a pod.

[0-configmap.yaml](./0-configmap.yaml) describes a configmap with information mongodb's host and port.

> **Secret**
>
> Just like ConfigMaps, secrets are used to store key-value properties that can be accessed by pods. However, secrets are intended to hold confidential data. Secrets values must be base64 encoded, but they are not encrypted/secured by default. Check the kubernetes documentation on details to keep secrets safe.

[1-secret.yaml](./1-secret.yaml) describes a kubernetes secret with the mongo database credentials. The opaque type means the secret contains arbitrary user data. For other types check https://kubernetes.io/docs/concepts/configuration/secret/#secret-types.

```shell
$ kubectl apply --filename 0-configmap.yaml
configmap/mongo created
$ kubectl apply --filename 1-secret.yaml
secret/mongo created
```

### Multi-document configuration files

Now we have both ConfigMap and Secret applied we can setup the mongodb deployment and its service. It is a common practice to declare both the deployment and its service in a single configuration file because they are closely related.

Multiple documents can be declared in a single `.yaml` file by dividing them with a triple dash (---). Kubernetes will consume them in the order they are declared.

```yaml
# document 1
apiVersion: ...
kind: ...
# rest of first document
---
# document 2
apiVersion: ...
kind: ...
# rest of second document
---
# ...
---
# document n
apiVersion: ...
kind: ...
# rest of nth document
```

Applying [2-deployment-service-mongodb.yaml](./2-deployment-service-mongodb.yaml) multi-document configuration:

```shell
$ kubectl apply --filename 2-deployment-service-mongodb.yaml
deployment.apps/mongo created
service/mongo created
```

The mongodb configuration contains a deployment and its _internal_ service.

Now we can apply [3-deployment-service-express.yaml](./2-deployment-service-express.yaml) configuration containing a mongo-express deployment and its service. Mongo-express is a small admin tool that we can use to interact with mongodb.

```shell
$ kubectl apply --filename 3-deployment-service-express.yaml
deployment.apps/mongo-express created
service/mongo-express created
```

### External Services

Different from the mongodb service, the mongo-express service is external. External services have a `type: NodePort` or `type: LoadBalancer` (note: internal services `type: ClusterIP` are still load balancers).

#### `type: NodePort` Service

NodePort services are the most primitive type of external services. It works by exposing a port (called `nodePort`) on all cluster nodes. A node port must be in the range 30000–32767. Once set up, the service will be directly addressable through each of the cluster node IPs on the service's `nodePort`. This type of service is not very secure because the ports are always open, so external clients have direct access to worker nodes.

When using minikube, the nodes' IPs can be obtained through the `minikube` or `kubectl` commands

```shell
$ # minikube provides the ip of the master node
$ minikube ip
192.168.49.2

$ # kubectl can provide the ip of all nodes
$ kubectl get nodes --output wide
NAME           ...   INTERNAL-IP    ...
minikube       ...   192.168.49.2   ...
minikube-m02   ...   192.168.49.3   ...
minikube-m03   ...   192.168.49.4   ...
```

Given the internal IPs returned by the kubectl command, our service will be available at: `192.168.49.2:8081`, `192.168.49.3:8081`, and `192.168.49.4:8081`.

#### `type: LoadBalancer` Service

This is the preferred type of external service. However, it is only available by cloud providers such as Google Cloud Platform. Load balancer services extend on nodePort services by rerouting requests from the cloud provider's external load balancer into the kubernetes cluster. The `nodePort` is still required, but now they are only exposed to the load balancer itself, which is going to redirect the traffic.
