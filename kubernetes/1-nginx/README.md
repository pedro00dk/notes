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

## Networking
