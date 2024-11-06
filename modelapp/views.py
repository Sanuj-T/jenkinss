from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Employee, Department, Project
from .serializers import EmployeeSerializer, DepartmentSerializer, ProjectSerializer

class EmployeeList(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetail(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_department(self, request, pk):
        employee = self.get_object(pk)
        department = employee.department
        department_serializer = DepartmentSerializer(department)
        return Response(department_serializer.data)

class DepartmentList(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentDetail(APIView):
    def get_object(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department)
        employees = department.employee_set.all()
        employee_serializer = EmployeeSerializer(employees, many=True)
        return Response({"department": serializer.data, "employees": employee_serializer.data})

    def put(self, request, pk):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = self.get_object(pk)
        if department.employee_set.exists():
            return Response({"error": "Cannot delete department with existing employees."}, status=status.HTTP_400_BAD_REQUEST)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectList(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetail(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def delete(self, request, pk):
        project = self.get_object(pk)
        if project.end_date >= date.today():
            return Response({"error": "Cannot delete project that is still ongoing."}, status=status.HTTP_400_BAD_REQUEST)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update_status(self, request, pk):
        project = self.get_object(pk)
        status = request.data.get('status')
        if status in dict(Project.STATUS_CHOICES).keys():
            project.status = status
            project.save()
            return Response({"status": "Project status updated."})
        return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

    def add_member(self, request, pk):
        project = self.get_object(pk)
        employee_id = request.data.get('employee_id')
        try:
            employee = Employee.objects.get(pk=employee_id)
            project.team.add(employee)
            return Response({"status": "Member added to project."})
        except Employee.DoesNotExist:
            return Response({"error": "Employee does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    def get_budget(self, request, pk):
        project = self.get_object(pk)
        total_budget = sum(employee.salary for employee in project.team.all())
        return Response({"total_budget": total_budget})
