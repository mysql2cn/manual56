# MySQL专业词汇表 #

## A ##
### ACID
### adaptive flushing 自适应刷新
### adaptive hash index 自适应哈希索引
### AHI adaptive hash index的缩写
### AIO 异步IO
### Antelope 不译，innodb code name
### application programming interface 译为: API
### apply 应用
### .ARM file 不译 Archive表的定义信息
### .ARZ file 不译 Archive表的数据文件
### asynchronous I/O 异步I/O 也可说AIO
### atomic 原子（性）
### atomic instruction CPU中不可中断的指令（原子指令）
### auto-increment 自增
### auto-increment locking 自增锁
### autocommit 自动提交
### availability 可用性

## B ##
### B-tree B树
### backticks 反引号
### backup 备份
### Barracda （Innodb code name）
### beta 公测
### binary log 二进制日志
### binlog 二进制日志（同binary log）
### bind query expansion （使用query expansion）
### bottleneck 瓶颈
### bounce 性能抖动
### buddy allocator （Innodb buffer pool内存分配中的单位）
### buffer 缓冲（或不译）
### buffer pool 缓冲池 （或不译）
### buffer pool instance 缓冲池实例（或不译）
### built-in 内置
### business rules 业务规则

## C ##
### cache 缓存
### cardinality 基数
### .cfg file 不译
### change buffer 变更缓冲区
### change buffering 变更缓冲
### checkpoint 检查点
### checksum 校验
### child table 子表
### clean page 干净的页
### clean shutdown 完成buffer刷新的关闭
### client 客户端
### clustered index 聚集索引
### cold backup 冷备份
### column 列
### column index 单列索引
### column prefix 列的前缀
### commit 提交
### compact row format 紧凑（compact）的行格式
### composite index 复合索引
### compressed backup 压缩备份
### compressed row format 压缩的行格式
### compression 压缩
### compression failure 压缩失败
### concatenated index 复合索引
### concurrency 并发
### configuration file 配置文件
### consistend read 一致性读
### constraint 约束
### counter 记数器
### covering index 覆盖索引
### crash 崩溃
### crash recovery 崩溃恢复
### CRUD （不译）
### cursor 游标 Or 光标

## D ##
### data definition language 译为：DDL
### data dictionary 数据字典
### data directory 数据目录 
### data files 数据文件
### data manipulation language 译为:DML
### data warehouse DW Or 数据仓库
### database 数据库
### DCL : Data control language 不译
### DDL
### deadlock 死锁
### deadlock detection 死锁检测
### delete 删除
### delete buffering 删除缓冲
### denormalized 反范式
### descending index 降序索引
### dirty page 脏页
### dirty read 脏读
### disk-based 基于磁盘
### disk-bound 磁盘带宽
### DML 
### document id 全文索引编号
### doublewrite buffer 双写缓冲
### drop 删除
### dynamic row format 变长行格式

## E ##
### early adopter 测试版
### error log 错误日志
### eviction 替换出去
### exclusive lock 排它锁
### extent 区

## F ##
### Fast Index Creation 快速创建索引
### fast shutdown 快速关闭
### file format 文件格式
### file-per-table 独立表空间
### fill factor 填充因子
### fixed row format 定长行格式
### flush 刷新
### flush list 刷新列表
### foreign key 外键
### FOREIGN KEY constraint 外键约束
### .frm file 
### FTS 全文搜索
### full backup 全备
### full table scan 全表扫描
### FULLTEXT index 全文索引
### fuzzy checkpointing 模糊检查点刷新

## G ##
### <a name="GA"/>GA 一般可用（建议直接用 GA）
### gap 间隙
### <a name="gap_lock"/>gap lock 间隙锁
### general log 数据库日志
### general query log 同general log 数据库日志
### global_transaction 全局事务
### group commit 组提交

## H ##
### hash index 哈希索引
### HDD 机械磁盘或不译
### heartbeat 心跳
### high-water mark 上限
### history list 清除链表
### hot 热
### hot backup 热备

## I ##
### I/O-bound I/O带宽
### ib-file set ib文件集
### ib_logfile ib_logfile redolog文件或不译
### ibbackup_logfile 不译
### .ibd file .ibd文件
### ibdata file ibdata文件
### ibtmp file ibtmp文件
### .ibz file .ibz文件
### ilist 索引词链表
### implicit row lock 隐式行锁
### in-memory database 内存数据库
### incremental backup 增量备份
### index 索引
### index cache 索引缓存
### index hint 索引提示
### index prefix 索引前缀
### index statistics 索引统计
### infimum record 伪记录
### INFORMATION_SCHEMA 系统信息库
### InnoDB InnoDB
### innodb_autoinc_lock_mode innodb参数，不用译
### innodb_file_format innodb参数，不用译
### innodb_file_per_table innodb参数，不用译
### innodb_lock_wait_timeout innodb参数，不用译
### innodb_strict_mode innodb参数，不用译
### insert 插入
### insert buffer change buffer以前的叫法
### insert buffering 插入缓存技术
### instance 实例
### instrumentation 监测
### intention exclusive lock 意向排它锁
### intention lock 意向锁
### intention shared lock 意向共享锁
### inverted index 反向索引
### IOPS 每秒读写次数，可不译
### .isl file .isl文件
### isolation level 事务隔离级别

## J ##
### join 关联

## K ##
### KEY_BLOCK_SIZE InnoDB表选项

## L ##
### latch 读写锁
### list buffer 页面lru链表
### lock 锁
### lock escalation 锁升级
### lock mode 锁模式
### locking 锁机制
### locking read 加锁读
### log 日志
### log buffer 日志缓冲
### log file 日志文件
### log group 日志组
### logical 逻辑
### logic backup 逻辑备份
### loose_ 一个前缀，不译
### low-water mark 下限
### LRU 最近最少使用
### LSN 日志序号

