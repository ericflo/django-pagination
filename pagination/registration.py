from django.conf import settings

default_pagination = getattr(settings, 'DEFAULT_PAGINATION', 20)

class PaginationRegistrar(object):
    _registry = {}
    
    def register(self, model, pagination=None):
        self._registry[model] = pagination or default_pagination
    
    def unregister(self, model):
        try:
            del self._registry[model]
        except KeyError:
            return
    
    def get_for_model(self, model):
        if model in self._registry:
            return self._registry[model]
        return None

def get_registry():
    registry = getattr(settings, '_pagination_registry', None)
    if registry is None:
        registry = PaginationRegistrar()
        setattr(settings, '_pagination_registry', registry)
    return registry