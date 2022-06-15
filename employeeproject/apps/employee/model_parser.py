from api.employee.serializer import EmployeeSerializer,EmployeeAuthSerializer


def extract_employee_list_to_dict(employees):
    serializer = EmployeeSerializer(employees,many=True)
    return serializer.data

def extract_employee_details_to_dict(employees):
    serializer = EmployeeSerializer(employees)
    return serializer.data