## M ##
### master server 主服务器
### master thread 主线程
### MDL 元数据锁
### memcached 不译
### merge 合并
### metadata lock 元数据锁
### metrics counter 计数器
### midpoint insertion strategy 一种缓存算法，不译
### mini-transaction 迷你事务
### mixed-mode insert 混合模式插入
### .MRG file .MRG文件
### multi-core 多核
### multiversion concurrency control 多版本并发控制
### mutex 互斥
### MVCC 多版本并发控制
### my.cnf 配置文件（Unix/Linux）
### my.ini 配置文件（Windows）
### .MYD file .MYD文件
### .MYI file .MYI文件
### mysql mysql（客户端）
### MySQL Enterprise Backup MySQL企业备份
### mysqlbackup command mysqlbackup命令
### mysqld MySQL daemon（Unix）或MySQL service（Windows）
### mysqldump mysqldump命令

## N ##
### natural key 自然主键
### neighbor page 相邻页
### next-key lock 行间隙锁
### non-blocking I/O 同AIO
### non-locking read 不加锁读
### non-repeatable read 非重复读
### normalized （符合）范式的
### NoSQL 不译
### NOT NULL constraint 非空约束
### NULL 空

## O ##
### off-page column 跨页列
### OLTP 在线联机查询
### online 在线
### online DDL 在线DDL
### .OPT file .OPT文件
### optimistic 乐观锁
### optimizer 优化器
### option 选项
### option file 选项文件
### overflow page 溢出页

## P ##
### page 数据页
### page cleaner 页清理器（页清理线程）
### page size 数据页大小
### .PAR file .PAR文件
### parent table 父表
### partial backup 部分备份
### partial index 部分索引
### Performace Schema 性能库
### persistent statistic 持久统计
### pessimistic 悲观锁
### phantom 幻（读）
### physical 物理
### physical backup 物理备份
### PITR 定点恢复
### plan stability 执等计划稳定性
### plugin 插件
### point-in-time recovery 定点恢复
### prefix 前缀
### prepared backup 一致备份
### primary key 主键
### process 进程
### pseudo-record 伪记录
### Pthread Posix threads 不译
### purge 清除
### purge buffering 清除缓冲
### purge lag 清除链表
### purge thread 清除线程

## Q ##
### query 查询
### query execution plan 查询执行计划 
### query log 查询日志
### quiesce 系统静默

## R ##
### RAID 磁盘阵列
### random dive 随机取样
### raw backup 原始备份
### READ COMMITTED 隔离级别，不译 
### READ UNCOMMITTED 隔离级别，不译
### read view MVCC在内核中用到的一个快照模式 
### read-ahead 预读
### read-only transaction 只读事务
### record lock 行锁
### redo 重做，不译
### redo log 重做日志，不译
### redundant row format 冗余行格式，innodb的一种行的存储格式，不译
### referential integrity 参照完整性 
### relational 关系
### relevance 相关性
### REPEATABLE READ 隔离级别，不译
### replication 复制
### restore 恢复
### rollback 回滚
### rollback segment 回滚段
### row 行
### row format 行格式
### row lock 行级锁
### row-based replication 行复制
### row-level locking 行级锁
### rw-lock 读写锁

## S ##
### savepoint 保存点
### scalability 可扩展性
### scale out 水平扩展 
### scale up 垂直扩展
### schema 数据库（仅MySQL）
### search index 搜索索引
### secondary index 二级索引
### segment 段
### selectivity 选择性
### semi-consistent read 半一致性读
### SERIALIZABLE 隔离级别，不译
### server 服务器
### shared lock 共享锁
### shared tablespace 共享表空间
### sharp checkpoint 清晰检查点
### fuzzy checkpoint 模糊检查点
### shutdown 关闭
### slave server 从服务器
### slow query log 慢查询日志
### slow shutdown 慢关闭
### snapshot 快照
### space ID 空间ID
### spin 自旋（锁） 
### SQL 结构化查询语言
### SSD 固态驱动器
### startup 启动
### statement-based replication 语句复制 
### statistics 统计信息
### stemming 词干
### stopword 停用词
### storage engine 存储引擎
### strict mode 严格模式
### sublist 子列表
### supremum record 最小上界记录
### surrogate key 代理主键,区别于自主ID产生的自然键值
### system tablespace 系统表空间

## T ## 
### table 表
### table lock 表级锁
### table scan 全表扫描
### table type 表（引擎）类型
### tablespace 表空间
### tablespace dictionary 表空间数据字典
### temporary table 临时表
### temporary tablespace 临时表空间
### text collection 文本集合 
### thread 线程
### torn page 残缺页
### TPS 每秒事务，不译
### transaction 事务
### transaction ID 事务ID
### transportable tablespace 可传输表空间 
### .TRG file 触发器参数文件
### .TRN file 触发器命名空间信息文件
### troubleshooting 故障排除
### truncate 删节
### tuple 元组
### two-phase commit 两段式提交

## U ##
### undo 撤销，不译
### undo buffer undo缓冲，不译
### undo log undo 日志，不译
### undo tablespace undo 表空间
### unique constraint 唯一约束
### unique index 唯一索引
### unique key 唯一键

## V ##
### victim 牺牲（死锁检测，牺牲影响最少行的事物） 

## W ##
### wait 等待
### warm backup 热备
### warm up 预热
### Windows 不译
### workload 工作负载
### write combining 合并写

## X ##
### XA XA

## Y ##
### young InnoDB Buffer Pool 通过LRU算法管理页面的替换策略。LRU List按照功能被划分为两部分：LRU_young 与LRU_old.
