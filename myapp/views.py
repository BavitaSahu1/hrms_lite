from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection, DatabaseError
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import logging


current_datetime = timezone.localtime(timezone.now())
current_date = timezone.localtime(timezone.now()).date()

# current_datetime = timezone.now()
# current_date = timezone.now().date()

logger = logging.getLogger(__name__)



def base_admin(request):
    try:
        return render(request, "base_admin.html")
    except Exception as e:
        logger.exception(e)
        return HttpResponse("Something went wrong", status=500)

def base_dashboard(request):
    try:
        return render(request,"base_dashboard.html")
    except Exception as e:
        logger.exception(e)
        return HttpResponse("Something went wrong", status=500)


def add_emp(request):
    try:
        return render(request, "add_emp.html")
    except Exception as e:
        logger.exception(e)
        return HttpResponse("Something went wrong", status=500)


@csrf_exempt
def saveEmployeeData(request):
    try:
        if request.method=='POST':
            First_Name = request.POST.get('f_name').strip().title()
            Last_name = request.POST.get('l_name').strip().title()
            Department = request.POST.get('department')
            Email = request.POST.get('email')
            Fullname = (First_Name+' '+Last_name)
            my_cur=connection.cursor()
            try:
                check_active_emp = "SELECT email_address from employee WHERE email_address = %s and deleted_at Is Null;"
                check_inactive_emp = "SELECT email_address from employee WHERE email_address = %s and deleted_at Is not Null;"

                my_cur.execute(check_active_emp, [Email])
                active_existing_Email = my_cur.fetchone()
                my_cur.execute(check_inactive_emp, [Email])
                inactive_existing_Email = my_cur.fetchone()

                if active_existing_Email:
                    messages.error(request,"Employee Email already exist")
                elif inactive_existing_Email:
                    messages.error(request,"This employee account exists but is currently inactive.")
                else:
                    insert_query = "insert into employee(full_name,department,email_address,created_at) values(%s,%s,%s,%s);" 
                                     
                    my_cur.execute(insert_query, [Fullname,Department,Email,current_datetime])
                    connection.commit()

                    messages.success(request,"Data Saved Successfully...")
            finally:
                my_cur.close()
    except DatabaseError as db_err:
        logger.exception(db_err)
        messages.error(request, "Database error occurred")
    except Exception as e:
        logger.exception(e)
        messages.error(request, "Unexpected error occurred") 
    return redirect('add_emp')


# dictfetchall for show data to all Pages --------------------------
def dictfetchall(cursor):
    try:
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
    except Exception as e:
        logger.exception(e)
        return []



@csrf_exempt
def view_emp(request):
    try:
        cursor = connection.cursor()
        try:

            if request.method == 'POST':
                user_input1 = request.POST.get('a_name')
                user_input2 = request.POST.get('a_email')

                conditions = []
                params = []

                if user_input1:
                    conditions.append("full_name LIKE %s")
                    params.append(f"%{user_input1}%")

                if user_input2:
                    conditions.append("email_address LIKE %s")
                    params.append(f"%{user_input2}%")

                query = """
                SELECT full_name, email_address, emp_id, department
                FROM employee
                WHERE deleted_at IS NULL
                """

                if conditions:
                    query += " AND (" + " OR ".join(conditions) + ")"

                cursor.execute(query, params)
                data = dictfetchall(cursor)

            else:
                query = """
                SELECT full_name, email_address, emp_id, department
                FROM employee
                WHERE deleted_at IS NULL
                """
                cursor.execute(query)
                data = dictfetchall(cursor)
        finally:
            cursor.close()

        return render(request, "view_emp.html", {'data': data})

    except Exception as e:
        logger.exception(e)
        messages.error(request, "Unable to fetch employee data")
        return redirect('view_emp')



