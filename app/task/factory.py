from app.task.save_players import SavePlayers
from app.task.server_message import ServerMessage

class TasksFactory:
    @staticmethod
    def create(task):
        if task.kind == "server_messages":
            return ServerMessage(task.interval, task.data)
        elif task.kind == "save_players":
            return SavePlayers(task.interval, task.data)
        else:
            raise ValueError(f"Tipo de processo não suportado: {task.kind}")
