# HRM LITE - Task is Give by Green Rider company - Connected through QuessCorp : Vendor Company 

## HRM Lite – Admin Panel (Deployed on Railway)

### 🔗 Live Project URL

👉 [https://hrmslite-production-caea.up.railway.app]

## 📌 Project Overview

HRM Lite is a **simple Human Resource Management (HRM) Admin Panel** developed to manage employees and their attendance records.
This project focuses on core HR functionalities with a clean dashboard and easy navigation.
It is deployed on **Railway** and currently works **without authentication (login is not required)**.


## 📊 Dashboard Features

The dashboard provides a quick overview of employee and attendance data using summary cards and tables:
* **Total Employees Count**
* **Present Employees Count (Current Day)**
* **Absent Employees Count (Current Day)**

# Recently Marked Attendance Table Displays:-
* The Recent Attendance table displays records of employees who have checked in on the current day. A limit is applied, so only the 5 most recent check-ins are shown in the table.



## 📂 Side Menu Navigation  :-
The side menu contains quick links to the following pages:

* **Dashboard**
* **Attendance Page**
* **Employee View Page**
* **Add Employee Form**

Each menu item redirects to its respective page where complete data can be viewed or managed.



## 👤 Employee Management ##

### ➕ Add Employee  :-
* New employees can be added using the **Add Employee Form**
* Employee details are saved directly to the database

* The Admin can add employees to the HRM portal by filling out a registration form, which includes **dynamic validations** to ensure data accuracy. The system **prevents duplicate entries**, meaning an employee’s details cannot be registered more than once. Additionally, employees who are no longer active (i.e., whose records have been deleted) cannot be re-registered. Upon successful registration, each employee is automatically assigned a unique Employee ID.

### 📋 View Employee Page  :-

The Employee Management Page displays details of all registered employees. It includes **two dynamic filters** implemented using Python, Django, and MySQL, along with **one client-side filter** using JavaScript that works on the data currently displayed on the page for quick searching and sorting. The Admin has full access to view all employee records and can also delete any employee record if needed.

* Filter by **Employee Name**
* Filter by **Employee Email**
* **Static Filter (JavaScript Based)**

I have implemented a **soft delete feature**, so when an employee record is deleted, it remains in the database. This ensures that the employee’s details are preserved, and they do not need to register again if reinstated.




## Attendance Management :-
* **Dynamic Filter (Database Level)** - **(Filter by Date)**
* **Static Filter (UI Level)** - **On current loaded data**
The Attendance Management page includes two different filters. A dynamic date filter is implemented using backend logic and SQL queries, while a JavaScript-based filter allows searching any user within the currently loaded page data.


## Mark Attendance :-
The Attendance Management module allows an Admin to mark employee attendance through a modal form on the same page. The Admin can select an employee and mark attendance for the current date or up to 40 past days. The system prevents duplicate records for the same employee on the same date. Check-Out is enabled only after Check-In and must be later than the Check-In time. All validations are enforced, and the record is securely saved to the database.




## 🔐 Authentication :-
* This is a **complete HRM Admin Panel**
* **No login or authentication is required** (intentionally kept simple)




## 🛠 Tech Stack  :- 
* Python
* Django
* HTML, CSS, JavaScript, Bootstrap, jquery, font-awesome, popper
* MySQL Database
* Railway (Deployment)