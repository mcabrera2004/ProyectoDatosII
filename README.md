# Proyecto de Recomendación de Viajes – Entorno de Desarrollo con Docker + Dev Containers

Este repositorio está preparado para trabajar 100% dentro de un entorno de desarrollo reproducible usando **Docker + VSCode Dev Containers**.

---

## ¿Cómo empezar?

### Requisitos:
- Docker instalado
- VSCode con la extensión **"Dev Containers"** instalada

---

### Primer inicio

Cloná este repositorio:
   ```bash
   git clone https://github.com/mcabrera2004/viajes_recomendacion.git
   cd viajes_recomendacion

Montar la imagen de docker con:
   docker-compose build

EJECUCION: 

Luego para ejecutar:
   docker-compose up -d

LUEGO SE ABRE DEV CONTAINERS:

 "dev container reopen in container"

---

### ENV

Crear carpeta .env colocando 

MONGO_URI=mongodb+srv://equipo_viajes:[contraseña]@ingdatos.hzoisln.mongodb.net/viajes_recomendacion?retryWrites=true&w=majority

DB_NAME=viajes_recomendacion

### DASHBOARD Power BI:
