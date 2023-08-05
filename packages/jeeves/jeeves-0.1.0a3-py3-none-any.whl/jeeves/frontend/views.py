from django.db import transaction
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect

from jeeves.db.models import Run, Flow, Task
from jeeves.core.registry import TaskRegistry
from jeeves.frontend.forms import FlowForm, TaskForm

registry = TaskRegistry()


class HomeView(View):
    def get(self, request):
        return redirect("dashboard")


class DashboardView(View):
    def get(self, request):
        return render(request, template_name="dashboard.j2")


class FlowsCRUD:
    @classmethod
    def add(self, request):
        if request.method == "POST":
            form = FlowForm(request.POST)
            if form.is_valid():
                messages.add_message(
                    request, messages.SUCCESS, "Flow added successfully"
                )
                form.save()
                return redirect("flow-list")
        else:
            form = FlowForm()
        return render(request, template_name="flows/add.j2", context={"form": form})

    @classmethod
    def list(cls, request):
        flows_list = Flow.objects.all()
        return render(
            request, template_name="flows/list.j2", context={"flows": flows_list}
        )

    @classmethod
    def detail(cls, request, uuid):
        return redirect("flow-task-list", uuid=uuid)

    @classmethod
    def run(cls, request, uuid):
        flow = Flow.objects.get(pk=uuid)
        execution = flow.execute()
        messages.add_message(
            request, messages.SUCCESS, f"Flow running: {str(execution.pk)}"
        )
        return redirect("flow-execution-list", uuid=uuid)

    @classmethod
    def execution_list(self, request, uuid):
        flow = Flow.objects.get(pk=uuid)
        return render(
            request, template_name="flows/execution-list.j2", context={"flow": flow}
        )

    @classmethod
    def execution_detail(self, request, uuid, execution_uuid):
        flow = Flow.objects.get(pk=uuid)
        execution = Run.objects.get(pk=execution_uuid)
        return render(
            request,
            template_name="flows/execution-detail.j2",
            context={"flow": flow, "execution": execution},
        )

    @classmethod
    def execution_delete(self, request, uuid, execution_uuid):
        flow = Flow.objects.get(pk=uuid)
        execution = Run.objects.get(pk=execution_uuid)
        if request.method == "POST":
            execution.delete()
            messages.add_message(request, messages.SUCCESS, "Run deleted successfully")
            return redirect("flow-execution-list", uuid=uuid)
        return render(
            request,
            template_name="flows/execution-delete.j2",
            context={"flow": flow, "execution": execution},
        )

    @classmethod
    def task_list(cls, request, uuid):
        flow = Flow.objects.get(pk=uuid)
        # definition = flow.definition
        # definition["tasks"] = [str(task.pk) for task in Task.objects.all()]
        # flow.definition = definition
        # flow.save()
        return render(
            request, template_name="flows/task-list.j2", context={"flow": flow}
        )

    @classmethod
    def task_add(cls, request, uuid):
        flow = Flow.objects.get(pk=uuid)
        if request.method == "POST":
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save()
                flow_def = flow.definition
                flow_def["tasks"].append(str(task.id))
                flow.definition = flow_def
                flow.save()
                messages.add_message(request, messages.SUCCESS, "Task added to flow")
                return redirect("flow-task-list", uuid=uuid)
        else:
            form = TaskForm()
        return render(
            request,
            template_name="flows/task-add.j2",
            context={"flow": flow, "form": form, "task_types": registry.tasks},
        )

    @classmethod
    def task_edit(cls, request, uuid, task_uuid):
        flow = Flow.objects.get(pk=uuid)
        task = Task.objects.get(pk=task_uuid)
        if request.method == "POST":
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save()
                messages.add_message(
                    request, messages.SUCCESS, f"Task {task.pk} edited"
                )
                return redirect("flow-task-list", uuid=uuid)
        else:
            form = TaskForm(instance=task, initial={"definition": task._definition})
        return render(
            request,
            template_name="flows/task-add.j2",
            context={
                "flow": flow,
                "form": form,
                "task": task,
                "task_types": registry.tasks,
            },
        )

    @classmethod
    @transaction.atomic
    def task_delete(self, request, uuid, task_uuid):
        flow = Flow.objects.get(pk=uuid)
        task = Task.objects.get(pk=task_uuid)
        task.delete()
        definition = flow.definition
        definition["tasks"].remove(str(task_uuid))
        flow.definition = definition
        flow.save()
        messages.add_message(request, messages.SUCCESS, f"Task {task_uuid} deleted")
        return redirect("flow-task-list", uuid=uuid)

    @classmethod
    def task_move(self, request, uuid, task_uuid, direction="up"):
        flow = Flow.objects.get(pk=uuid)
        definition = flow.definition
        index = definition["tasks"].index(str(task_uuid))
        new_index = (index - 1) if direction == "up" else index + 1
        definition["tasks"].insert(new_index, definition["tasks"].pop(index))
        flow.definition = definition
        flow.save()
        messages.add_message(request, messages.SUCCESS, "Task moved")
        return redirect("flow-task-list", uuid=uuid)

    @classmethod
    def delete(cls, request, uuid):
        flow = Flow.objects.get(pk=uuid)
        if request.method == "POST":
            flow_id = str(flow.id)
            flow.delete()
            messages.add_message(request, messages.SUCCESS, f"Flow {flow_id} deleted")
            return redirect("flow-list")
        return render(request, template_name="flows/delete.j2", context={"flow": flow})
