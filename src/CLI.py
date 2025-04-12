import os
from BBDD import obtener_base_datos
from crud_operations import insertar_destino, obtener_destinos, actualizar_destino, eliminar_destino, insertar_varios_destinos, eliminar_todos_los_destinos
from bson import ObjectId

db = obtener_base_datos()
coleccion = db["testeo"]

def main():
    while True:
        print("Menú CLI:")
        print("1. Listar destinos")
        print("2. Crear destino")
        print("3. Actualizar Destino")
        print("4. Eliminar destino")
        print("5. Insertar destinos con Faker")
        print("6. Eliminar todos los destinos")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            aplicar_filtros = input("¿Desea aplicar filtros? (si/no): ").strip().lower()
            filtros = {}
            if aplicar_filtros == "si":
                nombre = input("Filtrar por nombre (dejar vacío para omitir): ").strip()
                if nombre:
                    filtros["nombre"] = nombre
                pais = input("Filtrar por país (dejar vacío para omitir): ").strip()
                if pais:
                    filtros["pais"] = pais
                clima = input("Filtrar por clima (dejar vacío para omitir): ").strip()
                if clima:
                    filtros["clima"] = clima
                actividades = input("Filtrar por actividades (separadas por comas, dejar vacío para omitir): ").strip()
                if actividades:
                    filtros["actividades"] = actividades
                costo = input("Filtrar por costo_promedio (dejar vacío para omitir): ").strip()
                if costo:
                    filtros["costo_promedio"] = costo
                puntuacion = input("Filtrar por puntuacion (dejar vacío para omitir): ").strip()
                if puntuacion:
                    filtros["puntuacion"] = puntuacion
            
            try:
                destinos = obtener_destinos(filtros)
                if not destinos:
                    print("No se encontraron destinos con los filtros especificados.")
                for destino in destinos:
                    print(destino)
            except Exception as e:
                print("Error al obtener destinos:", e)
                
        elif opcion == "2":
            destino = {}
            destino["nombre"] = input("Ingrese nombre: ")
            destino["pais"] = input("Ingrese país: ")
            destino["clima"] = input("Ingrese clima: ")
            actividades = input("Ingrese actividades (separadas por comas): ")
            destino["actividades"] = [act.strip() for act in actividades.split(',')]
            while True:
                try:
                    costo = int(input("Ingrese costo promedio: "))
                    if costo < 0:
                        print("El costo promedio no puede ser negativo. Inténtelo nuevamente.")
                        continue
                    destino["costo_promedio"] = costo
                    break
                except ValueError:
                    print("Costo promedio inválido, ingrese un número entero.")
            while True:
                try:
                    puntuacion = int(input("Ingrese puntuación (1-5): "))
                    if puntuacion < 1 or puntuacion > 5:
                        print("La puntuación debe estar entre 1 y 5. Inténtelo nuevamente.")
                        continue
                    destino["puntuacion"] = puntuacion
                    break
                except ValueError:
                    print("Puntuación inválida, ingrese un número entero.")
    
            try:
                insertar_destino(destino)
                print("Destino creado exitosamente.")
            except Exception as e:
                print("Error al insertar destino:", e)
            
    
        elif opcion == "3":
            print("Actualizar destino")
            id_destino = input("Ingrese el ID del destino a actualizar: ").strip()
            try:
                filtro = {"_id": ObjectId(id_destino)}
            except Exception as e:
                print("ID inválido.")
                continue

            nuevos_valores = {}
            nuevo_nombre = input("Nuevo nombre (dejar vacío para omitir): ").strip()
            if nuevo_nombre:
                nuevos_valores["nombre"] = nuevo_nombre
            nuevo_pais = input("Nuevo país (dejar vacío para omitir): ").strip()
            if nuevo_pais:
                nuevos_valores["pais"] = nuevo_pais
            nuevo_clima = input("Nuevo clima (dejar vacío para omitir): ").strip()
            if nuevo_clima:
                nuevos_valores["clima"] = nuevo_clima
            nuevas_actividades = input("Nuevas actividades (separadas por comas, dejar vacío para omitir): ").strip()
            if nuevas_actividades:
                nuevos_valores["actividades"] = [act.strip() for act in nuevas_actividades.split(',')]
            
            nuevo_costo = input("Nuevo costo promedio (dejar vacío para omitir): ").strip()
            if nuevo_costo:
                try:
                    costo = int(nuevo_costo)
                    if costo < 0:
                        print("El costo promedio no puede ser negativo. No se actualizará este campo.")
                    else:
                        nuevos_valores["costo_promedio"] = costo
                except ValueError:
                    print("Costo promedio inválido. No se actualizará este campo.")
            
            nueva_puntuacion = input("Nueva puntuación (1-5, dejar vacío para omitir): ").strip()
            if nueva_puntuacion:
                try:
                    puntuacion = int(nueva_puntuacion)
                    if puntuacion < 1 or puntuacion > 5:
                        print("La puntuación debe estar entre 1 y 5. No se actualizará este campo.")
                    else:
                        nuevos_valores["puntuacion"] = puntuacion
                except ValueError:
                    print("Puntuación inválida. No se actualizará este campo.")
            
            if not nuevos_valores:
                print("No se proporcionaron nuevos valores para actualizar.")
                continue
            try:
                resultado = actualizar_destino(filtro, nuevos_valores)
                print(f"Destino actualizado. Registros modificados: {resultado.modified_count}")
            except Exception as e:
                print("Error al actualizar destino:", e)
        elif opcion == "4":
            print("Eliminar destino")
            id_destino = input("Ingrese el ID del destino a eliminar: ").strip()
            try:
                filtro = {"_id": ObjectId(id_destino)}
            except Exception as e:
                print("ID inválido:", e)
                continue
            try:
                resultado = eliminar_destino(filtro)
                print(f"Destino eliminado. Registros eliminados: {resultado.deleted_count}")
            except Exception as e:
                print("Error al eliminar destino:", e)
        elif opcion == "5":
            while True:
                try:
                    valor = int(input("¿Cuántos destinos desea insertar? (número entero). Máximo 20: "))
                    if valor <=0:
                        print("El número de destinos a insertar debe ser mayor que 0.")
                        continue
                    break
                except ValueError:
                    print("Valor inválido, ingrese un número entero.")
            if valor > 20:
                valor = 20
            insertar_varios_destinos(valor)
            print("Datos insertados correctamente.")

        elif opcion == "6":
            confirmacion = input("¿Está seguro de que desea eliminar todos los destinos? (si/no): ").strip().lower()
            if confirmacion == "si":
                try:
                    eliminar_todos_los_destinos()
                    print("Todos los destinos han sido eliminados correctamente.")
                except Exception as e:
                    print("Error al eliminar todos los destinos:", e)
            else:
                print("Operación cancelada.")
        elif opcion == "7":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:       
            print("Opción no reconocida.")

if __name__ == '__main__':
    main()