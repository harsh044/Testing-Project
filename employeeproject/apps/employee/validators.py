def validate_employee_details(salary):
    if salary:
        if type(salary) != float:
            return 102
        
    return ""

def validate_password(password):
    if len(password) < 8:
        return 104
    return ""