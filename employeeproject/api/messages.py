from rest_framework import status

messages = {
    100 : {
        "error": {"status_code": 100, "msg": "OOps! Something went wrong"},
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR
    },
    101 : {
        "error": {"status_code": 101, "msg": "Email Id already exist"},
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY
    },
    102 : {
        "error": {"status_code": 102, "msg": "Salary should be a valid float value"},
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY   
    },
    103 : {
        "error": {"status_code": 103, "msg": "Employee with given id doesn't exist!"},
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY   
    },
    104 : { 
        "error": {"status_code": 104, "msg": "Password Must be 8 Characters "},
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY   
    },
    105 : { 
        "error": {"status_code": 105, "msg": "User Not Exists"},
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY   
    },
    106 : { 
        "error": {"status_code": 106, "msg": "Incorrect password"},
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY   
    }
}