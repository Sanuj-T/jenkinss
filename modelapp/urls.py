from django.urls import path
from .views import (
    EmployeeList, EmployeeDetail,
    DepartmentList, DepartmentDetail,
    ProjectList, ProjectDetail
)

urlpatterns = [
    # Employee APIs
    path('employees/', EmployeeList.as_view(), name='employee-list'),
    path('employees/<int:pk>/', EmployeeDetail.as_view(), name='employee-detail'),
    path('employees/<int:pk>/department/', EmployeeDetail.as_view(), name='employee-department'),

    # Department APIs
    path('departments/', DepartmentList.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetail.as_view(), name='department-detail'),

    # Project APIs
    path('projects/', ProjectList.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('projects/<int:pk>/add-member/', ProjectDetail.as_view(), name='project-add-member'),
    path('projects/<int:pk>/update-status/', ProjectDetail.as_view(), name='project-update-status'),
]
