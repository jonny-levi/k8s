# ☸️ Kubernetes Cluster Deployment

<div align="center">

**Fully automated Kubernetes cluster provisioning with Ansible**

From bare Ubuntu VMs to a production-ready K8s cluster with vSphere CSI, ArgoCD, Prometheus, and Grafana — in a single playbook run.

[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.34-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io)
[![Ansible](https://img.shields.io/badge/Ansible-Automated-EE0000?logo=ansible&logoColor=white)](https://ansible.com)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-18.04%20%7C%2022.04-E95420?logo=ubuntu&logoColor=white)](https://ubuntu.com)
[![vSphere](https://img.shields.io/badge/vSphere-CSI-607078?logo=vmware&logoColor=white)](https://vmware.com)

</div>

---

## 📋 Overview

This Ansible project automates the entire lifecycle of deploying a Kubernetes cluster on Ubuntu virtual machines running on VMware vSphere/ESXi. It handles everything from OS preparation to deploying monitoring and GitOps tools.

### What It Does

1. 🖥️ **System Preparation** — Hostname, hosts file, packages, timezone, swap disable
2. 📦 **Container Runtime** — Installs containerd, runc, and CNI plugins
3. ☸️ **Kubernetes** — Installs kubeadm, kubelet, kubectl; initializes master; joins workers
4. 🌐 **CNI** — Deploys Weave Net pod network
5. 💾 **Storage** — Configures vSphere CSI driver for persistent volumes
6. 🚀 **ArgoCD** — GitOps continuous delivery (Helm-based)
7. 📊 **Prometheus** — Cluster monitoring
8. 📈 **Grafana** — Dashboards and visualization

## 🏗️ Architecture

```
                        ┌─────────────────┐
                        │  Ansible Server │
                        │  (Controller)   │
                        └────────┬────────┘
                                 │ SSH
              ┌──────────────────┼──────────────────┐
              │                  │                  │
     ┌────────▼───────┐ ┌───────▼────────┐ ┌───────▼────────┐
     │  Master Node   │ │  Worker Node 1 │ │  Worker Node 2 │
     │  172.20.10.30  │ │  172.20.10.31  │ │  172.20.10.32  │
     │                │ │                │ │                │
     │ • API Server   │ │ • kubelet      │ │ • kubelet      │
     │ • etcd         │ │ • containerd   │ │ • containerd   │
     │ • Scheduler    │ │ • kube-proxy   │ │ • kube-proxy   │
     │ • Controller   │ │                │ │                │
     │ • Helm         │ └────────────────┘ └────────────────┘
     │ • ArgoCD       │
     │ • Prometheus   │         ┌────────────────┐
     │ • Grafana      │         │   vCenter/ESXi │
     │ • vSphere CSI  │────────▶│  (CSI Storage) │
     └────────────────┘         └────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **3+ Ubuntu VMs** (18.04 or 22.04) on VMware ESXi/vSphere
- **Ansible** installed on a controller machine
- **SSH access** to all VMs with the same user/password
- **Network connectivity** between all nodes

### Installation

```bash
# 1. Install Ansible
sudo apt update && sudo apt install ansible -y

# 2. Clone the repo
git clone https://github.com/jonny-levi/k8s.git
cd k8s

# 3. Configure your inventory
cp inventory/hosts.yaml.example inventory/hosts.yaml
nano inventory/hosts.yaml  # Add your node IPs and credentials

# 4. Configure variables
nano vars/all.yml  # Adjust versions, vCenter settings, etc.

# 5. Choose which components to deploy
nano inventory/components.yaml

# 6. Run the playbook
ansible-playbook site.yaml -i inventory/
```

## ⚙️ Configuration

### inventory/hosts.yaml

Define your cluster nodes:

```yaml
all:
  children:
    k8s_masters:
      hosts:
        master_node01:
          ansible_host: <MASTER_IP>
          ansible_ssh_user: <USERNAME>
          ansible_ssh_pass: <PASSWORD>
          ansible_sudo_pass: <PASSWORD>
    k8s_nodes:
      hosts:
        worker_node01:
          ansible_host: <WORKER_1_IP>
          # ...
        worker_node02:
          ansible_host: <WORKER_2_IP>
          # ...
```

### vars/all.yml

| Variable | Default | Description |
|----------|---------|-------------|
| `kubernetes_version` | `v1.34` | Kubernetes version |
| `containerd_lastest_version` | `2.1.4` | Containerd version |
| `runc_latest_version` | `v1.3.0` | Runc version |
| `cni_plugin_version` | `v1.7.1` | CNI plugins version |
| `container_runtime` | `unix:///run/containerd/containerd.sock` | CRI socket path |
| `join_token` | `v80n8z.wuep8jgbr7r0btnj` | Kubeadm join token |
| `vcenter_host` | — | vCenter IP address |
| `vcenter_user` | — | vCenter username |
| `vcenter_password` | — | vCenter password |
| `docker_registry_host` | `172.20.10.120` | Local Docker registry IP |
| `docker_registry_port` | `5000` | Local Docker registry port |

### inventory/components.yaml

Toggle which add-ons to deploy:

```yaml
argocd_deployment: true      # GitOps CD
grafana_deployment: true     # Dashboards
prometheus_deployment: true  # Monitoring
```

## ➕ Adding New Worker Nodes

To add new workers to an **existing** cluster without affecting current nodes, use the dedicated scale-up playbook:

```bash
# 1. Add new nodes to inventory/hosts.yaml under k8s_nodes:
#    worker_node03:
#      ansible_host: 172.20.10.33
#      ...
#    worker_node04:
#      ansible_host: 172.20.10.34
#      ...

# 2. Generate a fresh join token on the master
ssh jonathan@172.20.10.30 "kubeadm token create --print-join-command"

# 3. Update vars/all.yml with the new token

# 4. Run ONLY on new nodes using --limit
ansible-playbook site.yaml -i inventory/ --limit worker_node03,worker_node04

# 5. Verify
ssh jonathan@172.20.10.30 "kubectl get nodes"
```

> **⚠️ Important:** The `--limit` flag ensures Ansible only runs on the new nodes, leaving your existing cluster untouched. The master role tasks use `kubeadm init` which would fail on an already-initialized master anyway, but `--limit` to worker nodes is the clean approach.

### Alternative: Dedicated Add-Node Playbook

For a safer approach, create `add-workers.yaml`:

```yaml
---
# add-workers.yaml — Add new worker nodes to existing cluster
# Usage: ansible-playbook add-workers.yaml -i inventory/ --limit worker_node03,worker_node04

- hosts: k8s_nodes
  gather_facts: true
  become: true
  pre_tasks:
    - name: Load variables
      ansible.builtin.include_vars: vars/all.yml
    - name: System preparation
      ansible.builtin.include_tasks: tasks/system_prepare.yml

- hosts: k8s_nodes
  gather_facts: true
  become: true
  pre_tasks:
    - name: Load variables
      ansible.builtin.include_vars: vars/all.yml
  roles:
    - { role: k8s/k8s_nodes }
```

Then run:
```bash
ansible-playbook add-workers.yaml -i inventory/ --limit worker_node03,worker_node04
```

## 📁 Project Structure

```
k8s/
├── site.yaml                           # Main playbook (full cluster setup)
├── inventory/
│   ├── hosts.yaml                      # Node inventory (IPs, credentials)
│   └── components.yaml                 # Toggle add-on deployments
├── vars/
│   └── all.yml                         # Global variables (versions, vCenter)
├── tasks/
│   ├── system_prepare.yml              # OS prep (hostname, packages, containerd)
│   ├── vSphere-CSI.yml                 # vSphere CSI storage driver setup
│   ├── argoCD-deployment.yml           # ArgoCD via Helm
│   ├── grafana-deployment.yml          # Grafana deployment
│   └── prometheus-deployment.yml       # Prometheus deployment
└── roles/
    └── k8s/
        ├── k8s_masters/
        │   ├── tasks/main.yaml         # kubeadm init, Helm, CNI
        │   └── vsphere-csi/            # CSI config files
        └── k8s_nodes/
            └── tasks/main.yaml         # kubeadm join
```

## 🔄 Playbook Flow

```
site.yaml
  │
  ├─ 1. ALL NODES (masters + workers)
  │     └─ system_prepare.yml
  │        ├─ Set hostname
  │        ├─ Update packages
  │        ├─ Install containerd + runc + CNI
  │        ├─ Disable swap
  │        ├─ Configure iptables
  │        └─ Install kubeadm, kubelet, kubectl
  │
  ├─ 2. MASTERS ONLY
  │     └─ k8s_masters role
  │        ├─ kubeadm init
  │        ├─ Setup kubeconfig
  │        ├─ Install Helm
  │        └─ Deploy Weave CNI
  │
  ├─ 3. WORKERS ONLY
  │     └─ k8s_nodes role
  │        └─ kubeadm join
  │
  ├─ 4. MASTERS — vSphere CSI
  │     └─ vSphere-CSI.yml
  │        ├─ Storage class
  │        ├─ Cloud controller
  │        └─ CSI driver
  │
  └─ 5. MASTERS — Add-ons
        ├─ ArgoCD (Helm)
        ├─ Grafana
        └─ Prometheus
```

## 🔧 Improvement Suggestions

> No code changes have been made — these are optional enhancements.

- [ ] **Remove credentials from inventory** — Use Ansible Vault (`ansible-vault encrypt`) or environment variables instead of plaintext passwords
- [ ] **Make master role idempotent** — Add `when` conditions to skip `kubeadm init` if cluster already exists
- [ ] **Add the `add-workers.yaml` playbook** — Dedicated playbook for scaling (see above)
- [ ] **Replace Weave with Calico** — Weave is deprecated; Calico or Cilium are better choices
- [ ] **Add health checks** — Post-deployment verification tasks (node Ready, pods Running)
- [ ] **Add rollback capability** — `kubeadm reset` playbook for tearing down nodes
- [ ] **Pin Helm chart versions** — ArgoCD and other Helm deployments should lock versions
- [ ] **Add `hosts.yaml.example`** — Template with placeholder values for safe sharing
- [ ] **Support multi-master HA** — Add etcd clustering and load balancer for API server
- [ ] **Add Ansible tags** — Allow selective execution (`--tags containerd,k8s`)

## 📄 License

MIT

---

<div align="center">

**Built with ❤️ by [Jonny Levi](https://github.com/jonny-levi)**

*From bare metal to production K8s — one playbook away ☸️*

</div>
