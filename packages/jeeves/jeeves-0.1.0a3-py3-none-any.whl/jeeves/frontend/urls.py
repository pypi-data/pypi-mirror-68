from django.urls import path, include

from jeeves.frontend.views import HomeView, FlowsCRUD, DashboardView

urlpatterns = (
    path("", HomeView.as_view(), name="home"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("flows", FlowsCRUD.list, name="flow-list"),
    path("flows/add", FlowsCRUD.add, name="flow-add"),
    path("flows/<uuid:uuid>", FlowsCRUD.detail, name="flow-detail"),
    path(
        "flows/<uuid:uuid>/",
        include(
            [
                path("run", FlowsCRUD.run, name="flow-run"),
                path(
                    "executions", FlowsCRUD.execution_list, name="flow-execution-list"
                ),
                path(
                    "executions/<uuid:execution_uuid>",
                    FlowsCRUD.execution_detail,
                    name="flow-execution-detail",
                ),
                path(
                    "executions/<uuid:execution_uuid>/delete",
                    FlowsCRUD.execution_delete,
                    name="flow-execution-delete",
                ),
                path("tasks", FlowsCRUD.task_list, name="flow-task-list"),
                path(
                    "tasks/<uuid:task_uuid>/delete",
                    FlowsCRUD.task_delete,
                    name="flow-task-delete",
                ),
                path(
                    "tasks/<uuid:task_uuid>/move/<str:direction>",
                    FlowsCRUD.task_move,
                    name="flow-task-move",
                ),
                path(
                    "tasks/<uuid:task_uuid>", FlowsCRUD.task_edit, name="flow-task-edit"
                ),
                path("tasks/add", FlowsCRUD.task_add, name="flow-task-add"),
                path("delete", FlowsCRUD.delete, name="flow-delete"),
            ]
        ),
    ),
)
