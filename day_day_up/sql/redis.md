### redis批量删除key（借助linux的xargs命令）
```shell
redis-cli -a [password] -n [DB] keys ["模式串"] | xargs redis-cli -a [password] -n [DB] del
```