# chas
MonoRepo for CHaS - Container Hosting System

## Components

* Scheduler - Allocates Containers to Nodes
* API - An API that maintains the state of the containers and the hosts they run on.
* Router - Ingress - Manages service discovery, the load balancing and ingress routing
* Datastore - mongodb/etcd, for persistence of state
* Nodes - Virtual Machines that host containers. Workload managed by Scheduler
  * https://github.com/awslabs/amazon-eks-ami/blob/main/templates/al2023/provisioners/install-worker.sh eg
  * iptables
  * containerd = v2
  * nerdctl = cmdline docker replacement
  * CNI - not yet
* Container - a running container instance on a node with it's configuration
  * image
  * port
  * command
  * env (list of environment vars)
  * resources (list of cpu and memory allocations)
* Deployment - The configuration of desired state of container(s)

TODO:
* Secret Management
* Storage
* Network comms

