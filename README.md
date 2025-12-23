# Garrett Carroll
## DevOps / Cloud Engineer

**Location:** Alvarado, Texas  
**Phone:** 817-350-1085  
**Email:** carrolgarrett55@gmail.com  
*(Ask me for my GitHub and other contact info through text or email)*

---

## Professional Summary

A pragmatic engineer specializing in building and automating the full lifecycle of cloud-native applications. My expertise lies in translating source code into **reliable, scalable, and secure systems** through **Infrastructure as Code (IaC)**, **CI/CD pipelines**, and **container orchestration**.

I build the **automated factories** that allow development teams to ship software with speed and confidence.

---

## Core Technical Skills

- **Cloud Infrastructure:** AWS (EKS, ECR, VPC, IAM), Infrastructure as Code (IaC)
- **Containerization & Orchestration:** Docker, Kubernetes (K8s), Container Registries
- **CI/CD Automation:** GitHub Actions, YAML Workflow Configuration, Automated Testing & Deployment
- **Languages & Frameworks:** Python, FastAPI
- **Tools & Technologies:** Terraform, Git, Linux, Flake8, API Security

---

## Key Project Experience

### End-to-End CI/CD Pipeline for a Cloud-Native Python API

Designed and built a complete, automated system for deploying a **secure, containerized FastAPI application** to the AWS cloud. The entire infrastructure and deployment process is **codified**, requiring **zero manual intervention** from code push to live deployment.

#### Infrastructure as Code (Terraform)
- Authored **Terraform modules** to provision all necessary AWS infrastructure, including an **ECR container repository** and a **managed EKS Kubernetes cluster**.
- Ensured the infrastructure is defined as a **repeatable, version-controlled blueprint**, eliminating environment drift and enabling rapid replication.

#### Containerization (Docker)
- Wrote a **multi-stage Dockerfile** to create a lightweight, production-ready container image for the Python application, optimizing for size and security.

#### Deployment Orchestration (Kubernetes)
- Developed **Kubernetes manifests** (Deployment, Service, Secret) to manage the application's runtime state.
- Implemented a **high-availability architecture** by deploying three replicas behind a Load Balancer Service, ensuring resilience and scalability.
- Managed application secrets correctly by injecting an API token as an **environment variable from a K8s Secret**, avoiding insecure hardcoding.

#### Continuous Integration & Deployment (GitHub Actions)
- Constructed a **CI/CD workflow in GitHub Actions** that automatically triggers on every push to the main branch.
- The pipeline performs:
  - Automated **code linting**
  - **Docker image build**
  - Push to **ECR**
  - Triggers a **rolling deployment** to the EKS cluster with **zero downtime**

---

## Education & Certifications

*(Add any relevant degrees, certifications like AWS Certified DevOps Engineer, or coursework here. If you are self-taught, it is perfectly acceptable to remove this section.)*

---

## Additional Information

I thrive in environments where **automation**, **repeatability**, and **reliability** are paramount. My goal is to empower engineering teams to focus on building great products while I ensure the underlying systems are rock-solid and deployment-ready at all times.
