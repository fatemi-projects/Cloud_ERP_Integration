# Cloud-Native ERP Integration Platform

## 🧠 Project Overview

This project migrates an **on-premise Odoo ERP system to a cloud-based architecture on Azure**.  
It exposes ERP modules (Customers, Products, Orders) through **FastAPI REST APIs**, fully containerized using Docker and deployed on Azure VM.

It also includes **JWT authentication**, **logging layer**, and **CI/CD pipeline using Jenkins**.

---

## 🚀 Architecture

- Odoo ERP (Docker container)
- PostgreSQL Database
- FastAPI backend (REST APIs)
- Azure VM deployment
- Jenkins CI/CD pipeline
- JWT authentication layer

---

## 📁 Project Structure



---

## ⚙️ Features

### 🔹 Backend
- FastAPI REST APIs
- Odoo XML-RPC integration
- Modular service structure

### 🔹 ERP Modules
- Customers (CRUD)
- Products (CRUD)
- Orders (CRUD)

### 🔹 Security
- JWT authentication
- Protected API endpoints

### 🔹 DevOps
- Docker containerization
- Azure VM deployment
- Jenkins CI/CD pipeline

### 🔹 Logging
- Centralized logging layer for debugging and monitoring

---

## 🔐 Authentication

1. Call login endpoint:
```http
POST /login