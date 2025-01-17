import os
import json
from enum import Enum
from typing import Dict, List, Optional
class Estados(Enum):
    PENDING = "Pendiente"
    IN_PROGRESS = "Realizando"
    COMPLETED = "Completada"
class ListManager:
    def __init__(self, ruta):
        self.ruta = ruta
        self._crear_archivo()

    def _crear_archivo(self) -> None:
        if not os.path.exists(self.ruta):
            with open(self.ruta, 'w', encoding='utf-8') as f:
                json.dump([], f)
    def _leer_tareas(self) -> List[Dict]:
        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _guardar_tareas(self, tareas: List[Dict]) -> None:
        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump(tareas, f, indent=4, ensure_ascii=False)

    def introducir_datos(self, id: int, item: str, status: str) -> None:
        try:
            status_enum = Estados(status)
        except ValueError:
            raise ValueError(f"Estado '{status}' no válido. Estados posibles: {[s.value for s in Estados]}")

        tareas = self._leer_tareas()

        nueva_tarea = {
            "id": id,
            "tarea": item,
            "status": status_enum.value
        }

        for i, tarea in enumerate(tareas):
            if tarea["id"] == id:
                tarea[i] = nueva_tarea
                break
        else:
            tareas.append(nueva_tarea)

        self._guardar_tareas(tareas)


    def obtener_tarea(self, id: int) -> Optional[Dict]:
        tareas = self._leer_tareas()

        for tarea in tareas:
            if tarea["id"] == id:
                return tarea

        return None

    def listar_tarea(self, status: Optional[str] = None) -> List[Dict]:
        tareas = self._leer_tareas()

        if status:
            try:
                status_enum = Estados(status)
                return [tarea for tarea in tareas if tarea["status"] == status_enum.value]
            except ValueError:
                raise ValueError(f"Estado '{status}' no válido. Estados posibles: {[s.value for s in Estados]}")

        return tareas

    def eliminar_tarea(self, id: int) -> bool:
        tareas = self._leer_tareas()
        init_length = len(tareas)

        tareas = [tarea for tarea in tareas if tarea["id"] != id]

        if len(tareas) < init_length:
            self._guardar_tareas(tareas)
            return True
        return False







