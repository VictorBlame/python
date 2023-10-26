import requests

get_all_employees = 'http://dummy.restapiexample.com/api/v1/employees'
post_create_employee = 'http://dummy.restapiexample.com/api/v1/create'
delete_employee = 'http://dummy.restapiexample.com/api/v1/delete/'
headers = {"User-Agent": "Roli_EPAM"}


def get_all_users(request, header):
    request_response = requests.get(request, headers=header)

    if request_response.status_code == 200:
        print('Status code is ' + str(request_response.status_code) + ', everything is okay')
        print(request_response.json())
    else:
        print('Status code is ' + str(request_response.status_code) + ', we have a problem!')


def post_create_user(request, header, name, age, salary):
    request_response = requests.post(request, headers=header,
                                     params={'employee_name': name, 'employee_salary': salary, 'employee_age': age})
    data = request_response.json()

    if request_response.status_code == 200 and data['data']['employee_name'] == name:
        print('Status code is ' + str(request_response.status_code) + ', and employee name is ' + str(
            data['data']['employee_name']) + ', everything is okay')
        print(data)
    else:
        print('Status code is ' + str(request_response.status_code) + ', we have a problem!')


def delete_user(request, header, id):
    request += str(id)
    request_response = requests.delete(request, headers=header)
    data = request_response.json()

    if data['message'] == 'Successfully! Record has been deleted':
        print('Deleting was successful')
        print(data)
    else:
        print('Deleting was not successful')


get_all_users(get_all_employees, headers)
post_create_user(post_create_employee, headers, 'Victor Blame', 26, 5000)
delete_user(delete_employee, headers, 1)
