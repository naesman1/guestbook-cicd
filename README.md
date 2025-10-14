# 🧩 Documentación del Pipeline CI/CD: Implementación GitOps con ArgoCD

El presente proyecto establece un flujo integral de **Integración Continua (CI)** y **Despliegue Continuo (CD)** para una aplicación *Guestbook* desarrollada en **Python/Flask**.  
Se adopta la metodología **GitOps** mediante el uso de **ArgoCD** para la sincronización automática del estado del clúster de Kubernetes (K8s) con la configuración declarativa contenida en un repositorio de manifiestos dedicado.

---

## 🗂️ 1. Estructura del Proyecto y Repositorios (Entregable 1)

La arquitectura de la solución se fundamenta en la separación de responsabilidades mediante la utilización de **dos repositorios distintos**:

### 📘 Repositorio de Código Fuente (`guestbook-cicd`)
Contiene el código Python, el sistema de gestión de dependencias (`requirements.txt`), las unidades de prueba y el `Dockerfile`.

🔗 **URL:** [https://github.com/naesman1/guestbook-cicd.git](https://github.com/naesman1/guestbook-cicd.git)

---

### 🧾 Repositorio de Manifiestos (GitOps - `guestbook-k8s-config`)
Constituye el repositorio declarativo de los manifiestos de Kubernetes (`frontend-deployment.yaml`, `redis-service.yaml`, etc.).  
Este repositorio es la **Fuente de Verdad (Source of Truth)**, siendo objeto de monitorización constante por parte de **ArgoCD**.

🔗 **URL:** [https://github.com/naesman1/guestbook-k8s-config.git](https://github.com/naesman1/guestbook-k8s-config.git)

---

### 🐳 Repositorio de Artefactos (Docker Hub - Entregable 2)
Es el registro donde se almacenan las imágenes Docker generadas durante la fase de Despliegue Continuo.

🔗 **URL:** [https://hub.docker.com/r/naesman1/guestbook-frontend](https://hub.docker.com/r/naesman1/guestbook-frontend)

---

## ⚙️ 2. Flujo de Trabajo y Pipeline de CI/CD (Entregable 3)

La orquestación del proceso CI/CD se realiza mediante **GitHub Actions**, aplicando la estrategia de ramificación **Git Flow** para la gestión del ciclo de vida del código.

---

### 🔀 2.1. Descripción de la Lógica Git Flow

| Rama | Flujo | Resultado |
|------|--------|------------|
| `develop` | Push / Pull Request | Ejecución exclusiva del pipeline de CI. Su propósito es validar la calidad del código, mitigando riesgos en producción. |
| `main` | Merge desde develop | Ejecución del pipeline integral de CI/CD. El despliegue se realiza solo si las validaciones de CI son exitosas. |

---

### 🧩 2.2. Etapas del Pipeline (`.github/workflows/ci-cd.yml`)

| Etapa (Job) | Descripción y Requisitos Cubiertos |
|--------------|------------------------------------|
| **ci (Integración Continua)** | Se ejecuta en las ramas `main`, `develop` y en eventos `pull_request`. Abarca: Tests unitarios, Informe de Cobertura, Linting (Flake8), Análisis Estático (SonarCloud) y Vulnerabilidades (Snyk). |
| **deploy (Despliegue Continuo)** | Activación condicionada a la rama `main`. Incluye: Construcción de Imagen Docker, Publicación en Docker Hub y actualización del manifiesto en el repositorio GitOps. |

---

### 📡 2.3. Ejecución y Monitorización del Workflow

- **Ejecución de CI (Desarrollo):**  
  Un `git push` a la rama `develop` inicia la ejecución del pipeline de CI.  
  Se puede monitorear desde la pestaña **Actions** en GitHub para verificar la finalización del job `ci`.

- **Ejecución de CD (Despliegue):**  
  Se activa al fusionar `develop` → `main` y hacer `git push origin main`.  
  Luego del job `deploy`, verificar en **ArgoCD** que la app `guestbook-app` transite los estados:  
  `Synced → Progressing → Healthy`.

---

## ☸️ 3. Prerrequisitos y Despliegue en K8s Local (Entregables 5, 6, 7)

### ⚙️ 3.1. Configuración de ArgoCD

**Instalación de ArgoCD:**
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

**Obtención de la Contraseña Inicial:**
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

**Creación de la Aplicación GitOps (Manifiestos de Kubernetes):**

- **Destination Server:** `https://kubernetes.default.svc`  
- **Repository URL:** [https://github.com/naesman1/guestbook-k8s-config.git](https://github.com/naesman1/guestbook-k8s-config.git)  
- **Path:** `k8s`

---

### 🌐 3.2. Acceso a la Aplicación Desplegada

**Ejecución del Túnel:**
```bash
kubectl port-forward svc/guestbook-frontend 8088:5000
```

**Acceso Web:**  
👉 [http://localhost:8088](http://localhost:8088)

---

## 🧹 4. Apagar o Eliminar la Aplicación

### ✅ 4.1. Remoción Mediante GitOps (Procedimiento Recomendado)

1. Acceder a la interfaz de **ArgoCD**.  
2. Seleccionar la aplicación `guestbook-app`.  
3. Pulsar la opción **DELETE (Eliminar)**.  

**Resultado:** ArgoCD elimina todos los recursos asociados (Deployments, Services, etc.), manteniendo la coherencia del estado del clúster.

---

### 🧨 4.2. Terminación del Clúster Local

**Con Kind:**
```bash
kind delete cluster --name kind
```

**Con Docker Desktop K8s:**
> Ir a `Settings > Kubernetes` y seleccionar **Reset Kubernetes Cluster**.

---

## 📋 5. Resumen y Listado de Entregables

| # | Entregable | Estado | Enlace / Ubicación |
|---|-------------|---------|--------------------|
| 1 | Enlace al Repositorio de Código | ✅ Completado | [https://github.com/naesman1/guestbook-cicd.git](https://github.com/naesman1/guestbook-cicd.git) |
| 2 | Repositorio de Artefactos (Docker Hub) | ✅ Completado | [https://hub.docker.com/r/naesman1/guestbook-frontend](https://hub.docker.com/r/naesman1/guestbook-frontend) |
| 3 | Fichero de Configuración del Pipeline | ✅ Completado | `.github/workflows/ci-cd.yml` |
| 4 | Screenshots del Pipeline de CI/CD | ⏳ Pendiente | Pestaña **Actions** en GitHub |
| 5 | Manifiestos de Kubernetes | ✅ Completado | [https://github.com/naesman1/guestbook-k8s-config.git](https://github.com/naesman1/guestbook-k8s-config.git) |
| 6 | Enlace/Screenshot de la Aplicación Desplegada | ⏳ Pendiente | [http://localhost:8088](http://localhost:8088) |
| 7 | Enlace/Screenshot del Proyecto en ArgoCD | ⏳ Pendiente | [https://localhost:8080](https://localhost:8080) |
| 8 | Proyecto en SonarCloud | ⏳ Pendiente | `Tu URL de SonarCloud` |
| 9 | Proyecto en Snyk o GitGuardian | ⏳ Pendiente | `Tu URL de Snyk` o logs de GitHub Actions |
| 10 | Vídeo Explicativo en YouTube | ⏳ Pendiente | `Tu enlace de YouTube` |

---

📘 **Autor:** [@naesman1](https://github.com/naesman1)  
🕓 **Última actualización:** Octubre 2025  
🚀 **Stack:** Python · Flask · Docker · Kubernetes · ArgoCD · GitHub Actions · SonarCloud · Snyk
