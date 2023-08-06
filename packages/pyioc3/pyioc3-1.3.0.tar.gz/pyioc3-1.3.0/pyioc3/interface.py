from abc import ABC, abstractmethod
from typing import Callable, Dict, List

from .scope_enum import ScopeEnum
from .bound_member import BoundMember


class Scope(ABC):
    """An IOC Instance Scope"""

    @abstractmethod
    def __contains__(self, annotation: any) -> bool:
        """Check if the given annotation exists in this scope.

        Arguments:
         annotation: The str or type var used to identify an instance.

        Returns:
         True, if the annotation exists. Else, False.
        """
        raise NotImplementedError()

    @abstractmethod
    def add(self, annotation: any, instance: object) -> None:
        """Add a instance to this scope under the given annotation

        Arguments:
         annotation: The str or type var used to identify an instance.
         instance: Any value to store as the instance associated with the annotation.
        """
        raise NotImplementedError()

    @abstractmethod
    def use(self, annotation: any) -> object:
        """Get the instance associated with the given annotation.

        Arguments:
         annotation: The str or type var used to identify an instance.

        Raises:
         KeyError, if the the given annotation does not exist in this scope.
        """
        raise NotImplementedError()


class Container(ABC):
    """An IOC Container"""

    @abstractmethod
    def get(self, annotation: any) -> object:
        """Retrieve an instance from the container

        The instance will be produced according to it's scope. If the instance
        is new, it's dependency chain will also be created according to their scope.

        Arguments:
         annotation: The hint used to locate the member

        Returns:
         An object instance, constant, or function
        """
        raise NotImplementedError()


class ContainerBuilder(ABC):
    """Bind classes, values, functions, and factories to a container."""

    @abstractmethod
    def bind(
        self,
        annotation: any,
        implementation: Callable,
        scope: ScopeEnum = ScopeEnum.TRANSIENT,
        on_activate: Callable[[any], any] = None,
    ):
        """Bind a class.

        Bind any callable type to an annotation. Dependencies will be
        injected into this object as needed when created.

        Scoping can be set to control reuse.

        Arguments:
          annotation:     The hint used to inject an instance of implementation

          implementation: A callable type who's result will be stored return and
                          stored according to the scope

          scope:          Identifies how the object should be cached. Options are
                          Transient, Requested, Singleton
                          Default: Transient.

          on_activate:    An optional function that will be called with the
                          constructed implementation before it is used as a dep
                          or given as the return in container.get()
                          Default: None.

        Scopes:
            Transient scopes and not cached.
            Requested scopes are cached during the current execution of a container.get call.
            Singleton scopes are only instanced once and cached for the lifetime of the container.

        Example:

            class Duck:
                def quack(self):
                    print("quack")

            ioc_builder.bind(
                annotation="duck",
                implementation=Duck)
        """
        raise NotImplementedError()

    @abstractmethod
    def bind_constant(self, annotation: any, value: object):
        """Bind a constant value

        This allows you to bind any object to an annotation in a singleton scope.

        Arguments:
          annotation: The hint used to inject the constant
          value: Any value. Object, function, type, anything.

        Example:

            ioc_builder.bind_constant(
                annotation="my_constant",
                value="Hello, world!")

        """
        raise NotImplementedError()

    @abstractmethod
    def bind_factory(self, annotation: any, factory: Callable[[Container], any]):
        """Bind a higher order function

        This approach allows you to control the creation of objects and gives you access
        to the container. This lets you make runtime decision about how to create an instance.

        Arguments:
          annotation: The hint used to inject the factory
          factory:    A higher order function that accepts the StackContainer as an
                      arugment.

        Example:
            def my_factory_wrapper(ctx: StaticContainer)

                def my_factory(foo):
                    bar = ctx.get("bar")
                    bar.baz(foo)
                    return bar

                return my_factory

            ioc_builder.bind_factory(
                annotation="my_factory",
                factory=my_function)
        """
        raise NotImplementedError()

    @abstractmethod
    def build(self) -> Container:
        """Compute dependency graph and return the container

        This call will roll over all the objects and compute the dependants of each
        member. The container itself is also added to the graph and can thus be
        injected using it's Type as the annotation.

        Example:
            ioc_builder = StaticContainerBuilder()
            ioc = ioc_builder.build()
            container = ioc.get(StaticContainer)
            container == ioc ## True
        """
        raise NotImplementedError()


class CycleTest(ABC):
    """Test a graph of BoundMembers for circular dependencies."""
    @abstractmethod
    def find_cycle(self, bound_members: Dict[any, BoundMember]) -> List[BoundMember]:
        """Check graph of BoundMembers for cycles.

        Arguments:
          bound_members: The graph to test.
        """
        raise NotImplementedError()

class BoundMemberFactory(ABC):
    @abstractmethod
    def build(
        self,
        annotation: any,
        implementation: Callable,
        scope: ScopeEnum
    ) -> BoundMember:
        """Create a new bound member.

        Arguments:
          annotation: The hint associated with this member
          implementation: The implementation used for this member.
          scope: The scope used to construct implementations for this member.
        """
        raise NotImplementedError()
