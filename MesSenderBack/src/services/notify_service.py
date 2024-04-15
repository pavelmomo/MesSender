from src.schemas import MessageDTO






class NotifyService:
    sessions : dict[int, dict[int, list [MessageDTO]]] = dict()
    @staticmethod
    def register(user_id: int) -> int:
        session_id : int
        if (user_id not in NotifyService.sessions):
            session_id = 0
            NotifyService.sessions[user_id] = { session_id : list()}
        else:
            session_id = NotifyService._find_new_session_id(NotifyService.sessions[user_id])
            NotifyService.sessions[user_id][session_id] = list()
        return session_id

    @staticmethod
    def unregister(user_id: int, session_id: int):
        del NotifyService.sessions[user_id][session_id]
        if (len(NotifyService.sessions[user_id]) == 0):
            del NotifyService.sessions[user_id]

    @staticmethod
    def add_messages(user_ids: list[int], message: MessageDTO):
        for id in user_ids:
            for session in NotifyService.sessions[id]:
                NotifyService.sessions[id][session].append(message)


    @staticmethod
    def get_new_messages(user_id: int, session_id: int) -> (bool, list | None):
        if (len(NotifyService.sessions[user_id][session_id]) > 0):
            buf = NotifyService.sessions[user_id][session_id].copy()
            NotifyService.sessions[user_id][session_id].clear()
            return True, buf
        else:
            return False, None

    @staticmethod
    def _find_new_session_id(user_dict : dict[int, list[MessageDTO]]) -> int:
        for i in range(100):
            if i not in user_dict:
                return i
