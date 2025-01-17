#!/usr/bin/env python3
import argparse
from modules import ListManager, Estados

def setup_parser():
    """Configura el parser de argumentos con todos los subcomandos."""
    parser = argparse.ArgumentParser(
        description="Gestor de tareas por línea de comandos",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponibles")
    subparsers.required = True

    # Comando: añadir
    add_parser = subparsers.add_parser("añadir", help="Añade una nueva tarea")
    add_parser.add_argument("--id", type=int, required=True, help="ID único de la tarea")
    add_parser.add_argument("--tarea", type=str, required=True, help="Descripción de la tarea")
    add_parser.add_argument(
        "--status",
        type=str,
        required=True,
        choices=[status.value for status in Estados],
        help="Estado de la tarea"
    )

    # Comando: listar
    list_parser = subparsers.add_parser("listar", help="Lista las tareas")
    list_parser.add_argument(
        "--status",
        type=str,
        choices=[status.value for status in Estados],
        help="Filtrar por estado (opcional)"
    )

    # Comando: obtener
    get_parser = subparsers.add_parser("obtener", help="Obtiene una tarea específica")
    get_parser.add_argument("--id", type=int, required=True, help="ID de la tarea a obtener")

    # Comando: eliminar
    delete_parser = subparsers.add_parser("eliminar", help="Elimina una tarea")
    delete_parser.add_argument("--id", type=int, required=True, help="ID de la tarea a eliminar")

    return parser

def format_task(task):
    """Formatea una tarea para mostrarla en la consola."""
    return f"ID: {task['id']:<5} | Tarea: {task['tarea']:<30} | Estado: {task['status']}"

def main():
    parser = setup_parser()
    args = parser.parse_args()

    # Inicializar el gestor de tareas
    manager = ListManager("tareas.json")

    try:
        # Procesar comandos
        if args.comando == "añadir":
            manager.introducir_datos(args.id, args.tarea, args.status)
            print(f"Tarea {args.id} añadida correctamente")

        elif args.comando == "listar":
            tareas = manager.listar_tarea(args.status)
            if not tareas:
                print("No hay tareas para mostrar")
            else:
                print("\nLista de tareas:")
                print("-" * 60)
                for tarea in tareas:
                    print(format_task(tarea))
                print("-" * 60)
                print(f"Total: {len(tareas)} tareas")

        elif args.comando == "obtener":
            tarea = manager.obtener_tarea(args.id)
            if tarea:
                print("\nDetalles de la tarea:")
                print("-" * 60)
                print(format_task(tarea))
                print("-" * 60)
            else:
                print(f"No se encontró la tarea con ID {args.id}")

        elif args.comando == "eliminar":
            if manager.eliminar_tarea(args.id):
                print(f"Tarea {args.id} eliminada correctamente")
            else:
                print(f"No se encontró la tarea con ID {args.id}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()