@csrf_exempt
def DeleteEmp(request):
    try:
        if request.method == 'POST':
            DeleteButton = request.POST.get('DeleteBtn')
            my_cur=connection.cursor()
            try:
                my_cur.execute("SELECT full_name FROM employee WHERE emp_id= %s and deleted_at Is Null;", [DeleteButton])
                emp_name = my_cur.fetchone()
                    
                query = "update employee set deleted_at = %s where emp_id = %s and deleted_at is Null;" 
                query2 = "update attendance set deleted_at = %s where emp_id = %s and deleted_at is Null;" 
                my_cur.execute(query, [current_datetime, DeleteButton])
                my_cur.execute(query2, [current_datetime, DeleteButton])
                connection.commit()
                messages.success(request, f"{emp_name[0]}'s Employee Record Deleted. ")
            finally:
                my_cur.close()
    except Exception as e:
        logger.exception(e)
        messages.error(request, "Failed to delete employee")
    return redirect('view_emp')


@csrf_exempt
def view_attendance(request):
    try:
        cursor = connection.cursor()
        try:
            if request.method == 'POST':          
                user_input = request.POST.get('att_date')
                if user_input:
                    query1  = """SELECT 
                        emp.full_name,
                        emp.emp_id,
                        COALESCE(att.attendance_date, '') AS attendance_date,
                        COALESCE(att.check_in, '') AS in_time,
                        COALESCE(att.check_out, '') AS out_time,
                        COALESCE(att.attendance_status, '') AS emp_status
                        FROM employee AS emp
                        LEFT JOIN attendance AS att
                        ON emp.emp_id = att.emp_id
                        where att.attendance_date = %s
                        and emp.deleted_at is Null
                        and att.deleted_at is Null;
                       """
                cursor.execute(query1, [user_input])
                attendance_data=dictfetchall(cursor)
            else:  
                query2  = """SELECT 
                        emp.full_name,
                        emp.emp_id,
                        COALESCE(att.attendance_date, '') AS attendance_date,
                        COALESCE(att.check_in, '') AS in_time,
                        COALESCE(att.check_out, '') AS out_time,
                        COALESCE(att.attendance_status, '') AS emp_status
                        FROM employee AS emp
                        LEFT JOIN attendance AS att
                        ON emp.emp_id = att.emp_id
                        where emp.deleted_at is Null
                        and att.deleted_at is Null
                        ORDER BY att.attendance_date IS NULL, att.attendance_date DESC;
                       """
                cursor.execute(query2)
                attendance_data = dictfetchall(cursor)

            query_for_model = """SELECT DISTINCT emp_id, email_address FROM employee WHERE deleted_at IS NULL;"""
            cursor.execute(query_for_model)
            model_data = dictfetchall(cursor)
        finally:
            cursor.close()
        return render(request,"view_attendance.html", {'data':attendance_data, 'model_data':model_data})
    except Exception as e:
        logger.exception(e)
        messages.error(request, "Unable to fetch attendance data")
        return redirect('dashboard')




@csrf_exempt
def dashboard(request):
    try:
        cursor = connection.cursor()
        try:
            query1 = "select count(*) AS employee_id from employee where deleted_at is Null;"
            query2 = "select count(*) AS present_employee from attendance where attendance_status = 'Present' and attendance_date = CURDATE() and deleted_at is Null;"
            query3 = "select count(*) AS absent_employee from attendance where attendance_status = 'Absent' and attendance_date = CURDATE() and deleted_at is Null;"
            query4 = """SELECT emp.full_name,
                        emp.department,
                        att.attendance_status,
                        att.attendance_date,
                        att.check_in
                    FROM employee emp
                    Inner JOIN attendance att
                        ON att.emp_id = emp.emp_id
                    where emp.deleted_at is Null
                    and att.deleted_at is Null
                    and att.attendance_date = %s
                    ORDER BY 
                        CAST(att.check_in AS TIME) DESC
                    limit 5; """
            cursor.execute(query1)
            total_employees = dictfetchall(cursor)

            cursor.execute(query2)
            present_employees = dictfetchall(cursor)

            cursor.execute(query3)
            absent_employees = dictfetchall(cursor)

            cursor.execute(query4, [current_date])
            recent_attendance_updated = dictfetchall(cursor)
        finally:
            cursor.close()
        
        return render(request,"dashboard.html", {'data1':total_employees, 'data2':present_employees, 'data3':absent_employees, 'data4':recent_attendance_updated})
    except Exception as e:
        logger.exception(e)
        messages.error(request, "Failed to load dashboard")


