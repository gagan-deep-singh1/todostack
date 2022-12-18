from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from django.utils import timezone
from accounts.models import User
from todo_core.models import TodoItem


class IndexView(APIView):
    def get(self, request):
        return render(request, "todo_core/index.html")


class TaskListView(ListView, LoginRequiredMixin):
    """ Using Class based view - ListView """

    model = TodoItem
    template_name = "todo_core/tasks.html"  # <app_name>/<model>_<viewtype>.html
    context_object_name = "tasks"

    def get_queryset(self):
        print(self.request.user)
        current_user = User.objects.get(system_user=self.request.user)
        print('hey')
        return current_user.todo_items.all()


class MoveTasksView(APIView, LoginRequiredMixin):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        # Gets the Task's ID from the checkbox that is clicked
        task_id = request.POST["task_id"]
        # Gets the Task's Class name from the checkbox that is clicked
        task_class = request.POST["task_class"]
        # If the Clicked Task is an Active Task - Move it from Active Table to Complete Table
        if "mark_as_done" in task_class:
            # Select the Task whose id matches with task_id
            done_task = TodoItem.objects.get(pk=task_id)
            # Update the 'completed_at' attribute to True. i.e, Mark as Done
            done_task.completed_at = timezone.now()
            # Save the changes to the Database
            done_task.save()

        # If the Clicked Task is a Complete Task - Move it from Complete Table to Active Table
        elif "mark_as_undone" in task_class:
            # Select the task matching with the task_id
            undone_task = TodoItem.objects.get(pk=task_id)
            # Update the 'completed_at' attribute to 'False' i.e, Mark as Undone
            undone_task.completed_at = None
            # Save the changes to the Database
            undone_task.save()

        # Return redirect response to a different view with reverse 'tasks'

        return HttpResponse("Success!")


# Convert the above view to function based view
@csrf_exempt
@login_required
def move_tasks(request):
    if request.method == "POST":
        # Gets the Task's ID from the checkbox that is clicked
        task_id = request.POST["task_id"]
        # Gets the Task's Class name from the checkbox that is clicked
        task_class = request.POST["task_class"]
        # If the Clicked Task is an Active Task - Move it from Active Table to Complete Table
        print(task_class)
        if "mark_as_done" in task_class:
            # Select the Task whose id matches with task_id
            done_task = TodoItem.objects.get(pk=task_id)
            # Update the 'completed_at' attribute to True. i.e, Mark as Done
            done_task.completed_at = timezone.now()
            # Save the changes to the Database
            done_task.save()

        # If the Clicked Task is a Complete Task - Move it from Complete Table to Active Table
        elif "mark_as_undone" in task_class:
            # Select the task matching with the task_id
            undone_task = TodoItem.objects.get(pk=task_id)
            # Update the 'completed_at' attribute to 'False' i.e, Mark as Undone
            undone_task.completed_at = None
            # Save the changes to the Database
            undone_task.save()
        print("Success!")

        # Return redirect response to a different view with reverse 'tasks'
        return HttpResponse("Success!")


# @method_decorator(csrf_exempt, name="dispatch")
class AddNewTaskView(APIView, LoginRequiredMixin):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        # Getting the task Name from Ajax
        task_name = request.POST["title"].strip()
        # Dummy User - for the purpose of testing
        creator = request.user.todostack_user
        # Adding the task to the Database Table - Task
        temp_task = TodoItem(title=task_name, author=creator)
        # Saving the changes to the Database
        temp_task.save()
        # Converting the newly added task that is saved to Dictionary format and returning as JSON format
        task_json_string = model_to_dict(temp_task, fields=["id", "title", "owner"])

        return JsonResponse(task_json_string)


# Convert the class to a function based view
@csrf_exempt
@login_required
def add_new_task(request):
    if request.method == "POST":
        # Getting the task Name from Ajax
        task_name = request.POST["title"].strip()
        print(request.POST)
        print(task_name)
        # Dummy User - for the purpose of testing
        creator = request.user.todostack_user
        # Adding the task to the Database Table - Task
        temp_task = TodoItem(title=task_name, owner=creator)
        # Saving the changes to the Database
        temp_task.save()
        # Converting the newly added task that is saved to Dictionary format and returning as JSON format
        task_json_string = model_to_dict(temp_task, fields=["id", "title", "owner"])

        return JsonResponse(task_json_string)


