# Process Node Template

## 节点

- `current_node`: `{node_id}`
- `last_checkpoint`: `{checkpoint}`
- `active_workflow`: `{workflow}`

## 目标

{一句话说明当前节点要完成什么}

## 输入

- `{file_or_decision}`

## 已完成

- {只写结果，不写长过程}

## 当前阻塞

- {没有则写“无”}

## 下一步

- {下一步动作}

## 上下文

允许读取：

- `{current_context_file}`

禁止读取：

- `{forbidden_context_file}`
