# SQL查询指南

## 文档概述

SQL查询指南帮助产品经理使用自然语言描述需求，生成标准SQL查询语句，用于数据分析和报表制作。

---

## 使用场景

- 数据分析需求描述
- 报表数据提取
- 用户行为查询
- 业务指标计算

---

## 常用SQL模板

### 1. 基础查询

**查询指定字段**：

```sql
SELECT 
    user_id,
    user_name,
    created_at
FROM users
WHERE status = 'active'
ORDER BY created_at DESC
LIMIT 100;
```

**查询说明**：
- 选择活跃用户的基本信息
- 按创建时间倒序排列
- 限制返回100条记录

---

### 2. 聚合统计

**按维度统计**：

```sql
SELECT 
    DATE(created_at) AS date,
    COUNT(DISTINCT user_id) AS dau,
    COUNT(*) AS total_actions
FROM user_actions
WHERE created_at >= '2024-01-01'
GROUP BY DATE(created_at)
ORDER BY date;
```

**查询说明**：
- 按日期统计日活用户数和总操作数
- 使用COUNT(DISTINCT)去重统计

---

### 3. 用户留存查询

**N日留存计算**：

```sql
SELECT 
    DATE(first_login) AS cohort_date,
    COUNT(DISTINCT user_id) AS total_users,
    COUNT(DISTINCT CASE WHEN DATE(login_date) = DATE(first_login) + 1 THEN user_id END) AS day1_retention,
    COUNT(DISTINCT CASE WHEN DATE(login_date) = DATE(first_login) + 7 THEN user_id END) AS day7_retention,
    COUNT(DISTINCT CASE WHEN DATE(login_date) = DATE(first_login) + 30 THEN user_id END) AS day30_retention
FROM user_logins
GROUP BY DATE(first_login)
ORDER BY cohort_date;
```

---

### 4. 漏斗分析

**转化漏斗查询**：

```sql
SELECT 
    COUNT(DISTINCT step1.user_id) AS step1_users,
    COUNT(DISTINCT step2.user_id) AS step2_users,
    COUNT(DISTINCT step3.user_id) AS step3_users,
    COUNT(DISTINCT step4.user_id) AS step4_users,
    ROUND(COUNT(DISTINCT step2.user_id) * 100.0 / COUNT(DISTINCT step1.user_id), 2) AS step2_rate,
    ROUND(COUNT(DISTINCT step3.user_id) * 100.0 / COUNT(DISTINCT step1.user_id), 2) AS step3_rate,
    ROUND(COUNT(DISTINCT step4.user_id) * 100.0 / COUNT(DISTINCT step1.user_id), 2) AS step4_rate
FROM 
    (SELECT DISTINCT user_id FROM events WHERE event_name = 'view_home') step1
LEFT JOIN 
    (SELECT DISTINCT user_id FROM events WHERE event_name = 'view_product') step2 ON step1.user_id = step2.user_id
LEFT JOIN 
    (SELECT DISTINCT user_id FROM events WHERE event_name = 'add_cart') step3 ON step1.user_id = step3.user_id
LEFT JOIN 
    (SELECT DISTINCT user_id FROM events WHERE event_name = 'purchase') step4 ON step1.user_id = step4.user_id;
```

---

### 5. 用户分群

**RFM模型分群**：

```sql
SELECT 
    user_id,
    NTILE(5) OVER (ORDER BY last_purchase_date DESC) AS recency_score,
    NTILE(5) OVER (ORDER BY purchase_count DESC) AS frequency_score,
    NTILE(5) OVER (ORDER BY total_amount DESC) AS monetary_score,
    CASE 
        WHEN recency_score >= 4 AND frequency_score >= 4 THEN '高价值用户'
        WHEN recency_score >= 4 AND frequency_score < 4 THEN '新用户'
        WHEN recency_score < 4 AND frequency_score >= 4 THEN '流失风险用户'
        ELSE '普通用户'
    END AS user_segment
FROM (
    SELECT 
        user_id,
        MAX(purchase_date) AS last_purchase_date,
        COUNT(*) AS purchase_count,
        SUM(amount) AS total_amount
    FROM orders
    GROUP BY user_id
) t;
```

---

## 常用函数速查

### 聚合函数

| 函数 | 用途 | 示例 |
|------|------|------|
| COUNT() | 计数 | COUNT(*), COUNT(DISTINCT user_id) |
| SUM() | 求和 | SUM(amount) |
| AVG() | 平均值 | AVG(price) |
| MAX() | 最大值 | MAX(created_at) |
| MIN() | 最小值 | MIN(created_at) |

### 时间函数

| 函数 | 用途 | 示例 |
|------|------|------|
| DATE() | 提取日期 | DATE(created_at) |
| NOW() | 当前时间 | NOW() |
| DATE_SUB() | 日期减法 | DATE_SUB(NOW(), INTERVAL 7 DAY) |
| DATE_ADD() | 日期加法 | DATE_ADD(NOW(), INTERVAL 1 MONTH) |
| DATEDIFF() | 日期差 | DATEDIFF(date1, date2) |
| YEAR/MONTH/DAY() | 提取年月日 | YEAR(created_at) |

### 字符串函数

| 函数 | 用途 | 示例 |
|------|------|------|
| CONCAT() | 字符串连接 | CONCAT(first_name, ' ', last_name) |
| SUBSTRING() | 截取字符串 | SUBSTRING(name, 1, 10) |
| LOWER/UPPER() | 大小写转换 | LOWER(email) |
| LIKE | 模糊匹配 | name LIKE '%关键词%' |

### 条件函数

| 函数 | 用途 | 示例 |
|------|------|------|
| CASE WHEN | 条件判断 | CASE WHEN status = 1 THEN '活跃' ELSE '不活跃' END |
| COALESCE() | 空值处理 | COALESCE(value, 0) |
| IFNULL() | 空值替换 | IFNULL(value, '默认值') |

---

## 查询优化建议

| 建议 | 说明 |
|------|------|
| 使用索引 | WHERE条件字段建立索引 |
| 避免SELECT * | 只查询需要的字段 |
| 限制结果集 | 使用LIMIT限制返回行数 |
| 使用EXPLAIN | 分析查询执行计划 |
| 避免全表扫描 | 合理使用WHERE条件 |

---

## 输出要求

1. SQL语句格式规范、缩进清晰
2. 添加必要的注释说明
3. 确保查询效率合理
4. 验证结果正确性

---

## 相关文档

- 07-04 队列分析报告
- 07-05 数据分析报告
- 07-06 AB测试分析报告