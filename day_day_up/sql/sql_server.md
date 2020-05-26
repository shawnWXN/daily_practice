### SQL Server常用转换方法CAST与CONVERT
>官方教程:[https://docs.microsoft.com/zh-cn/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver15](https://docs.microsoft.com/zh-cn/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver15)
- 时间转时间字符串
    ```sql
    SELECT CONVERT(NVARCHAR(30),GETDATE())
    output：04 11 2020 9:13AM
    SELECT CONVERT(NVARCHAR(30),GETDATE(),22)
    output：04/11/20 9:14:18 AM
    SELECT CONVERT(NVARCHAR(30),GETDATE(),20)
    output：2020-04-11 09:15:34
    SELECT CONVERT(NVARCHAR(30),GETDATE(),21)
    output：2020-04-11 09:16:12.510
    ```
- 时间字符串转时间
    ```sql
    SELECT CONVERT(DATETIME,'4/1/2020 06:32:45 PM')
    output：2020-04-01 18:32:45
    ```