@csrf_exempt
def MarkAttendance(request):
    try:
        if request.method == "POST":
            emp_id = request.POST.get("emp_id")
            date = request.POST.get("attendance_date")
            in_time = request.POST.get("in_time")
            out_time = request.POST.get("out_time")
            status = request.POST.get("emp_status") 

            cursor = connection.cursor()
            try:
                query1 = "SELECT emp_id, full_name FROM employee WHERE deleted_at is Null;"
                cursor.execute(query1)

                query2 = "select emp_id, attendance_date from attendance where emp_id = %s and attendance_date = %s and deleted_at is Null;"
                cursor.execute(query2, [emp_id, date])
                check_attendance = dictfetchall(cursor)
                if check_attendance:
                    messages.error(request,f"Attendance already exists for Employee ID '{check_attendance[0]['emp_id']}' "
                    f"on the selected date {check_attendance[0]['attendance_date']}. "
                    f"Duplicate entry is not allowed.")
                else:
                    query3 = "insert into attendance(emp_id, attendance_date, attendance_status, check_in, check_out, created_at) values(%s,%s,%s,%s,%s,%s)"
                    cursor.execute(query3, [emp_id, date, status, in_time, out_time, current_datetime])
                    connection.commit()
                    messages.success(request, f"Attendance marked successfully...")
            finally:
                cursor.close()
    except Exception as e:
        logger.exception(e)
        messages.error(request, "Failed to mark attendance")
    return redirect("view_attendance")



def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)





# @csrf_exempt
# def UpdateAttendance(request):
#     try:
#         if request.method == 'POST': 
#             EmpID = request.POST.get('emp_id')         
#             AttendanceDate = request.POST.get('attendance_date')
#             InTime = request.POST.get('in_time')
#             OutTime = request.POST.get('out_time')
#             AttendanceStatus = request.POST.get('attendance_status')

#             cursor = connection.cursor()
#             try:
#                 cursor.execute("SELECT full_name FROM employee WHERE emp_id = %s and deleted_at is Null;", [EmpID])
#                 emp_name = cursor.fetchone()

#                 query = "select emp_id, attendance_date from attendance where emp_id = %s and attendance_date = %s and deleted_at is Null;"
#                 cursor.execute(query, [EmpID, AttendanceDate])
#                 check_attendance = dictfetchall(cursor)
#                 if check_attendance:
#                     messages.error(request,f"Attendance already exists for Employee ID {check_attendance[0]['emp_id']} "
#                 f"on the selected date {check_attendance[0]['attendance_date']}. "
#                 f"Duplicate entry is not allowed.")
#                 else:

#                     cmd = "insert into attendance(emp_id, attendance_date, check_in, check_out, attendance_status) values(%s,%s,%s,%s,%s)" 
#                     cursor.execute(cmd, [EmpID, AttendanceDate, InTime, OutTime, AttendanceStatus])
#                     connection.commit()
#                     messages.success(request, f"Attendance Details Updated for {emp_name[0]}")
#             finally:
#                 cursor.close()
#     except Exception as e:
#         logger.exception(e)
#         messages.error(request, "Failed to update attendance")
#     return redirect('view_attendance')


###############
# @csrf_exempt
# def EditAttStatus(request):
#     try:
#         if request.method == 'POST':
#             emp_id = request.POST.get('editBtn')
#             att_date = request.POST.get('editBtn2')
#             cursor = connection.cursor()
#             try:
#                 # cmd = "SELECT * FROM employee WHERE emp_id = %s and attendance_date = %s and deleted_at is Null;"
#                 cmd2 = "SELECT * FROM attendance WHERE emp_id = %s and attendance_date = %s and deleted_at is Null;"
#                 # cursor.execute(cmd, [emp_id,att_date])
#                 # a = dictfetchall(cursor)
#                 cursor.execute(cmd2, [emp_id,att_date])
#                 attendance_upd = dictfetchall(cursor)
#             finally:
#                 cursor.close()
#         return render(request,"EditAttStatus.html", {'data2':attendance_upd})
#     except Exception as e:
#         logger.exception(e)
#         messages.error(request, "Unable to fetch attendance details")
#         return redirect('view_attendance')