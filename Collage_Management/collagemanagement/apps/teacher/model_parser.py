from api.teacher.serializer import StudentlistSerializer

def extract_student_list_to_dict(students):
    serializer = StudentlistSerializer(students,many=True)
    return serializer.data

def extract_student_detail_to_dict(students):
    serializer = StudentlistSerializer(students)
    return serializer.data