class DeleteTaskView(APIView, LoginRequiredMixin):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        # Getting the task_id from AJAX
        task_id = request.POST["task_id"]
        # Selecting the task with the given task_id
        del_task = TodoItem.objects.get(id=task_id)
        # Deleting the task from the Table
        del_task.delete()
        print(f"Deleted the Task with ID: {task_id}")
        return HttpResponse("Deleted the Task")


# Convert the class to a function based view
@csrf_exempt
@login_required
def delete_task(request):
    if request.method == "POST":
        # Getting the task_id from AJAX
        task_id = request.POST["task_id"]
        # Selecting the task with the given task_id
        del_task = TodoItem.objects.get(id=task_id)
        # Deleting the task from the Table
        del_task.delete()
        print(f"Deleted the Task with ID: {task_id}")
        return HttpResponse("Deleted the Task")


class DeleteAllCompletedTasksView(APIView, LoginRequiredMixin):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        # Getting the Tasks that are Marked as Completed - i.e, Tasks that have completed_at == 1
        del_tasks = TodoItem.objects.filter(completed_at__isnull=False)
        # Deleting the Completed Tasks
        del_tasks.delete()
        # print('Deleted all Completed Tasks')
        return HttpResponse("Successfully Deleted all Completed Tasks")


# Convert the class to a function based view
@csrf_exempt
@login_required
def delete_all_completed_tasks(request):
    if request.method == "POST":
        # Getting the Tasks that are Marked as Completed - i.e, Tasks that have completed_at == 1
        del_tasks = TodoItem.objects.filter(completed_at__isnull=False)
        # Deleting the Completed Tasks
        del_tasks.delete()
        # print('Deleted all Completed Tasks')
        return HttpResponse("Successfully Deleted all Completed Tasks")


class UpdateTaskView(APIView, LoginRequiredMixin):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        # Getting the Task ID of the task to be updated from AJAX Call
        task_id = request.POST["task_id"]
        # Getting the modified Task name from AJAX Call
        new_task = request.POST["task_name"]
        # Querying the Task model to get the task based on task_id
        changed_task = TodoItem.objects.get(id=task_id)
        # Updating the Task Name with the NEW Value
        changed_task.title = new_task.strip()
        # Saving the changes to the Database
        changed_task.save()
        # For Debugging Purpose
        print(f"Task Updated ID: {task_id}")
        return HttpResponse("Successfully Updated Tasks")


# Convert the class to a function based view
@csrf_exempt
@login_required
def update_task(request):
    if request.method == "POST":
        # Getting the Task ID of the task to be updated from AJAX Call
        task_id = request.POST["task_id"]
        # Getting the modified Task name from AJAX Call
        new_task = request.POST["task_name"]
        # Querying the Task model to get the task based on task_id
        changed_task = TodoItem.objects.get(id=task_id)
        # Updating the Task Name with the NEW Value
        changed_task.title = new_task.strip()
        # Saving the changes to the Database
        changed_task.save()
        # For Debugging Purpose
        print(f"Task Updated ID: {task_id}")
        return HttpResponse("Successfully Updated Tasks")


class RefreshDataView(APIView, LoginRequiredMixin):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        # Getting the username of the User requested
        user = request.user
        # Converting the user's tasks to JSON format
        data = serializers.serialize("json", user.task_set.all())
        # Return the JSON string. Will work only if safe is set to 'False'
        return JsonResponse(data, safe=False)


@csrf_exempt
@login_required
def refresh_data(request):
    if request.method == "POST":
        # Getting the username of the User requested
        user = request.user.todostack_user
        # Converting the user's tasks to JSON format
        data = serializers.serialize("json", user.todo_items.all())
        # Return the JSON string. Will work only if safe is set to 'False'
        # print(data)
        return JsonResponse(data, safe=False)
