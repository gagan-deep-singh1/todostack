from django.urls import path

from .views import (
    IndexView,
    TaskListView,
    add_new_task,
    refresh_data,
    move_tasks,
    delete_task,
    delete_all_completed_tasks,
    update_task,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasks/", TaskListView.as_view(), name="tasks"),
    path("move_tasks/", move_tasks, name="move_tasks"),
    path("add_new_task/", add_new_task, name="add_new_task"),
    path("delete_task/", delete_task, name="delete_task"),
    path(
        "delete_all_completed_tasks/",
        delete_all_completed_tasks,
        name="delete_all_completed_tasks",
    ),
    path("update_task/", update_task, name="update_task"),
    path("refresh_data/", refresh_data, name="refresh_data"),
]
