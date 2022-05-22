# Kubernetes

This repository was created to learn and practice kubernetes concepts and tools. It follows an example based approach, meaning kubernetes concepts and details will be only shallowly presented as examples examples use it. More details can be found at kubernetes documentation. Commands are also only superficially presented, use `--help` to check for more options.

Useful links:

-   Kubernetes Home: https://kubernetes.io/
-   Documentation: https://kubernetes.io/docs/home/

## Getting Started

Two things are necessary to get started with kubernetes, a cluster where the applications are executed, and kubectl, the tool to interact with the cluster.

### Cluster

A kubernetes cluster is the set of computing environments (physical, virtual, or container machines) called **nodes** where the the applications run.

Usually there are two types of nodes, master and worker. Master nodes manager the cluster and workers run the applications. A node might also be both master and worker at the same time, but that is only used on development environments.

For development purposes, there are several tools that can be used to create kubernetes clusters, such as:

-   [`kubeadm`](https://kubernetes.io/docs/reference/setup-tools/kubeadm/): The _hard_ way to setup a kubernetes cluster. It can be used to setup clusters using the best kubernetes practices, but it is more convoluted to use if compared to other tools.
-   [`minikube`](https://minikube.sigs.k8s.io/docs/): A simple solution for setting up a kubernetes cluster. It is the tool that will be used in the following steps.
-   [`kind`](https://minikube.sigs.k8s.io/docs/): Another simple solution that uses docker containers to create a cluster.
-   There are other options to create and manage local kubernetes clusters such as [Docker Desktop](https://www.docker.com/products/docker-desktop/), [Rancher Desktop](https://rancherdesktop.io/) [k3s](https://k3s.io/), [`MicroK8s`](https://microk8s.io/) and many more.
-   Manually created kubernetes clusters can be created in production environments and public clouds. On the latter, managed cloud solutions such as [Google Cloud Platform (GCP)](https://cloud.google.com/)`s [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) are usually recommended.

### Minikube

Setting up a cluster using minikube is straightforward, just run `minikube start` and a new cluster is going to be automatically created.

Clusters are going to use different technologies (called [drivers](https://minikube.sigs.k8s.io/docs/drivers/)) under the hood depending on the platform. As a recommendation, the docker driver is preferred on all platforms, and can be used by running `minikube start --driver docker`.

Other relevant options that can passed to `minikube start` are `--cpus <count|int>` for specifying how many cpu cores a cluster node has access (per node), `--memory <mb|int>` to set the cluster node memory (per node), and `--nodes <count|int>` to define how many nodes will be created.

Optionally, all these options can be set as default by running `minikube config set <option> <value>`, e.g. `minikube config set driver docker`, `minikube config set memory 4096`.

#### Profiles

Multiple kubernetes clusters can be created by using different profiles, each cluster may have different configuration as well. By default, the `minikube` profile is used for all commands (`start`, `stop`, etc).

In order to create a new cluster the `--profile <name>` option can be set (e.g. `minikube start --profile my-second-cluster`). The profiles can be listed with the `minikube profile list` command.

### Kubectl

Kubectl is the de-facto command line tool for managing kubernetes clusters. Before being able to manage clusters it first needs to connect to them. The following link (https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/) contains the documentation on different ways to connect to clusters.

When using minikube however, that is automatically setup when a cluster is created. The configuration can be checked with the command `kubectl config view` or accessing the configuration file at `~/.kube/config`.

Examples:

-   [Example 0: Nginx](./0-nginx/): Introduction to pods, creating and interacting them.
-   [Example 1: Nginx](./1-nginx/): ReplicaSets, deployments, and services (internal).
-   [Example 2: Mongo](./2-mongo/): ConfigMaps, secrets, multi-document files, and services (internal and external).
