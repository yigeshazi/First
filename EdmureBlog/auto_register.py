import requests

base='root'
for item in range(100,200):
    username=base+str(item)
    email=username+'@163.com'
    pwd=username
    confirm_pwd=pwd
    print(username,email,pwd,confirm_pwd)
    data={'username':username,'password':pwd,'confirm_password':pwd,'email':email,'nickname':'root'}
    url='http://127.0.0.1:6555/register.html'
    res=requests.post(url=url,data=data)

