from django.contrib.sessions.backends.db import SessionStore as DbSessionStore

class SessionStore(DbSessionStore):
    def cycle_key(self):
        data = self._session
        key = self.session_key
        self.create()
        self._session_cache = data
        if key:
            ...  # здесь пишем логику
            self.delete(key)