# Sistema de Gestión de Tareas con API REST

**PFO - Redes**

---

## 1. Descripción del Proyecto

Este proyecto implementa un sistema de gestión de tareas mediante una API REST desarrollada en Flask (Python), con persistencia de datos en SQLite y autenticación de usuarios mediante contraseñas hasheadas.

La aplicación permite:
- Registrar nuevos usuarios
- Iniciar sesión con autenticación segura
- Crear, listar, completar y eliminar tareas
- Interactuar tanto por interfaz web como por consola

---

## 2. Requisitos del Sistema

- Python 3.8 o superior
- Sistema operativo: Linux, macOS o Windows

---

## Capturas
![Servidor](/PFO2-Redes/images/servidor.png.png)
![Cliente](/PFO2-Redes/images/cliente.png)
![ServidorWeb](/PFO2-Redes/images/servidorweb.png)
![Base de Datos](/PFO2-Redes/images/bd.png)

---


## 3. Instalación

### 3.1. Clonar el repositorio (si corresponde)
```bash
git clone <https://github.com/SchallmoserJuan/PFO2-Redes>
cd <carpeta-del-proyecto>
```

### 3.2. Crear entorno virtual
```bash
python3 -m venv venv
```

### 3.3. Activar el entorno virtual

**Linux / macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3.4. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 4. Ejecución

### 4.1. Iniciar el servidor
```bash
python servidor.py
```

El servidor estará disponible en: `http://localhost:5000`

### 4.2. Acceder a la aplicación

- **Interfaz web:** http://localhost:5000/tareas
- **Cliente por consola:** En otra terminal ejecutar `python cliente.py`

---

## 5. Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/registro` | Registrar nuevo usuario |
| POST | `/login` | Iniciar sesión |
| GET | `/tareas` | Página de bienvenida (HTML) |
| GET | `/tareas/<id>` | Listar tareas de un usuario |
| POST | `/tareas` | Crear nueva tarea |
| PUT | `/tareas/<id>` | Completar una tarea |
| DELETE | `/tareas/<id>` | Eliminar una tarea |

---

## 6. Pruebas con curl

### Registro de usuario nuevo
```bash
curl -X POST http://localhost:5000/registro \
  -H "Content-Type: application/json" \
  -d '{"usuario": "juan", "contraseña": "123456"}'
```
**Respuesta:** `201 Created`

---

### Registro con usuario existente
```bash
curl -X POST http://localhost:5000/registro \
  -H "Content-Type: application/json" \
  -d '{"usuario": "juan", "contraseña": "123456"}'
```
**Respuesta:** `409 Conflict`

---

### Inicio de sesión exitoso
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"usuario": "juan", "contraseña": "123456"}'
```
**Respuesta:** `200 OK` → `{"mensaje": "Login exitoso", "usuario_id": 1}`

---

### Inicio de sesión con contraseña incorrecta
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"usuario": "juan", "contraseña": "incorrecta"}'
```
**Respuesta:** `401 Unauthorized`

---

### Listar tareas de un usuario
```bash
curl http://localhost:5000/tareas/1
```
**Respuesta:** `200 OK` → JSON con lista de tareas

---

### Crear una tarea
```bash
curl -X POST http://localhost:5000/tareas \
  -H "Content-Type: application/json" \
  -d '{"usuario_id": 1, "titulo": "Hacer TP", "descripcion": "Redes"}'
```
**Respuesta:** `201 Created`

---

### Completar una tarea
```bash
curl -X PUT http://localhost:5000/tareas/1 \
  -H "Content-Type: application/json" \
  -d '{"usuario_id": 1}'
```
**Respuesta:** `200 OK`

---

### Eliminar una tarea
```bash
curl -X DELETE "http://localhost:5000/tareas/1?usuario_id=1"
```
**Respuesta:** `200 OK`

---

## 7. Respuestas a Preguntas Conceptuales

### ¿Por qué es necesario hashear las contraseñas?

El hasheo de contraseñas es una práctica fundamental de seguridad. Cuando un usuario crea una cuenta, su contraseña no se almacena en texto plano, sino que se transforma mediante una función unidireccional (en este caso, bcrypt). 

Si la base de datos fuera comprometida, un atacante solo accedería a los hashes, no a las contraseñas reales. Además, bcrypt incluye un "salt" automático que protege contra ataques de tablas rainbow, haciendo que cada hash sea único incluso si dos usuarios tienen la misma contraseña.

---

### ¿Cuáles son las ventajas de utilizar SQLite?

1. **Sin servidor externo**: No requiere instalar MySQL, PostgreSQL u otro sistema de gestión de bases de datos. Todo está contenido en una biblioteca de Python.

2. **Portabilidad**: La base de datos se guarda en un solo archivo (`.db`), facilitando su traslado, respaldo y distribución.

3. **Simplicidad de configuración**: Ideal para proyectos pequeños, prototipos y trabajos prácticos donde el volumen de datos es moderado.

4. **Integración nativa**: Python incluye soporte para SQLite en su librería estándar (`sqlite3`), sin necesidad de configuraciones adicionales.

---

## 8. Estructura de Archivos

```
├── servidor.py          # API REST con Flask
├── cliente.py           # Cliente interactivo por consola
├── requirements.txt     # Dependencias del proyecto
├── tareas.db            # Base de datos SQLite (se crea automáticamente)
├── templates/
│   └── index.html       # Interfaz web
└── README.md            # Este archivo
```

---

Práctica formativa obligatoria - Programación sobre Redes