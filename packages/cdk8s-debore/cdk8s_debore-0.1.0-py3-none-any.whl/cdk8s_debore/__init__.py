"""
# cdk8s-debore

Run your apps on Kubernetes cluster without bored YAMLing, powered by the [cdk8s project](https://cdk8s.io) 🚀

## Overview

**cdk8s-debore** is a [cdk8s](https://cdk8s.io) library which allows you to define your Kubernetes app with just few lines of code.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DeboredApp(self, "webapp",
    image="your-image:latest",
    auto_scale=True,
    ingress=True
)
```

Then the Kubernetes manifests created by `cdk8s synth` command will have Kubernetes resources such as `Deployment`, `Service`, `HorizontalPodAutoscaler`, `Ingress`, as follows.

<details>
<summary>manifest.k8s.yaml</summary>

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-webapp-deployment-deployment-d67b425c
  namespace: default
spec:
  selector:
    matchLabels:
      app: myappwebapp4BD95A2A
  template:
    metadata:
      labels:
        app: myappwebapp4BD95A2A
    spec:
      containers:
        - image: your-image:latest
          imagePullPolicy: Always
          name: app
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: 400m
              memory: 512Mi
            requests:
              cpu: 200m
              memory: 256Mi
---
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-webapp-deployment-hpa-bd8107fd
  namespace: default
spec:
  maxReplicas: 10
  metrics:
    - resource:
        name: cpu
        target:
          averageUtilization: 85
          type: Utilization
      type: Resource
    - resource:
        name: memory
        target:
          averageUtilization: 75
          type: Utilization
      type: Resource
  minReplicas: 1
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app-webapp-deployment-deployment-d67b425c
---
apiVersion: v1
kind: Service
metadata:
  name: my-app-webapp-exposable-service-d6a35671
  namespace: default
spec:
  ports:
    - port: 8080
      targetPort: 80
  selector:
    app: myappwebapp4BD95A2A
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/rewrite-target: /
  name: my-app-webapp-exposable-ingress-c350957f
  namespace: default
spec:
  rules:
    - http:
        paths:
          - backend:
              serviceName: my-app-webapp-exposable-service-d6a35671
              servicePort: 80
            path: /my-app-webapp-deployment-deployment-d67b425c
```

</details>

## Installation

[cdk8s](https://cdk8s.io) supports TypeScript and Python at this point, so as cdk8s-debore.

### TypeScript

TODO

### Python

TODO

## Contribution

1. Fork ([https://github.com/toricls/cdk8s-debore/fork](https://github.com/toricls/cdk8s-debore/fork))
2. Bootstrap the repo:

   ```bash
   npx projen   # generates package.json and friends
   yarn install # installs dependencies
   ```
3. Development scripts:
   |Command|Description
   |-|-
   |`yarn compile`|Compiles typescript => javascript
   |`yarn watch`|Watch & compile
   |`yarn test`|Run unit test & linter through jest
   |`yarn test -u`|Update jest snapshots
   |`yarn run package`|Creates a `dist` with packages for all languages.
   |`yarn build`|Compile + test + package
   |`yarn bump`|Bump version (with changelog) based on [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
   |`yarn release`|Bump + push to `master`
4. Create a feature branch
5. Commit your changes
6. Rebase your local changes against the master branch
7. Create a new Pull Request (use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for the title please)

## Licence

[Apache License, Version 2.0](./LICENSE)

## Author

[Tori](https://github.com/toricls)
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import cdk8s
import constructs

from ._jsii import *


class DeboredApp(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk8s-debore.DeboredApp"):
    """DeboredApp class.

    stability
    :stability: experimental
    """
    def __init__(self, scope: constructs.Construct, name: str, *, auto_scale: typing.Optional[bool]=None, container_port: typing.Optional[jsii.Number]=None, default_replicas: typing.Optional[jsii.Number]=None, image: typing.Optional[str]=None, ingress: typing.Optional[bool]=None, namespace: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, resources: typing.Optional["ResourceRequirements"]=None) -> None:
        """
        :param scope: -
        :param name: -
        :param auto_scale: Whether use HPA or not. Default: false
        :param container_port: Internal port. Default: 8080
        :param default_replicas: Number of replicas. If ``autoScale`` is enabled, this will be used for ``minReplicas`` (while ``maxReplicas`` is x10). Otherwise, this value will be used to specify the exact number of replicas in the deployment. Default: 1
        :param image: The Docker image to use for this app. Default: 'busybox'
        :param ingress: Whether use Nginx ingress or not. Default: false
        :param namespace: The Kubernetes namespace where this app to be deployed. Default: 'default'
        :param port: External port. Default: 80
        :param resources: Resources requests for the web app. Default: - Requests = { CPU = 200m, Mem = 256Mi }, Limits = { CPU = 400m, Mem = 512Mi }

        stability
        :stability: experimental
        """
        opts = DeboredOptions(auto_scale=auto_scale, container_port=container_port, default_replicas=default_replicas, image=image, ingress=ingress, namespace=namespace, port=port, resources=resources)

        jsii.create(DeboredApp, self, [scope, name, opts])


@jsii.data_type(jsii_type="cdk8s-debore.DeboredOptions", jsii_struct_bases=[], name_mapping={'auto_scale': 'autoScale', 'container_port': 'containerPort', 'default_replicas': 'defaultReplicas', 'image': 'image', 'ingress': 'ingress', 'namespace': 'namespace', 'port': 'port', 'resources': 'resources'})
class DeboredOptions():
    def __init__(self, *, auto_scale: typing.Optional[bool]=None, container_port: typing.Optional[jsii.Number]=None, default_replicas: typing.Optional[jsii.Number]=None, image: typing.Optional[str]=None, ingress: typing.Optional[bool]=None, namespace: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, resources: typing.Optional["ResourceRequirements"]=None) -> None:
        """
        :param auto_scale: Whether use HPA or not. Default: false
        :param container_port: Internal port. Default: 8080
        :param default_replicas: Number of replicas. If ``autoScale`` is enabled, this will be used for ``minReplicas`` (while ``maxReplicas`` is x10). Otherwise, this value will be used to specify the exact number of replicas in the deployment. Default: 1
        :param image: The Docker image to use for this app. Default: 'busybox'
        :param ingress: Whether use Nginx ingress or not. Default: false
        :param namespace: The Kubernetes namespace where this app to be deployed. Default: 'default'
        :param port: External port. Default: 80
        :param resources: Resources requests for the web app. Default: - Requests = { CPU = 200m, Mem = 256Mi }, Limits = { CPU = 400m, Mem = 512Mi }

        stability
        :stability: experimental
        """
        if isinstance(resources, dict): resources = ResourceRequirements(**resources)
        self._values = {
        }
        if auto_scale is not None: self._values["auto_scale"] = auto_scale
        if container_port is not None: self._values["container_port"] = container_port
        if default_replicas is not None: self._values["default_replicas"] = default_replicas
        if image is not None: self._values["image"] = image
        if ingress is not None: self._values["ingress"] = ingress
        if namespace is not None: self._values["namespace"] = namespace
        if port is not None: self._values["port"] = port
        if resources is not None: self._values["resources"] = resources

    @builtins.property
    def auto_scale(self) -> typing.Optional[bool]:
        """Whether use HPA or not.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('auto_scale')

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        """Internal port.

        default
        :default: 8080

        stability
        :stability: experimental
        """
        return self._values.get('container_port')

    @builtins.property
    def default_replicas(self) -> typing.Optional[jsii.Number]:
        """Number of replicas.

        If ``autoScale`` is enabled, this will be used for ``minReplicas`` (while
        ``maxReplicas`` is x10). Otherwise, this value will be used to specify the
        exact number of replicas in the deployment.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('default_replicas')

    @builtins.property
    def image(self) -> typing.Optional[str]:
        """The Docker image to use for this app.

        default
        :default: 'busybox'

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def ingress(self) -> typing.Optional[bool]:
        """Whether use Nginx ingress or not.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('ingress')

    @builtins.property
    def namespace(self) -> typing.Optional[str]:
        """The Kubernetes namespace where this app to be deployed.

        default
        :default: 'default'

        stability
        :stability: experimental
        """
        return self._values.get('namespace')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """External port.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get('port')

    @builtins.property
    def resources(self) -> typing.Optional["ResourceRequirements"]:
        """Resources requests for the web app.

        default
        :default: - Requests = { CPU = 200m, Mem = 256Mi }, Limits = { CPU = 400m, Mem = 512Mi }

        stability
        :stability: experimental
        """
        return self._values.get('resources')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DeboredOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="cdk8s-debore.ResourceQuantity", jsii_struct_bases=[], name_mapping={'cpu': 'cpu', 'memory': 'memory'})
