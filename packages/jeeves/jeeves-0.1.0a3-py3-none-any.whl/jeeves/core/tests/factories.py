import factory

from jeeves.core.objects import Flow, Task


class TaskFactory(factory.Factory):
    name = factory.Faker("name")
    type = "jeeves.core.actions.stub:StubSuccessAction"
    parameters = {}

    class Meta:
        model = Task


class FlowFactory(factory.Factory):
    name = factory.Faker("name")
    tasks = factory.LazyFunction(lambda: [TaskFactory() for _ in range(0, 2)])

    class Meta:
        model = Flow
