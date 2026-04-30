import requests
import sys

BASE_URL = "http://localhost:5000"

def menu_principal():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Ver tareas")
        print("4. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar()
        elif opcion == "2":
            login()
        elif opcion == "3":
            ver_tareas()
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida")

def registrar():
    print("\n--- REGISTRO ---")
    usuario = input("Usuario: ").strip()
    contraseña = input("Contraseña: ").strip()

    try:
        r = requests.post(f"{BASE_URL}/registro", json={"usuario": usuario, "contraseña": contraseña})
        if r.status_code == 201:
            print(f"✅ {r.json()['mensaje']}")
        else:
            print(f"❌ Error: {r.json().get('error', 'Error desconocido')}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")

def login():
    print("\n--- INICIO DE SESIÓN ---")
    usuario = input("Usuario: ").strip()
    contraseña = input("Contraseña: ").strip()

    try:
        r = requests.post(f"{BASE_URL}/login", json={"usuario": usuario, "contraseña": contraseña})
        if r.status_code == 200:
            data = r.json()
            print(f"✅ {data['mensaje']}")
            menu_usuario(data.get("usuario_id"), usuario)
        else:
            print(f"❌ Error: {r.json().get('error', 'Error desconocido')}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")

def menu_usuario(usuario_id, nombre_usuario):
    while True:
        print(f"\n=== MENÚ DE {nombre_usuario.upper()} ===")
        print("1. Ver mis tareas")
        print("2. Crear tarea")
        print("3. Completar tarea")
        print("4. Eliminar tarea")
        print("5. Cerrar sesión")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            listar_tareas(usuario_id)
        elif opcion == "2":
            crear_tarea(usuario_id)
        elif opcion == "3":
            completar_tarea(usuario_id)
        elif opcion == "4":
            eliminar_tarea(usuario_id)
        elif opcion == "5":
            break
        else:
            print("Opción inválida")

def ver_tareas():
    usuario_id = input("Ingrese su ID de usuario: ").strip()
    if not usuario_id.isdigit():
        print("❌ ID inválido")
        return
    
    try:
        r = requests.get(f"{BASE_URL}/tareas/{usuario_id}")
        if r.status_code == 200:
            tareas = r.json().get("tareas", [])
            if tareas:
                print("\n--- TAREAS ---")
                for t in tareas:
                    estado = "✅" if t["completada"] else "⭕"
                    print(f"{t['id']}. {estado} {t['titulo']} - {t.get('descripcion', 'Sin descripción')}")
            else:
                print("No hay tareas")
        else:
            print(f"❌ Error: {r.json().get('error', 'Error')}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")

def listar_tareas(usuario_id):
    try:
        r = requests.get(f"{BASE_URL}/tareas/{usuario_id}")
        if r.status_code == 200:
            tareas = r.json().get("tareas", [])
            if tareas:
                print("\n--- TAREAS ---")
                for t in tareas:
                    estado = "✅" if t["completada"] else "⭕"
                    print(f"{t['id']}. {estado} {t['titulo']} - {t.get('descripcion', 'Sin descripción')}")
            else:
                print("No hay tareas")
        else:
            print(f"❌ Error: {r.json().get('error', 'Error')}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")

def crear_tarea(usuario_id):
    titulo = input("Título: ").strip()
    descripcion = input("Descripción: ").strip()
    try:
        r = requests.post(f"{BASE_URL}/tareas", json={
            "usuario_id": usuario_id,
            "titulo": titulo,
            "descripcion": descripcion
        })
        if r.status_code == 201:
            print(f"✅ Tarea creada")
        else:
            print(f"❌ Error: {r.json().get('error', 'Error')}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")

def completar_tarea(usuario_id):
    tarea_id = input("ID de tarea: ").strip()
    try:
        r = requests.put(f"{BASE_URL}/tareas/{tarea_id}", json={"usuario_id": usuario_id})
        if r.status_code == 200:
            print(f"✅ Tarea completada")
        else:
            print(f"❌ Error: {r.json().get('error', 'Error')}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")

def eliminar_tarea(usuario_id):
    tarea_id = input("ID de tarea: ").strip()
    try:
        r = requests.delete(f"{BASE_URL}/tareas/{tarea_id}?usuario_id={usuario_id}")
        if r.status_code == 200:
            print(f"✅ Tarea eliminada")
        else:
            print(f"❌ Error: {r.json().get('error', 'Error')}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")

if __name__ == "__main__":
    print("=== CLIENTE DE GESTIÓN DE TAREAS ===")
    menu_principal()