class ResourceQuantity():
    def __init__(self, *, cpu: typing.Optional[str]=None, memory: typing.Optional[str]=None) -> None:
        """
        :param cpu: Default: - no limit
        :param memory: Default: - no limit

        stability
        :stability: experimental
        """
        self._values = {
        }
        if cpu is not None: self._values["cpu"] = cpu
        if memory is not None: self._values["memory"] = memory

    @builtins.property
    def cpu(self) -> typing.Optional[str]:
        """
        default
        :default: - no limit

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory(self) -> typing.Optional[str]:
        """
        default
        :default: - no limit

        stability
        :stability: experimental
        """
        return self._values.get('memory')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ResourceQuantity(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="cdk8s-debore.ResourceRequirements", jsii_struct_bases=[], name_mapping={'limits': 'limits', 'requests': 'requests'})
class ResourceRequirements():
    def __init__(self, *, limits: typing.Optional["ResourceQuantity"]=None, requests: typing.Optional["ResourceQuantity"]=None) -> None:
        """
        :param limits: Maximum resources for the web app. Default: - CPU = 400m, Mem = 512Mi
        :param requests: Required resources for the web app. Default: - CPU = 200m, Mem = 256Mi

        stability
        :stability: experimental
        """
        if isinstance(limits, dict): limits = ResourceQuantity(**limits)
        if isinstance(requests, dict): requests = ResourceQuantity(**requests)
        self._values = {
        }
        if limits is not None: self._values["limits"] = limits
        if requests is not None: self._values["requests"] = requests

    @builtins.property
    def limits(self) -> typing.Optional["ResourceQuantity"]:
        """Maximum resources for the web app.

        default
        :default: - CPU = 400m, Mem = 512Mi

        stability
        :stability: experimental
        """
        return self._values.get('limits')

    @builtins.property
    def requests(self) -> typing.Optional["ResourceQuantity"]:
        """Required resources for the web app.

        default
        :default: - CPU = 200m, Mem = 256Mi

        stability
        :stability: experimental
        """
        return self._values.get('requests')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ResourceRequirements(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "DeboredApp",
    "DeboredOptions",
    "ResourceQuantity",
    "ResourceRequirements",
]

publication.publish()
