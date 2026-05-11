# Kubernetes Cluster Automation

## Overview

Ansible automation for building and operating a Kubernetes cluster on Ubuntu virtual machines. The project prepares hosts, installs the container runtime and Kubernetes components, initializes the control plane, joins workers, and can deploy common platform add-ons such as vSphere CSI, Argo CD, Prometheus, Grafana, and Velero/MinIO backup resources.

## Features

- Host preparation for Kubernetes nodes
- containerd, runc, and CNI plugin installation
- kubeadm-based Kubernetes cluster bootstrap
- Control-plane initialization and worker join flow
- Optional platform add-ons controlled by inventory variables
- vSphere CSI storage integration tasks
- Argo CD deployment task
- Prometheus and Grafana deployment tasks
- Velero/MinIO manifests for backup lab workflows

## Architecture / Structure

```text
k8s/
├── inventory/
│   ├── hosts.yaml          # Cluster node inventory
│   └── components.yaml     # Add-on deployment toggles
├── tasks/
│   ├── system_prepare.yml  # OS/runtime/Kubernetes bootstrap
│   ├── vSphere-CSI.yml     # vSphere CSI setup
│   ├── argoCD-deployment.yml
│   ├── prometheus-deployment.yml
│   └── grafana-deployment.yml
├── vars/all.yml            # Kubernetes/runtime/add-on variables
├── velero/                 # Velero + MinIO kustomize manifests
└── site.yaml               # Main playbook
```

Typical topology:

```text
Ansible controller -> Kubernetes control plane -> worker nodes
                                      |
                                      +-> CNI, CSI, GitOps, monitoring, backup add-ons
```

## Prerequisites

- Ubuntu-based VMs or hosts for Kubernetes nodes
- SSH access from the Ansible controller to all nodes
- Sudo privileges on target hosts
- Ansible installed on the controller
- Network connectivity between all cluster nodes
- Internet or local mirror access for packages and container images
- vSphere/vCenter access only if enabling vSphere CSI

Install useful Ansible collections:

```bash
ansible-galaxy collection install kubernetes.core community.general
```

## Getting Started

```bash
git clone https://github.com/jonny-levi/k8s.git
cd k8s
```

Review and customize:

- `inventory/hosts.yaml` — node names and SSH settings
- `vars/all.yml` — Kubernetes/runtime versions and environment settings
- `inventory/components.yaml` — optional add-ons to deploy

Run the playbook:

```bash
ansible-playbook site.yaml -i inventory/
```

## Deployment / Operations

Validate the cluster:

```bash
kubectl get nodes -o wide
kubectl get pods -A
kubectl get storageclass
```

Deploy selected add-ons by enabling them in `inventory/components.yaml` and rerunning the playbook.

For adding workers to an existing cluster, generate a fresh kubeadm join command and run with an Ansible limit that targets only the new worker hosts.

## Backup / Monitoring

- Use the Prometheus and Grafana tasks for baseline observability.
- Use Velero/MinIO manifests as a starting point for backup workflows.
- Back up cluster manifests, inventory, and any external datastore or persistent volume data.
- Test restore procedures before relying on backups.

## Security Notes

- Never commit real SSH passwords, kubeadm tokens, kubeconfigs, vCenter credentials, or registry credentials.
- Use Ansible Vault, SSH keys, and environment-specific private inventories.
- Rotate any bootstrap tokens or credentials that were committed or shared.
- Review add-on exposure, RBAC, and network access before production use.

## Author

Jonny Levi — [github.com/jonny-levi](https://github.com/jonny-levi)
