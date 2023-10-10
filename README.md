# ToDoApi

```bash

https://todoapi-42b6.onrender.com/api

```
## Sign UP
```
/register

{
  "username":"x",
  "password":"y"
}
```
## LogIn ( method = POST )
```
/login

{
  "username":"x",
  "password":"y"
}
```
## Add Task ( method = POST )
```
/add
Note : (time_format => %Y-%m-%d %H:%M:%S)
{
    "title":"my1",
    "desc":"mydesc",
    "time":"2023-10-10T12:00:00Z"  
}
```
## Update Task ( method = PUT )
```
/update
Note : (time_format => %Y-%m-%d %H:%M:%S)
{
      "task_id": 1,
      "title": "my1",
      "time": "2023-10-10T12:00:00Z",
      "description": "mydesc",
      "completed": true
}
```

## Delete Task  (method = DELETE)
```
/delete

{
    "task_id": 2
}

```
## Log Out  ( method = POST )
```
/logout
```
## List All Tasks  ( method = GET )
```
/list
```









