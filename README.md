# 🔐 Security Platform

Plataforma de análisis de dominios desarrollada con **FastAPI + Celery + Docker**, capaz de escanear múltiples objetivos de forma asíncrona y almacenar los resultados en una base de datos.

---

## 🚀 Características

* 🔍 Análisis de dominios (uno o varios)
* 🌐 Resolución DNS (IP)
* 📡 Análisis HTTP/HTTPS
* 🧠 Detección de tecnologías (nginx, apache…)
* 🔁 Detección de redirecciones
* 🔓 Escaneo de puertos comunes
* ⚡ Procesamiento asíncrono con Celery
* 🗄️ Persistencia en PostgreSQL
* 📚 Documentación automática con Swagger

---

## 🧱 Arquitectura

El proyecto está basado en microservicios usando Docker:

* **FastAPI** → API principal
* **Celery Worker** → procesamiento en segundo plano
* **Redis** → broker de tareas
* **PostgreSQL** → base de datos

---

## 📂 Estructura del proyecto

```
security-platform/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── db/
│   │   ├── models/
│   │   └── ...
│   │
│   ├── workers/
│   │   ├── tasks.py
│   │   └── celery_app.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── infra/
│   └── docker-compose.yml
│
└── README.md
```

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/security-platform.git
cd security-platform/infra
```

---

### 2. Levantar el entorno

```bash
docker-compose up --build
```

---

### 3. Acceder a la API

👉 http://localhost:8000/docs

---

## 🧪 Uso de la API

### 🔍 Analizar dominios

**POST /targets**

```json
{
  "domains": ["google.com", "github.com"]
}
```

---

### 📊 Ver resultados

**GET /results**

* Todos los resultados:

```
/results
```

* Filtrar por dominio:

```
/results?domain=google.com
```

---

## 🗄️ Acceso a la base de datos

Entrar al contenedor:

```bash
docker exec -it infra-db-1 bash
```

Conectarse a PostgreSQL:

```bash
psql -U user -d security_db
```

Consultar datos:

```sql
SELECT * FROM targets;
SELECT * FROM scan_results;
```

---

## ⚠️ Notas importantes

* Si modificas modelos (añadir columnas, etc), reconstruye con:

```bash
docker-compose down -v
docker-compose up --build
```

* Los resultados se procesan de forma asíncrona, pueden tardar unos segundos en aparecer.

---

## 🧠 Tecnologías utilizadas

* FastAPI
* Celery
* Redis
* PostgreSQL
* SQLAlchemy
* Docker / Docker Compose

---

## 📌 Futuras mejoras

* 🔐 Autenticación (JWT)
* 📈 Dashboard web (React/Vue)
* 🌍 Integración con APIs externas (Shodan, Whois…)
* ⚡ Escaneo más avanzado (nmap)
* 📊 Exportación de resultados (JSON / CSV)

---

## 👨‍💻 Autor

Desarrollado como proyecto de aprendizaje en ciberseguridad y backend.

---

## ⭐ Contribuciones

Si quieres mejorar el proyecto, ¡pull requests bienvenidas!

---
