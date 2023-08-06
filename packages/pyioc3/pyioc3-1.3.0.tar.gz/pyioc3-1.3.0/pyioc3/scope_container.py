from .bound_member import BoundMember
from .interface import Scope
from .scope_enum import ScopeEnum

class PersistentScope(Scope):

    def __init__(self):
        self._cache = {}

    def __contains__(self, annotation) -> bool:
        return annotation in self._cache.keys()

    def add(self, annotation, instance) -> None:
        self._cache[annotation] = instance

    def use(self, annotation) -> object:
        return self._cache[annotation]


class TransientScope(Scope):

    def __init__(self):
        self._cache = {}

    def __contains__(self, annotation) -> bool:
        return annotation in self._cache.keys()

    def add(self, annotation, instance) -> None:
        if annotation in self:
            self._cache[annotation].append(instance)
        else:
            self._cache[annotation] = [instance]

    def use(self, annotation) -> object:
        inst = self._cache[annotation].pop()
        if len(self._cache[annotation]) == 0:
            del self._cache[annotation]
        return inst


class ScopeContainer:

    def __init__(self, singleton: Scope):
        self._scopes = {
            ScopeEnum.SINGLETON: singleton,
            ScopeEnum.REQUESTED: PersistentScope(),
            ScopeEnum.TRANSIENT: TransientScope()}

    def _create_instance(self, member: BoundMember) -> object:
        args = list()
        for dep in member:
            args.append(self.get_instance_of(dep))
        return member.on_activate(member.implementation(*args))

    def _get_scope(self, member: BoundMember):
        return self._scopes[member.scope]

    def has(self, member: BoundMember) -> bool:
        return member.annotation in self._get_scope(member)

    def add(self, member: BoundMember):
        self._get_scope(member).add(member.annotation, self._create_instance(member))

    def get_instance_of(self, member: BoundMember) -> object:
        return self._get_scope(member).use(member.annotation)
