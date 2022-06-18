## Example 4: Prometheus

> **Helm**
>
> [Helm](https://helm.sh/) is a package manager for kubernetes. A Helm registry serves packages called _charts_. A chart is a set of template files, with the purposes of deploying an application into a cluster.
>
> Helm is also a Kubernetes template engine. Charts' template files are just Kubernetes configuration files that allow values to be injected and conditional expressions to be evaluated based on external properties. These properties are called _values_, and can be used to generate the Kubernetes configuration files from a chart's templates. The resulting files are then applied to the cluster by helm.

The helm CLI tool is not part of kubernetes. Hence, it needs to be installed separately.

Helm's main registry is https://artifacthub.io/. It can be used to search for packages, and look at installation scripts, template files and default values.

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm install prometheus prometheus-community/kube-prometheus-stack

helm uninstall prometheus
