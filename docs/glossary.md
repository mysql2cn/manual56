# MySQL专业词汇表 #

这些术语在MySQL数据库服务器中经常被用到。此词汇表源于InnoDB存储引擎的专业术语手册，并且主要的释义都是InnoDB相关的。

## <a name="A"></a>A ##
### <a name='glos_acid' /></a>ACID: ACID 
原子性(atomicity).  一致性(consistency). 隔离性(isolation)和持久性(durability)的首字母缩写。这些属性是一个数据库系统全部具备的，并且与事务(***transaction***)的概念紧紧绑在一起。InnoDB的事务特性遵守ACID原则。

事务是可以提交或回滚的原子(***atomic***)工作单元。当一个事务造成数据库的多处更改，所有的更改要么在事务提交(***committed***)后全部成功，要么在事务回滚(***rolled back***)后全部撤消。

数据库在任何时候都处于一致的状态——在每一次提交或回滚后，以及事务在进行中时。如果相关的数据正在被跨表更新，查询看到的是所有的旧值或所有的新值，而不会是新旧兼有的。

当事务在进行时它们之间是被保护(被隔离)的；它们之间不能互相干涉或看到其它事务未提交的数据。这种隔离是靠锁(***locking***)机制实现的。有经验的用户可以调整隔离级别(***isoloation level***)，当他们可以确认事务真的不会相互干涉时，牺牲少许保护换取性能和并发(***concurrency***)的提升。

事务的结果是持久的：一旦提交操作成功了，在掉电. 系统崩溃. 资源竞争或其它非数据库应用所引起的潜在危险等情况下，事务引起的更改是安全的。持久性通常需要写到磁盘存储上，具有一定冗余量来防止在写操作过程中的掉电故障或软件崩溃。(在InnodDB中，双写缓冲(***doublewrite buffer***)来帮助完成一致性。)

参见 [atomic], [commit], [concurrency], [doublewrite buffer], [isolation level], [locking], [rollback], [transaction].

### <a name='glos_adaptive_flushing'></a>adaptive flushing: 自适应刷新
一个***InnoDB***用来平滑处理由检查点(***checkpoints***)产年的I/O压力的算法。MySQL周期性地将小集合的修改了的页面(***pages***)刷新(***flushing***)到数据文件(***data files***)中，而不是一次性将所有修改过的页从缓冲池(***buffer pool***)中刷新到数据文件。自适应刷新算法通过基于刷新率和redo信息产生的速率，估计出执行周期刷新的最佳值，而扩展了这个进程。它在MySQL 5.1的InnoDB插件中第一次被提到。

参见 [buffer pool], [checkpoint], [data files], [flush], [InnoDB], [page], [redo log].

### <a name='glos_adaptive_hash_index'></a>adaptive hash index: 自适应哈希索引
是一个通过在内存中构建哈希索引(***hash index***)来加速对InnoDB的表=和IN查找操作的优化。MySQL监视InnoDB表的索引查询，如果查询更适合哈希索引，它会为被频繁访问到的索引页(***pages***)自动创建一个哈希索引。从某种意义上讲，自适应哈希索引实时地配置MySQL，以利用大内存的优势，这样做更接近于内存数据库的架构。这个特性由[innodb_adaptive_hash_index]()这个选项控制。因为这个功能只对部分负载有好处，并且***buffer pool***中哈希索引所用过的内存也被保留了，所以你对这个功能权衡取舍。

哈希索引创建一直是基于已存在的InnoDB的以B树(***B-tree***)结构组织的二级索引(***secondary index***)。根据使用索引搜索模式的不同，MySQL可以在任何长度的B树键值前缀上构建哈希索引。一个哈希索引可以是部分的；整个B树没必要全缓存在buffer pool中。

在MySQL 5.6或更高的版本中，另一种利用InnoDB表快速单值查询优势的方法是在InnoDB中使用***memcached***的接口。结节参见[第14.2.9节，InnoDB集成memcached](14.02.09)

参见 [B-tree], [buffer pool], [hash index], [memcached], [page], [secondary index].

### <a name='glos_ahi'></a>AHI: adaptive hash index的缩写
adaptive hash index的缩写。

参见 [adaptive hash index]。

### <a name='glos_aio'></a>AIO: 异步IO
异步I/O(asynchronous I/O)的缩写。你会在InnoDB的消息或关键字中看到它。

参见 [asynchronous I/O]。

### <a name='glos_antelopoe'></a>Antelope: 不译，innodb code name
原始InnoDB文件格式的代码名称。它支持冗余(***redundant***)与精简(***compact***)的行格式，但是不支持新的***Barracuda***代码中的动态(***dynamic***)与压缩(***compressed***)行格式。

如果你的应用能受益于InnoDB表压缩，或使用BLOBs或大文本字段时能从动态行格式中获益，你可以将表切到Barracuda格式。你可以通过在创建表之前设置[innodb_file_format]选项来选择使用何种文件格式。

参见 [Barracuda], [compact row format], [compressed row format], [dynamic row format], [file format], [innodb_file_format], [redundant row format].

### <a name='glos_application_programming_interface'></a>application programming interface: API
一个函数或程序集合。一个API为函数. 程序. 参数和返回值提供一组稳定名字与类型。

### <a name='glos_apply'></a>apply: 应用
当一个MySQL企业版备份(MySQL Enterprise Backup)在数据库运行时生成的备份并没有包含最新的修改时，更新备份文件以包含这些改动的过程程就被称为应用(***apply***)步骤。它由`mysqlbackup`命令的`apply-log`选项指定。

在改动被应用前，我们把文件称为原始备份(***raw backup***)。在改动被应用后，我们把文件称为一致备份(***prepared backup***)。改动记录在***ibbackup_logfile**文件中；一旦应用步骤完成，这些文件就没啥用了。

参见 [hot backup], [ibbackup_logfile], [MySQL Enterprise Backup], [prepared backup], [raw backup].

### <a name='glos_arm_file'></a>.ARM file: 不译 Archive表的定义信息
Archive表的定义信息。相对于.ARZ文件。这个后缀的文件总是包含由MySQL企业版备份mysqlbackup命令所产生的备份中。

参见 [.ARZ file], [MySQL Enterprise Backup], [mysqlbackup command].

### <a name='glos_arz_file'></a>.ARZ file: 不译 Archive表的数据文件
Archive表的数据文件。相对于.ARM文件。这个后缀的文件总是包含由MySQL企业版备份mysqlbackup命令所产生的备份中。

参见 [.ARM file], [MySQL Enterprise Backup], [mysqlbackup command].

### <a name='glos_asynchronous_io'></a>asynchronous I/O: 异步I/O，也可说AIO
一种允许其它操作可以在I/O完成之前继续的I/O操作类型。也叫无阻塞I/O，简写为AIO。InnoDB在某些可以运行并行操作但不影响数据库准确性的操作上使用这种I/O类型，比如把那些实际上没有访问到但马上就要被访问到的页读进buffer pool中。

从历史上来看，InnoDB曾经只在Window系统上使用过异步I/O。从InnoDB Plugin 1.1 开始，InnoDB在Linux系统上也使用了异步I/O。这个改变对libaio产生依赖。在其它类Unix系统上，InnoDB只使用同步I/O。

参见 [buffer pool], [non-blocking I/O].

### <a name='glos_atomic'></a>atomic: 原子(性)
在SQL的环境中，事务是要么完全生效(当提交后)，或完全无效(当回滚后)的工作集。这个不可分割(“原子”)的属性就是缩写***ACID***中的“A”。

参见 [ACID], [commit], [rollback], [transaction].

### <a name='glos_atomic_instruction'></a>atomic instruction: CPU中不可中断的指令(原子指令)
CPU提供的特殊机制，用来保证关键的低层操作不被打断。

### <a name='glos_auto_increment'></a>auto-increment: 自增
一个在列上自动添加递增序列值的表的列属性(用`AUTO_INCREMENT`关键字指定)。InnoDB只支持主键列上的自增。

它会节省开发者的工作量，在插入新行时不必再生成新的唯一值。它为查询分析器提供很有用的信息，因为列已知是非空且值唯一。这样的列上值可以在各种环境中用做查询键，并且因为它们是自动生成的，所以根本没有必要改动它们；正因如此，主键列常常被定义为自增。

自增万会对基于语句的复制(***statement-based replicataion***)带来麻烦， 因为在从库上同步过去的语句不一定会生成与主库上一致的列值，这要归咎于计时问题。当你有一个自增主键，你只能在`innodb_autoinc_lock_mode=1`的情况下使用基于语句的复制。如果你设置了`innodb_autoinc_lock_mode=2`，它会允许高并发的插入操作，请使用基于行的复制(***row-based replication***)而不要使用基于语句的复制。`innodb_autoinc_lock_mode=0`是之前的(传统的)默认设置，但只有遇到兼容性问题时才会使用该设置。

参见 [auto-increment locking], [innodb_autoinc_lock_mode], [primary key], [row-based replication], [statement-based replication].

### <a name='glos_auto_increment_locking'></a>auto-increment locking: 自增锁
自增(`auto-increment`)主键在带来方便会引起对并发性能上的权衡。在最简单的情况，如果一个事务正在往表里插值，其它的事务必须等待各自的插表，为的是让第一个事务插入的行能够获得连续的键值。InnoDB包含一些优化以及`innodb_autoinc_lock_mode`选项，这样你就可以选择如何在可预测的自增序列值与最大并发(`concurrency`)插入之间做出取舍。

参见 [auto-increment], [concurrency], [innodb_autoinc_lock_mode].

### <a name='glos_autocommit'></a>autocommit: 自动提交
使在每句SQL语句后产生提交(`commit`)操作的选项。在InnoDB表中使用跨多条`SQL`语句的事务(`transactions`)的情况下，不推荐这个模式。它会帮助提高InnoDB表只读的事务(`read-only transactions`)，这儿会将锁(`locking`)的负载和产生的`undo`数据最小化，特别是在MySQL 5.6.4及更高版本中。它同样适用于事务不起作用的MyISAM表。

参见 [commit], [locking], [read-only transaction], [SQL], [transaction], [undo].

### availability 可用性
对MySQL. 操作系统或硬件故障及因为维护行为而引起宕机等主机故障的处理能力，以及在必要情况下从上述所有故障中恢复的能力。经常与扩展性(`scalability`)配合使用，成为大规模部署中的一个关键因素。

参见 [scalability].

## <a name='B'></a>B ##

### <a name='glos_b_tree'></a>B-tree: B树
数据库索引上很流行使用的树形数据结构。该数据结构一直保持排序状态，保证快速精确查找(等于操作)和范围查找(比如大于. 小于和BETWEEN操作)。这种类型的索引在绝大多数的存储引擎中是可用的，如InnoDB和MyISAM。

因为B树的节点可以有很多子节点，所以B树和二叉数不同，二叉树的节点最多有两个子节点。

哈希索引(***hash index***)与它的差别是，哈希索引只在内存存储引擎中可用。内存存储引擎也可以使用B树索引，如果查询中用到了范围查找操作，你可以为内存表选用B树索引。

参见 [hash index].

### <a name='glos_backticks'></a>backticks: 反引号
MySQL SQL语句中的标识如果含有特殊字符或保留词，就必须用反引号(`)括起来。例如，为了使用名为`FOO#BAR`的或名为`SELECT`列，你就要把这些标识符指定为\`FOO#BAR\`和\`SELECT\`。由于反引号提供一种额外的安全级别，它们被广泛使用的程序生成的SQL语句，其中的标识符名称可能不会提前知道。

其它的数据库系统使用双引号(")将这样的特殊名字包围起来。为了移植性起见，你可以在MySQL启用ANSI_QUOTES模式并用双引号来代替反引号来限定标识符名称。
参见 [SQL].

### <a name='glos_backup'></a>backup: 备份
为了安全保存起见，拷贝MySQL实例部分或全部表的数据和元数据的过程。也指拷备完成的文件集合。这是DBA们的一项终极任务。这个过程的反向操作是恢复(***restore***)。

对于MySQL，物理备份(***physical backup***)由MySQL企业版备份(***MySQL Enterprise Backup***)产品来完成，逻辑备份(***logical backup***)由***mysqldump***命令来完成。这些技术所产生备份数据在文件大小与文件结构以及速度(特别是恢复操作的速度)等方面都有不同的特性。

热备(***hot backup***). 温备(***warm backup***)和冷备(c***old backup***)因它们干涉数据库操作的多少而有很大不同。(热备最少干涉，冷备最多。)

参见 [cold backup], [hot backup], [logical backup], [MySQL Enterprise Backup], [mysqldump], [physical backup], [warm backup].

### <a name='glos_barracda'></a>Barracda: Innodb code name
支持表压缩的InnoDB文件格式的代码名。这种文件格式首先是在InnoDB Plugin中提到的。它提供压缩行格式实现InnoDB的表压缩，提供动态行格式来提高BLOB和大文本字段的存储分布。你可以通过innodb_file_format选项来选择使用。

因为InnoDB系统表空间是以原始的Antelope文件格式存储的，所以要使用Barracuda文件格式时，你必须要启用file-per-table选项，它会讲最新创建表的表空间从系统表空间中隔离出来。

MySQL企业版备份产品的3.5版及以上版本支持用Barracuda文件格式来备份表空间。

参见 [Antelope], [compact row format], [compressed row format], [dynamic row format], [file format], [file-per-table], [innodb_file_format], [MySQL Enterprise Backup], [row format], [system tablespace].

### <a name='glos_beta'>beta: 公测
软件产品生命周期中早期阶段，彼时它只用来评估，经常是没有定义发行号或发行号小于1。InnoDB没有用beta名称，而更喜欢用可以扩展为几次发布的测试版来演进为一个GA版。

参见 [early adopter], [GA].

### <a name='glos_binary_log'></a>binary log: 二进制日志
包含所有尝试修改表数据的语句记录的文件。这些语句可以是为更新从库(replication)副本而重放了的，也可以是从一个备份中恢复表数据后产生的。你可以将记录二进制日志的功能打开或闭，虽然Oracle建议你在用复制或备份时一直打开它。

你可以通过mysqlbinlog命令来检查二进制日志的内容，或将这些语句在复制或恢复时重放。如需更多二进制日志的信息，参考[第5.2.4章，二进制日志][05.02.04]。如需更多MySQL中二进制日志相关的配置选项，参考[16.1.4.4章，二进制选项与变量][16.01.04.04]。

对于MySQL企业备份(***MySQL Enterprise Backup***)产品，二进制日志的文件名和文件中的当前位置是非常重要的细节。你可以用`--slave-info`选项来让在复制环境下的备份文件记录主库的信息。

在MySQL 5.0 之前的版本中有一个类似的功能叫更新日志(update log)。在MySQL5.0及更高版本中，二进制日志代替了更新日志。

参见 [binlog], [MySQL Enterprise Backup], [replication].

### <a name='glos_binlog'></a>binlog: 二进制日志(同binary log)
二进制日志(***binary log***)的俗称。例如，你会在邮件消息或论坛话题中看到这个简写。

参见 [binary log].

### blind query expansion: 使用query expansion
一种使用`WITH QUERY EXPANSION`短语激活的全文搜索的特殊模式。它会执行两次搜索，第二次的搜索的短语是由第一次搜索结果中少数几个高度关联的文档拼成的。这种技术主要用在短词搜索上，很有可能只有一个词。它能发现那些搜索项并没有在文档中明确出现但有关联的匹配。

参见 [full-text search].

### <a name='glos_bottleneck'></a>bottleneck: 瓶颈
系统中大小或能力受限的部分，它会影响限制整个系统的吞吐量。比如，内部可能比实际需要的少；访问一个必需的资源可能会阻止多个CPU内核同时运行；或等待硬盘I/O完成可能会阻止CPU的满负荷运行。干掉瓶颈往往是提高并发(***concurrency***)。例如，多个InnoDB ***buffer pool***实例的功能减少了多个会话同时读写buffer pool时的资源竞争。

参见 [buffer pool], [concurrency].

### <a name='glos_bounce'></a>bounce: 性能抖动
重启之后的紧跟着出现的关闭(***shutdown***)。理想情况是提前做一个预热，这样性能和吞吐量会很快恢复到一个较高水平。

参见 [shutdown].

### <a name='glos_buddy_allocator'></a>buddy allocator (Innodb buffer pool内存分配中的单位)
InnoDB ***buffer pool***管理不同大小***pages***的机制。

参见 [buffer pool], [page], [page size].

### <a name='glos_buffer'></a>buffer: 缓冲(或不译)
一个用来做临时存储的内存或磁盘空间。数据被缓存在内存中，以便更高效地写磁盘(使用少而大的I/O操作代替多而小)。数据缓存在磁盘上以获得更高的可靠性，这样即使在极端情况下发生崩溃或其它故障发生时也可以恢复。InnoDB主要的缓冲类型就是***buffer pool***. ***doublewrite buffer***和***insert buffer***。
参见 [buffer pool], [crash], [doublewrite buffer], [insert buffer].

### <a name='glos_buffer_pool' /></a>buffer pool: 缓冲池 (或不译)
保持缓存了的InnoDB表和索引的内存区域。为了获得高容量的读操作的效率，buffer pool被分为页页(***page***)以持有多行。为了获得更高缓存管理的效率，buffer pool实现为一个页面链接；很少使用的数据利用***LRU***算法的变体从将其老化并从缓存中剔出。在大内存的系统中，你可以通过将buffer pool分割为多个buffer pool实例(***buffer pool instance***)来提高并发。

好几种`InnoDB`的状态变量. `information_schema`表及`performance_schema`表都能帮助你监测buffer pool的内部工况。自MySQL 5.6始，你还可以在通过诸如`innodb_buffer_pool_dump_at_shutdown`和`innodb_buffer_pool_load_at_startup`的InnoDB的配置变量，在启动和关闭服务时导出或恢复buffer bool中的内容，也可以在任何时间手工操作。

参见 [buffer pool instance], [LRU], [page], [warm up].

### <a name='glos_buffer_pool_instance'></a>buffer pool instance: 缓冲池实例(或不译)
在buffer pool中划分的任何区域，由innodb_buffer_pool_instances配置控制。由innodb_buffer_pool_size指定的总内存大小在被所有的实例瓜分。通常情况下，系统分配给InnoDB buffer pool好多个GB情况下，才适合用多buffer pool instances(每个实例1GB或更大)。在系统在多个并发会话环境下从buffer pool中加载或查寻大量的数据时，利用多实例可以降低对管理buffer pool的数据结构的排它访问竞争。

参见 [buffer pool].

### <a name='glos_built_in'></a>built-in: 内置
The built-in InnoDB storage engine within MySQL is the original form of distribution for the storage engine. Contrast with the ***InnoDB Plugin***. Starting with MySQL 5.5, the InnoDB Plugin is merged back into the MySQL code base as the built-in InnoDB storage engine (known as InnoDB 1.1).

MySQL中内置的InnoDB存储引擎是存储引擎发布的原始形态。相对于InnoDB Plugin而言。自MySQL 5.5始，InnoDB Plugin又合并回MySQL代码中成为内置的InnoDB存储引擎(也就是InnoDB 1.1)。

这在MySQL 5.1中的区别还是蛮大的，功能与bug可能会应用到InnoDB Plugin而不是内置的InnoDB中，反之亦然。

参见 [InnoDB], [plugin].

### <a name='glos_business_rules'></a>business rules: 业务规则
规范商业软件基础行为的关系和序列，用于运作一个商业公司。有时这些规则由法律决定，有时由公司政策决定。小心规划保证关系由数据库编码与加强，并且行为通过应用逻辑来执行，精确反应出公司的真实政策并能处理现实生活中的情况。

例如，一个员工离职可能会触发一系列人力资源部门的行为。人力资源数据库也可能具备能描述一个已受雇但尚未开始工作的员工数据的灵活性。在一个在线服务中关闭一个账户可能会导致数据从数据库中删除，或数据被移走或被标志以便以后在该账户重新启用时恢复。一个公司可能要制定政策除了要考虑如工资不能为负数等合理性检查之外，还要考虑工资的最大值. 最小值及如何调整等。一个零售业数据库可能不允许相同序列号被返回一次以上的采购，或当. 不允许信用卡购买超过某个金额，而一个用来检测欺诈行为的数据库则允许这些行为。

参见 [relational].

## <a name="C"></a>C ##

### <a name='glos_cache'></a>cache: 缓存
存储被频繁或高速检索的数据拷贝的内存区域的常规叫法。在InnodB中，最主要的缓存结构体为***buffer pool***。

参见 [buffer], [buffer pool].

### <a name='glos_cardinality'></a>cardinality: 基数
表的列中不同值的数目。当一个查询引用到一些有索引(***index***)的列时，每个列的基数会影响到哪种访问方式是最有效的。例如，对于一个有唯一约束(***unique constraint***)的列，不同值的数目就等于表里的行数。如果一个表里有一百万行数据但某列只有10个不同的值，每到一个值会(平均)出现十万次。像`SELECT c1 FROM t1 WHERE c1 = 50; `这样的查询，有可能返回一行，也有可能返回巨多行，数据库服务也可能会根据c1的基数来有区别地执行这个查询。

如果列中的值分布不是很均匀，依靠基数来决择最优执行计划并不是个好方法。例如，`SELECT c1 FROM t1 WHERE c1 = x; `有可能当x=50时返回一行，而在x=30时返回一百万行。在这种情况下，你可能需要使用索引提示(***index hint***)来传递哪种方式对此类特定的查询更有效一些。

基数也适用于多个列中的不同值的数量，比如在组合索引中。

对于InnoDB，评估索引基数的进程会受[innodb_stats_sample_pages]和[innodb_sttas_on_metadata]配置选项的影响。评估值在持久统计([persisitent statistics])启用的情况下会更稳定一些(在MySQL 5.6及以上版本中)。

参见 [column], [composite index], [index], [index hint], [persistent statistics], [random dive], [selectivity], [unique constraint].

### <a name='glos_cfg'></a>.cfg file: .cfg文件，或不译
`InnoDB`可传输表空间(***transportable tablespace***)特性所用到的元数据文件。它是由`FLUSH TABLES ... FOR EXPORT`命令产生的，这条语句将一个或多个表置到一个统一的状态，这样它们可以被拷贝到其它服务器。.`cfg`文件会随着`.ibd`文件一起拷贝，并且常常在`ALTER TABLE ... IMPORT TABLESPACE`阶段会调整`.ibd`文件内部的值，比如 ***space ID***。

参见 [.ibd file], [space ID], [transportable tablespace].

### <a name='glos_change_buffer'></a>change buffer：变更缓冲区
一个记录二级索引(***secondary indexes***)中页(***pages***)上变化的特殊的数据结构。这些值可能是用SQL中的`INSERT`. `UPDATE`或`DELETE`语句(***DML***)引起的。这些特性加上变更缓冲区叫做变更缓冲，由插入缓冲(***insert buffer***). 删除缓冲(***delete buffer***)和清除缓冲(***purge buffer***)组成。

当不在buffer pool中的二级索引中的相关页发生时，变更只被记录在变更缓冲区中。当相关的索引页被加载到buffer pool中且关联的变更还在变更缓冲区中时，这些page的变更会利用变更缓冲区中的数据应用到buffer pool(***merged***)中。在系统几近空闲或在缓慢关机时，清除(***purge***)操作会周期性地执行，将新的索引页写到硬盘上。清除操作可以将一个序列的索引值一起写到硬盘块中，这样做比将每一个值立即写到硬盘上要更有效。

从物理角度看，变更缓冲区是系统表空间(***system tablespace***)中的一部分，所以在数据库重启过程中索引的变更是被保持缓冲的。变量只有在页面因为其它读操作而被加载到buffer pool中时才会被应用(***merged***)。

存储在变更缓冲区中的数据的数量与类型由[innodb_change_buffering]和[innodb_change_buffer_max_size]配置选项来决定。要观察关于当前变更缓冲区中的数据，可以执行[SHOW ENGINE INNODB STATUS]命令。

以前叫插入变更区(***insert buffer***)。

参见 [buffer pool], [change buffering], [delete buffering], [DML], [insert buffer], [insert buffering], [merge], [page], [purge], [purge buffering], [secondary index], [system tablespace].

### <a name='glos_change_buffering'></a>change buffering: 变更缓冲
有关变更缓冲区(***change buffer***)功能的总称，由插入缓冲(***insert buffering***. 删除缓冲(***delete buffering***)和清除缓冲(***purge buffering***)构成。索引变更是由SQL语句引起，通常会带来随机I/O操作，变更会被“憋住”并用后台线程(***thread***)来周期性地执行。这种顺序操作可以将一个序列的索引值一起写到硬盘块中，这样做比将每一个值立即写到硬盘上要更有效。由[innodb_change_buffering]和[innodb_change_buffer_max_size]配置选项控制。

参见[change buffer], [delete buffering], [insert buffering], [purge buffering].

### <a name='glos_checkpoint'></a>checkpoint: 检查点
当缓存在***buffer pool***中的数据页被变更后，这些变更会在晚些时候写入到数据文件(***date files***)中，这个过程叫刷新(***flushing***)。检查点就是记录最后更改被成功写入到数据文件的位置(由***LSN***值来表示)。

参见 [buffer pool], [data files], [flush], [fuzzy checkpointing], [LSN].

### <a name='glos_checksum'></a>checksum: 校验
`InnoDB`中一个用来监测表空间(***tablespace***)中的一个页(***page***)从磁盘读入到InnoDB buffer pool中时是否正确的验证机制。这个特性可以通过[innodb_checksum]配置选项来开关。在MySQL 5.6中，你也可以通过指定配置选项`innodb_checksum_algorithm=crc32`来快速启用校验。

[innochecksum]命令在MySQL服务在关闭的情况下通过测试指定的表空间(***tablespace***)文件的校验值来帮助诊断损坏的问题。

MySQL也可以使用出于复制目的来做校验。如需更多细节，参考配置选项[binlog_checksum]，[master_verify_checksum]和[slave_sql_verify_checksum]。
[innodb_checksum][binlog_checksum]，[master_verify_checksum]和[slave_sql_verify_checksum]
参见 [buffer pool], [page], [tablespace].

### <a name='glos_child_table'></a>child table: 子表
在一个外键(***foreign key***)关系中，一个表中的行用指定列中相同的值引用(或指向)了另一个表中行，前者就是子表。这个表用`FOREIGN KEY ... REFERENCES`子句来约束，用`ON UPDATE`和`ON DELETE`子句来配置。父表(***parent table***)中对应的行在子表的行可以创建之前必须存在。子表中的值可以阻止对父表删除或更新操作，或可以基于在创建外键时的ON CASCADE的选项来引发子表中自动删除或更新操作。

参见 [foreign key], [parent table].

### <a name='glos_clean_page'></a>clean page: 干净的页
InnoDB ***buffer pool***中，一个页中所有在内存中产生的变更都被写到(刷新到)数据文件(***date files***)时，这个页就叫干净的页。对应脏页(dirty page)。

参见 [buffer pool], [data files], [dirty page], [flush], [page].

### <a name='glos_clean_shutdown'></a>clean shutdown: 完成buffer刷新的关闭
在没有任何错误并且所有的变更在关闭之前都被应用到InnoDB表中的情况下的关闭(shutdown)，相对的是崩溃或快速关闭(***fast shutdown***)。是慢关闭(***slow shutdown***)的同义词。

参见 [crash], [fast shutdown], [shutdown], [slow shutdown].

### <a name='glos_client></a>client: 客户端
发送请求到服务器，并解释或处理结果的一种程序类型。客户端软件只能运行一段时间(如邮件或聊天软件)，可能以交互方式运行(如`mysql`命令处理器)。

参见 [mysql], [server].

### <a name='glos_clustered_index'></a>clustered index: 聚集索引
InnoDB主键(***primary key***)索引术语。InnoDB表存储是基于主键列中的值来组织的，用来加速涉及主键列的查询与排序。为了得到最优性能，请基于最关键性能的查询谨慎选择主键列。因为修改聚集索引是一个非常昂贵操作，请选择很少或从来不被修改的列为主键列。

在Orcale的数据库产品中，这种表的类型被称为索引组织的表(***index-organized table***)。

参见 [index], [primary key], [secondary index].

### <a name='glos_cold_backup'></a>cold backup: 冷备份
数据库在关闭状态下生成的备份(***backup***)。对于比较忙的应用和网站，这可能不太现实，你可以选择温备(***warm bakcup***)或热备(***hot bakcup***)。

参见 [backup], [hot backup], [warm backup].

### <a name='glos_column'></a>column: 列
一行(***row***)中的一个数据项，它的存储和语义用数据类型来定义。每张表(***table***)和索引(***index***)主要由它所包含的列集来定义。

第一列都有一个基数(***cardinality***)值。一个列可以是这个表的主键(***primary key***)，也可以是主键的一部分。一个列可以受到唯一约束(***unique constraint***). 非空约束(***NOT NULL constraint***)，或两者共同约束。不同列中的值，即使在不同的表中，也可以用外键(***foreign key***)关系来联系起来。

在讨论MySQL内部操作时，有时也用别名字段(***field***)来代替。

参见 [cardinality], [foreign key], [index], [primary key], [row], [SQL], [table], [unique constraint].

### <a name='glos_column_index'></a>column index 单列索引
在单列上加的索引(***index***)。

参见 [composite index], [index].

### <a name='glos_column_prefix'></a>column prefix: 列的前缀
当一个索引在创建时指定了长度，如`CREATE INDEX idx ON t1 (c1(N))`，只有这个列中值的前N个字符会被存储到索引中。保持小的索引前缀会使得索引精简，同时内存与磁盘I/O节省，有助于提高性能。(不过索引前缀太小的话，进入查询优化器的不同值的行会重复，所以会妨碍查询优化)。

对于含有二进制或大文本字符串的字段，排序不是主要的考虑因素，把全部的值都存到索引中会浪费空间，索引会自动使用前N(一般来说是768)个字符来做查询与排序。

参见 [index].

### <a name='glos_commit'></a>commit: 提交
一个用来结束一个事务(***transaction***)的***SQL***语句，使得任何事务产生的变更持久化。与它相对的是回滚(***rollback***)，它会将任何事务产生的变更撤销。

InnoDB为提交使用了乐观(***opimistic***)机制，这样变更在提交操作真正发生之前可以写进数据文件中。这个技术让提交本身变得比较快，但代价是回滚操作需要多花些开销。

默认情况下，MySQL使用自动提交设置，它可以在每一条SQL语句执行之后自动执行提交。

参见 [autocommit], [optimistic], [rollback], [SQL], [transaction].

### <a name='glos_compact_row_format'></a>compact row format: 紧凑(compact)的行格式
MySQL 5.0.3之后InnoDB默认的行格式(***row format***)。对于使用Antelope文件格式(***Antelope file format***)的表有效。相较于之前默认的文件格式(***redundant row format***)，它在空值和变长字段方面有体现得更紧凑一些。

因为B树(***B-tree***)索引在InnoDB中按行查询很快，所以就算是将所有行都保持相同大小，带来的性能提升也只是一点点。

参见 [Antelope], [file format], [redundant row format], [row format].

### <a name='glos_composite_index'></a>composite index: 复合索引
包含多列的索引。

参见 [index], [index prefix].

### <a name='glos_compressed_backup'></a>compressed backup: 压缩备份
MySQL企业备份产品(***MySQL Enterprise Backup***)的一个压缩属性，它为每一个表空间生成一个压缩拷贝，并把后缀名从`.ibd`改为`.ibz`。压缩备份数据可以让你本机保留更多备份，并且节省将备份传输到其它服务上的时间。数据在恢复操作中解压。当压缩备份操作一个已经压缩过的表时，它会跳过对这个表的压缩步骤，因为再次压缩对空间的节省可能只是一小点或没有。

由MySQL企业备份产品(***MySQL Enterprise Backup***)生成的文件集，里面每个表空间(***tablespace***)都是压缩过的。压缩过的文件以`.ibz`后缀重命名。

备份从一开始就使用压缩有助于避开压缩过程中存储开销，同时可以避开往其它服务器上传输时的网络开销。应用(***apply***)二进制日志(***binary log***)的过程需要更多时间，并需要解压备份文件。

参见 [apply], [binary log], [compression], [hot backup], [MySQL Enterprise Backup], [tablespace].

### <a name='glos_compressed_row_format'></a>compressed row format: 压缩的行格式
一种可以让InnoDB表中数据和索引压缩的行格式(***row format***)。它做为***Barracuda***文件格式的一部分，在InnoDB Plugin中被引入。大字段从存储剩下字段的页中被隔离存储，如动态行格式(***dynamic row format***)。索引页和大字段都被压缩，节省了内存与磁盘。根据数据结构的不同，内存和磁盘使用量上的减少的好处是否能超过解压这些文件带来的性能开销还不好说。使用细节参见第[14.2.8节，`InnoDB`压缩表](14.02.08)。

参见 [Barracuda], [compression], [dynamic row format], [row format].

### <a name='glos_compression'></a>compression: 压缩
是一个使用更少磁盘空间. 执行更少I/O和使用更少用来缓存的内存的等好处多多的特性。InnoDB的表和索引数据可以在数据库操作过程中保持压缩格式。

当查询需要时数据被解压，当被***DML***操作改变时被重新压缩。当你对某个表启用了压缩了，这个过程对用户和应用开发者来说是透明的。DBA可以查阅***information_schema***表来监控压缩的参数是如何为MySQL实例和特定的压缩表提供工作效率的。

当InnoDB表被压缩了，表(***table***)本身. 所有关联的索引(***index***)以及加载到***buffer pool***中的页都会被压缩。压缩不会被应用到***undo buffer***中的页中。

表压缩特性需要MySQL 5.5或更高版本，或InnoDB Plugin 5.1或更早版本，并且使用***Barracuda***文件格式和压缩行格式来创建表(***innodb_file_per_table***选项要打开)。对每个表的压缩是受`CREATE TABLE`和`ALTER TABLE`语句的`KEY_BLOCK_SIZE`子句的影响。在MySQL 5.6及更高版本中，压缩也受服务范围的配置参数`innodb_compression_failure_threshold_pct`. `innodb_compression_level`和`innodb_compression_pad_pct_max`的影响。使用细节参考[第14.2.8节，`InnoDB`压缩表](14.02.08)。

另一种压缩类型是压缩备份(***compression buckup***)，是MySQL企业备份产品的特性。

参见 [Barracuda], [buffer pool], [compressed row format], [DML], [hot backup], [index], [INFORMATION_SCHEMA], [innodb_file_per_table], [plugin], [table], [undo buffer].

### <a name='glos_compression_failure'></a>compression failure 压缩失败
不是一个真正的错误，更恰当的说法是在混合使用压缩(***compression***)和***DML***操作时产生的一个“昂贵”的操作。会在以下情况下发生：修改一个压缩过的页(***page***)溢出了为记录修改所预留的页；所有的变更都应用到表数据中，页面被再次压缩；重新压缩过的数据不再能适应原始的页，需要MySQL分割数据到两个新的页并对其单独分别压缩。为了检查这种情况发生的频率，查询表`INFORMATION_SCHEMA.INNODB_CMP`并检查有多少`COMPRESS_OPS`列的值超过`COMPRESS_OPS_OK`列上的值。理想情况下，压缩失败并常经常出现；当它们出现时，你可以调整配置选项[innodb_compression_level]. [innodb_compression_failure_threshold_pct]和[innodb_compression_pad_pct_mac]。

参见 [compression], [DML], [page].

### <a name='glos_concatenated_index'></a>concatenated index: 复合索引
参考 [composite index].

### <a name='glos_concurrency'></a>concurrency: 并发
多个操作(在数据库的术语中，叫***transactions***)同时执行而不会互联影响的能力。并发也与性能是密切相关的，因为在理想情况下，使用了高效的锁机制(***locking***)来以最小的性能代价去保护多个同时工作的事务。

参见 [ACID], [locking], [transactions].

### <a name='glos_configuration_file'></a>configuration file: 配置文件
保存MySQL启动参数选项(***option***)的文件。传统上该文件在Linux和UNIX上名为`my.cnf`，在Windows上名为`my.ini`。你可以在该文件的[mysqld]节设置大量与InnoDB相关的选项。

一般来讲，这个文件可以在`/etc/my.cnf`. `/etc/mysql/my.cnf`. `/usr/local/mysql/etc/my.cnf`和`~/.my.cnf`下可以找到。有关该文件的搜索路径的细节请参考[第4.2.3.3节，使用配置文件](04.02.03.03)。

当你使用MySQL企业备份(***MySQL Enterprise Backup***)产品，你一般会用到两个配置文件：一个用来指定数据从哪儿来工它们是如何组织的(它可能是你真正服务的最原始的配置文件)，另一个是只包含一小部分选项的精简版，用来指定备份数据去哪儿和它们是如何组织的。要使用MySQL企业备份(***MySQL Enterprise Backup***)产品的话，配置文件中必须包含常规配置文件中一些没有加进去的选项，所以为使用MySQL企业备份(***MySQL Enterprise Backup***)产品起见，你可能要向已存在的配置文件中加入一些选项。

参见 [my.cnf](mycnf), [option file].

### <a name='glos_consistend_read'></a>consistend read: 一致性读
一个使用快照信息来呈现基于一个时间点的查询结果的读操作，而不管同一时间点上执行的事务所带来的变更。如果查询到的数据已经被其它事务改变，原始数据会基于***undo log***中的内容进行重建。这个技术避免了一些因为一个事务被强制等待另一个事务结束而降低并发(***concurrency***)的加锁(***locking***)问题。

在可重复读隔离(***repeatable read***)级别，快照基于第一次读操作执行的时间。在提交可读(***read committed***)隔离级别，快照在每一次一致性读操作时都重置。

一致性读的默认模式下，InnoDB会用提交可读(***READ COMMITTED***)和可重复读(***REPEATABLE
READ***)隔离级别处理`SELECT`语句。因为一个一致性读操作不会向它访问的表加任何锁，所以其它会话可以在一个一致性读操作正在这个表上执行的时候自由地修改这些表。

更多可用的隔离级别的技术细节，请参考[第14.2.2.4节，一致性无锁读](14.02.02.04)。

参考 [ACID], [concurrency], [isolation level], [locking], [MVCC], [READ COMMITTED], [READ UNCOMMITTED], [REPEATABLE READ], [SERIALIZABLE], [transaction], [undo log].

### <a name='glos_constraint'></a>constraint: 约束
一个可以阻止数据库更改以防止数据变得不一致的自动测试。(在计算机科学术语中，是一种与不变状态相关的断言)。约束是***ACID***理念中至关重要的组成部，用来维持数据的一致性。MySQL中支持约束的有外键约束(***FOREIGN KEY constraints***)与唯一约束(***UNIQUE constraints***)。

参考 [ACID], [foreign key], [relational], [unique constraint].

### <a name='glos_counter'></a>counter: 计数器
由一种特殊的`InnoDB`操作增加的一个值。有助于标志一个服务繁忙程度. 分析性能问题的源头和测试变更(例如，对配置选项或查询使用的索引的变更)是否有期望的低级别的效果。不同类型的计数器可以通过***performance_schema***表和***infomation_schema***表，特别是`infomation_schema.innodb_metrics`表来获得。

参见 [INFORMATION_SCHEMA], [metrics counter], [Performance Schema].

### <a name='glos_covering_index'></a>covering index: 覆盖索引
一个包含查询所检索的所有列的索引(***index***)。替代将索引值当成指针在全表行里查找，查询直接从索引结构中返回值，节省了磁盘I/O。InnoDB要比MyISAM能更多地应用这种优化技术，因为InnoDB的二级索引(***secondary index***)也包含了主键列。InnoDB不能在被一个事务修改过的表上应用这种技术，直到这个事务结束为止。

给定一下正确的查询，任何单列索引(***column index***)或组合索引(***composite index***)都可以做为一个覆盖索引。设计你的索引或查询让它们能够在任何可能的情况下利到这种优化技术的好处。

参见 [column index], [composite index], [index], [secondary index].

###  <a name='glos_crash'></a>crash: 崩溃
MySQL使用“崩溃”这个术语来一般指代服务的任何在没有做自己正常清理工作情况下的非预期的宕机(***shutdown***)操作。例如，一个崩溃可能由数据库服务器上机器或存储设备的硬件故障引发；一个潜在的数据不匹配导致MySQL服务的挂起；一个DBA触发的快速关机(***fast shutdown***)；或其它更多原因。***InnoDB***自动崩溃恢复(***crash recovery***)的鲁棒性确保在服务重起后数据是一致的，而不需要DBA做额外的工作。

参见 [crash recovery], [fast shutdown], [InnoDB], [redo log], [shutdown].

### <a name='glos_crash_recovery'></a>crash recovery 崩溃恢复
MySQL在崩溃后再次启动时做的清理行为。对于InnoDB表，未完成的事务带来的变更会利用redo log中的数据来重放。在崩溃之前提交的但尚未写到数据文件中的变更会从双写缓冲中重构。当数据库正常关机时，此类行为会在关闭时由清除操作来执行。

在正常的操作中，提交了的数据在写入到数据文件前的一段时间内被存储在变更缓冲中。这在与一直让数据文件保持最新之间存在取舍，让数据保持最新会在正常操作中带来性能开销，但缓冲数据会在关机或崩溃恢复时要花费更多时间。

参见 [change buffer], [commit], [crash], [data files], [doublewrite buffer], [InnoDB], [purge], [redo log].

### <a name='glos_crud'></a>CRUD: CRUD
“create, read, update, delete”首字母缩写，数据库应用中的常见操作序列。经常表示一类相对简单的可以快速用任何语言可以实现数据库用法(基本的***DDL***. ***DML***和***SQL***查询(***query***)语句)的应用。

参见 [DDL], [DML], [query], [SQL].

### <a name='glos_cursor'></a>cursor: 游标或光标
一个用来表示查询(***query***)结果集的内部数据结构，或其它使用SQL `WHERE`子句执行搜索的操作。它像其它高级语言中的迭代器一样工作，让结果集中的每个值都被请求到。

虽然SQL为你处理了游标进程，但你可以在处理性能关键的代码时可以深入了解内部工作机理。

参见 [query].

## <a name="D"></a>D ##

### <a name='glos_data_definition_language'></a>data definition language: DDL

参见 [DDL].

### <a name='glos_data_dictionary'></a>data dictionary: 数据字典
保存跟踪诸如表(***tables***). 索引(***indexes***)以及表列(***columns***)等InnoDB相关的对象的元数据。这些元数据的物理位置在InnoDB系统表空间(***system tablespace***)中。因为历史原因，它与存储在***.frm***文件中的信息在某些维度上是重合的。

因为MySQL企业备份(***MySQL Enterprise Backup***)产品一直备份系统表空间，所以所有的备份都多包含数据字典的内容。

参见 [column], [.frm file][frm file], [hot backup], [index], [MySQL Enterprise Backup], [system tablespace], [table].

### <a name='glos_data_directory'></a>data directory: 数据目录
一个目录，下面存储着每个MySQL实例(***instance***)保存InnoDB的数据文件(***data files***)以及对因数据库的目录。由datadir配置选项控制。

参见 [data files], [instance].

### <a name='glos_data_files'></a>data files 数据文件
在物理上包含InnoDB表(***table***)和索引(***index***)数据的文件。在一种类型的系统表空间(***system tablespace***)中，在数据文件和表之间可以是一对多的关系，它可以持有多个InnoDB表和数据目录(***data dictionary***)。当***file-per-table***选项激活时，数据文件和表之间也可以是一对一的关系，新创建的表将被存储到单独的表空间(***tablespace***)中。

参见 [data dictionary], [file-per-table], [index], [system tablespace], [table], [tablespace].

### <a name='glos_data_manipulation_language'></a>data manipulation language: DML

参见 [DML]。

### <a name='glos_data_warehouse'></a>data warehouse: DW或数据仓库
一个主要用来运行大查询(***queries***)的数据库系统或应用。为了提高查询效率，只读或几乎只读的数据以反范式(***denormalized***)的形式组织。在MySQL 5.6及更高版本中，可以获益于为只读事务做的优化。

与***OLTP***相对。

参见 [denormalized], [OLTP], [query], [read-only transaction].

### <a name='glos_database'></a>database: 数据库
在MySQL数据目录(***data directory***)中，每个数据库都用一个单独的目录来表示。InnoDB的系统表空间(***system tablespace***，它也可以保持MySQL实例(***instance***)中多个数据库的表数据)被保存在数据文件(***data files***)中，数据文件存在于单独的数据库目录之外。当file-per-table模式激活，代表InnoDB表的.ibd文件存储在数据库目录中。

对于长时间使用MySQL的用户来说，数据库是一个熟悉的概念。一个有Oracle数据库背景的用户会发现MySQL中数据库的意思与Oracle数据库中所谓的***schema***很相近。

参见 [data files], [file-per-table], [.ibd file][ibd file], [instance], [schema], [system tablespace].

### <a name='glos_dcl'></a>DCL: Data control language
数据控制语言，一组用来管理权限的***SQL***语句。在MySQL中，由***GRANT***和***REVOKE***语句组成。

与***DDL***与***DML***对应。

参见 [DDL], [DML], [SQL].

### <a name='glos_ddl'></a>DDL: Data definition language
数据定义语言，一组用来操作数据库本身而不是单独表行的***SQL***语句。包括所有的`CREATE`. `ALTER`和`DROP`语句。也包括`TRUNCATE`语句，因为它异于`DELETE FROM tabel_name`语句，尽管从最终效果上看，两者是非常相似。

DDL语句自动提交(***commit***)当前事务(***transaction***)；它们不能回滚(***rolled back***)。

InnoDB相关的DDL方面有`CREATE INDEX`和`DROP INDEX`的速度提高和***file-per-table***选项对`TRUNCATE TABLE`语句行为影响的方式。

与DML和DCL对应。

参见 [commit], [DCL], [DML], [file-per-table], [rollback], [SQL], [transaction].

### <a name='glos_deadlock'></a>deadlock: 死锁
不同的事务不能够继续的一种情况，因为它们都持有一个其它事务(***transactions***)所需要的锁(***lock***)。由于两个事务都需要等待资源可用，也永远不会释放他们所持有的锁。

当一个事务以相反的顺序锁定了多个表中的行(由诸如`UPDATE`或`SELECT .. FOR UPDATE`)时会发生死锁。一个死锁也有可能在诸如锁定索引的范围和间隙时发生，每个事务获取了一些锁但因为时间原因没有获取到其它锁。

为了减少死锁的几率，使用事务，而不是`LOCK TABLE`语句；保持事务中插入或更新的数据足够小这样它们就不会过久地停留在打开状态；当不同的事务更新多个表或大范围的行时，在每个事务中使用相同的操作顺序(如`SELECT ... FOR UPDATE`)；为`SELECT ... FOR UPDATE`和`UPDATE ... WHERE`语句创建索引。死锁几率与隔离级别(***isolation level***)无关，因为隔离级别改变读操作行为，而死锁因写操作而起。

如果一个死锁产生了，InnoDB检测到状态并让其中一个事务(***victim***)回滚(***rolls back**)。因此，就算是你的应用逻辑准确无比，你也应该处理一个事务需要重试的情况。要查看InnoDB用户事务中的最后一个死锁，使用`SHOW ENGINE INNODB STATUS`。如果频繁的死锁让一个事务结构体或应用错误处理的问题变得非常明显，激活`innodb_print_all_deadlocks`选项运行`mysqld`，它会将所有关于死锁的信息全打到`mysqld`错误日志中。

更多死锁如何自动检测与处理的背景资料，参考[第14.2.2.10节，死锁检测与回滚][14.02.02.10]。更多避免与恢复死锁状况的提示，参考[第14.2.2.11节，如何应对死锁][14.02.02.11]。

参考 [concurrency], [gap], [isolation level], [lock], [locking], [rollback], [transaction], [victim].

### <a name='glos_deadlock_detection'></a>deadlock detection: 死锁检测
一个自动检测死锁(***deadlock***)发生并自动回滚(***roll back***)其中一个事务(***the victim***)的机制。

参见 [deadlock], [rollback], [transaction], [victim].

### <a name='glos_delete'></a>delete: 删除
当InnoDB处理一个删除语句时，行记录被立即标记为删除并不再能被查询返回。存储稍后会在称为清除操作的周期性垃圾回收期间被收回，由单独的线程执行。要移除大量的数据，与它们自己性能特性相关的操作是***truncate***和***drop***

参考 [drop], [purge], [truncate].

### <a name='glos_delete_buffering'></a>delete buffering 删除缓冲技术。
将因删除操作而发生的索引变更在插入缓冲(***insert buffer***)中存储而不是立马写入它们的技术，这么做是为了将物理写操作的随机I/O降到最小。(因为删除操作有两步处理，这个操作将正常标记索引记录为删的写操作缓冲下来。)它是变更缓冲(***change buffering***)的一种类型；其它的为插入缓冲(***insert buffering***)和清除缓冲(***purge buffering***)。

参见 [change buffer], [change buffering], [insert buffer], [insert buffering], [purge buffering].

### <a name='glos_denormalized'></a>denormalized: 反范式
一种数据存储策略，它将多个不同表中的数据重复复制，而不是将这些表通过外键(***foreign keys***)和关联(***join***)查询链接起来。一般在数据仓库(***data warehouse***)应用中使用，它的数据在加载后不会再更新。在这样的应用中，查询的性能要比为更新时维持一致更重要而使其简单更重要。

与它对应的是范式(***normalized***)。

参见 [data warehouse], [normalized].

### <a name='glos_descending_index'></a>descending index: 降序索引
在某些数据库系统中有效的一种索引，索引的存储专门为处理`ORDER BY column DESC`子句而优化。虽然目前MySQL允许`DESC`关键字出现在`CREATE TABLE`语句中，但它并没有为结果索引使用用任何特殊的存储布局。

参见 [index].

### <a name='glos_dirty_page'></a>dirty page: 脏页
一个已经在内存中被更新过，但变更尚未写入(刷新,***flushed***)到数据文件(***data files***)中的InnoDB ***buffer pool***中页(***page***)。

与它对应的是净页(***clean page***)。

参见 [buffer pool], [clean page], [data files], [flush], [page].

### <a name='glos_dirty_read'></a>dirty read: 脏读
一个获取到不可靠数据的操作，数据被另一个事务更新但尚未提交。它只在未提交读的隔离级别中有可能出现。

这种操作并不遵守数据库设计的ACID原则。它的一致性是非常有风险的，因为数据可能会被回滚，或在提交前进一步被更新；那个时候，做了脏读的事务可能会使用从未被准确确认过的数据。

它的对立面是一致性读，InnoDB全力确保一个事务不会读到另一个事务修改过的信息，即使其它事务在期间已经做了提交。

参见 [ACID], [commit], [consistent read], [isolation level], [READ COMMITTED], [READ UNCOMMITTED], [rollback].

###  <a name='glos_disc_based'></a>disk-based 基于磁盘
See Also adaptive hash index, buffer pool, in-memory database.
主要在磁盘(硬盘或等同于硬盘)上组织数据的一种数据库。数据在磁盘与内存之间来回传输修改。与它对应的是内存数据库。尽管InnoDB是基于磁盘的，但经也包含一些诸如buffer pool. 多buffer pool实例和自适应索引等让一些工作主要在内存中完成。

参见 [adaptive hash index], [buffer pool], [in-memory database].

### <a name='glos_cpu_bound'></a>cpu-bound: CPU受限
一种瓶颈(***bottleneck***)主要是内存中CPU操作的负载类型。通常来说会包括读密集型的操作，其中的结果可以全部缓存中***buffer pool***中。

参见 [boteneck], [buffer pool], [disk-bound], [workload].

### <a me='glos_disk_bound'></a>disk-bound: 磁盘受限
一种瓶颈(***bottleneck***)主要是磁盘I/O的负载类型。(也叫I/O带宽,***I/O-bound***。)一般包括频繁写盘或随机读取更多不适合放在***buffer pool***中的数据。

参见 [bottleneck], [buffer pool], [cpu-bound], [workload].

### <a name='glos_dml'></a>DML: 不译
数据操作语言，一组用来执行insert. update和delete操作的SQL语句。SELECT语句有时候也被当成是DML句句，因为SELECT ... FOR UPDAET模式受到与INSERT. UPDATE和DELETE一样的锁的考虑。

DML语句对InnoDB表的操作是以事务方式进行的，所以它的效果可以当成一个单元被提交或回滚。

对比使用***DDL***和***DCL***。

参见 [commit], [DCL], [DDL], [locking], [rollback], [SQL], [transaction]。

### <a name='glos_document_id'></a>document id: 全文索引编号
在InnoDB全文搜索(***full-text search***)特性中，一个在表中包含全文索引(***FULLTEXT  index***)的特殊的列，用来唯一标识与每个搜索词链表(***ilist***)相关联的文档。它的名字为`FTS_DOC_ID`(必须大写)。此列本身类型必须为`BIGINT UNSIGNED NOT NULL`，并有一个名为`FTS_DOC_ID_INDEX`的唯一索引。你最好在创建表的时候就定义此列。如果InnoDB必须加入此列，同时创建一个全文(***FULLTEXT***)索引，索引操作是相当昂贵的。

参见 [full-text search], [FULLTEXT index], [ilist].

### <a name='glos_doublewrite_buffer'></a>doublewrite buffer: 双写缓冲
InnoDB使用一种新的文件刷新技术叫双写。在页(***pages***)写入到数据文件(***data files***)之前，InnoDB先把它们写到相邻的一个叫做双写缓冲的区域中。只有当写入并刷新到双写缓冲的操作已经完成的情况下，InnoDB才会将这些页写到数据文件中它们真正的位置上。如果操作系统在页写的中途崩溃了，InnoDB可以在稍后的崩溃恢复(***crash recovery***)中从双写缓冲找到一个健全的页的拷贝来。

尽管数据始终要写两次，但双写缓冲并不需要两部的I/O开销或I/O操作。数据自身被当成一个大的连续的块写入到缓冲中，并用一个单独的`fsync()`调用操作系统。

要关掉双写缓冲，设置选项`innodb_doublrwrite=0`。

参见 [crash recovery], [data files], [page], [purge].

### <a name='glos_drop'></a>drop: 删除
一种通过诸如`DROP TABLE`或`DROP INDEX`等语句来删除数据库对象的***DDL***操作。内部映射为`ALTER TABLE`语句。从InnoDB角度看，这些操作的性能考虑主要包括为确保相关的对象全部被更新而锁定数据字典(***data dictionary***)的时间，以及更新如***buffer pool***等内存结构的时间。对于一个表(***table***)来说，drop操作跟***truncate***操作(TRANCATE TABLE语句)在特性上有一点儿不一样。

参见 [buffer pool], [data dictionary], [DDL], [table], [truncate].

### <a name='glos_dynamic_row_format'></a>dynamic row format: 变长行格式
InnoDB Plugin中引入的一种行格式，是Barracuda文件格式(***Barracuda file format***)中的一部分。因为`TEXT`和`BLOB`字段在保持其它字段的页之外存储，所以它对包含大对量的行来说非常高效。因为大字段通常不会被访问用来做查询条件，所以他们经常不会被带入到`buffer pool`中，从而减少I/O操作，并更合理地利用了缓存。

参见 [Barracuda], [buffer pool], [file format], [row format].

## <a name="E"></a>E ##

### <a name='glos_early_adopter'></a>early adopter: 测试版
类似测试(***beta***)，是一个产品在非关键任务环境中通过了性能. 功能和兼容性评估的阶段。InnoDB用***early adopter***来代替beta，通过一系列的更新版本，达到***GA***发布版本。

参见 [beta], [GA].

### <a name='glos_error_log'></a>error log: 错误日志
一种展示MySQL启动. 关键运行时错误及崩溃(***crash***)信息的日志(***log***)，细节请参考[5.2.2节，错误日志](05.02.02)。

参见 [crash], [log].

### <a name='glos_evition'></a>eviction: 替换出去
一个将项目从缓存或其它临时存储区删除的过程，比如从InnoDB ***buffer pool***中。通常但不总时用***LRU***算法来判断将哪个项目删除。当一个脏页(***dirty page***)被替换出去，它的内容会被刷新(***flushed***)到磁盘，并且任何脏(***dirty***)的相邻(***neighbor***)页也可能会被刷新。

参见 [buffer pool], [dirty page], [flush], [LRU].

### <a name='glos_exclusion_lock'></a>exclusive lock: 排它锁
一种阻止任何其它的事务(***transaction***)锁定相同行的锁(***lock***)。取决于事务隔离级别(***isolation level***)，这种类型的锁可能阻止其它事务写相同的行，也有可能阻止其它事务读取相册的行。InnoDB默认的隔离级别，可重复读(***REPEATABLE READ***)，通过允许事务读取加有排它锁的行获得更高的并发(***concurrency***)，这种技术叫做一致性读(***consistent read***)。

参见 [concurrency], [consistent read], [isolation level], [lock], [REPEATABLE READ], [shared lock], [transaction].

### <a name='glos_extent'></a>extent: 簇
表空间(***tablespace***)中总共1MB的一组页(***pages***)。默认的页大小(***page size***)为16KB，一个区包含64个页。在MySQL5.6中，页大小可以是4KB或8KB，这种情况下一个簇可以包含更多的页，但总大小仍为1M。

诸如段(***segments***). 预读(***read-ahead***)请求和双写缓冲(***doublewrite buffer***)等这样InnoDB的特性在使用读. 写. 申请或释放数据时，都是一次一个簇来操作。

参见 [doublewrite buffer], [neighbor page], [page], [page size], [read-ahead], [segment], [tablespace].

## <a name="F"></a>F ##

### <a name='glos_fast_index_creation'></a>Fast Index Creation: 快速索引创建
一种通过避免完全重写对应的表而加速InnoDB二级索引(***secondary indexes***)创建速度的功能，在InnoDB Plugin中引入，一在是MySQL 5.5及更高版本的组成之一。加速同样适用于删除二级索引。

因为索引的维护会增加性能上的开销来完成大量的数据传输操作，所以可以考虑在做诸如`ALTER TABLE ... ENGINE=INNODB`或`INSERT INTO ... SELECT FROM ...`的操作时不做二级索引，而在完成后再创建索引。

在MySQL 5.6中，这个特性变得更加通用：你可以在索引正在被创建时读写这个表，并且更多类型ALTER TABLE操作可以在不拷贝表. 不阻止***DML***操作或两者兼有的情况下执行。因此我们可以将这组特性叫做在线DDL而不是快速索引创建。

参见 [DML], [index], [online DDL], [secondary index].

### <a name='glos_fast_shutdown'></a>fast shutdown: 快速关闭
InnoDB默认的关闭(***shutdown***)程序，基于配置设置`innodb_fast_shutdown=1`。为了节省时间，某些刷新(***flush***)操作被跳过。这类关闭在正常使用中是安全的，因为刷新操作会在下次启动时执行，使用了与崩溃恢复(***crash recovery***)相同的机制。在因为升级或降级而关闭数据库的情况下，做缓慢关机(***slow shutdown***)替代以确保关机过程中所有相关的变更都应用到数据文件(***data files***)中。

参见 [crash recovery], [data files], [flush], [shutdown], [slow shutdown].

### <a name='glos_file_format'></a>file format: 文件格式
InnoDB为每个表所使用的格式，通常激活***file-per-table***设置来确保每张表都存储在单独的`.ibd`文件(***.ibd file***)中。目前，InnoDB中可用的格式是***Antelope***和***Barracuda***。每种文件格式都支持一种或多种行格式(***row format***)。Barracuda表中可用的行格式，压缩(***COMPRESSED***)与动态(***DYNAMIC***)，为InnoDB开启了重要的新的存储特性。

参见 [Antelope], [Barracuda], [file-per-table], [.ibd file][ibd file], [ibdata file], [row format].

### <a name='glos_file_per_table'></a>file-per-table: 独立表空间
受`innodb_file_per_table`选项控制的设置的普通名。这是一个影响InnoDB文件存储. 功能可用性及I/O好多方面的重要配置。在MySQL 5.6.7及更高版本中它默认开启。在MySQL 5.6.7之前的版本中它默认关闭。

对于每一个在此选项生效时创建的表来说，数据是存储在一个单独的.ibd文件(***.ibd file***)中，而不是系统表空间(***system tablespace***)的ibdata文件(***ibdata file***)中。当表数据存储在独立的文件中时，你有更多选择非默认文件格式(***file format***)与行格式(***row format***)的灵活性，这些格式要求一些必须的特性，如数据压缩。`TRUNCATE TABLE`操作也会更快，并且回收了的空间可以为操作系统所用，而不是留给InnoDB。

MySQL企业备份产品(***MySQL Enterprise Backup***)对它们自己文件中的表来说更具灵活性。比如，表在单独的文件中时，它可以从备份中排除掉。所以，这个选项适合那些备份频率降低或在不同的备份日程中的表。

参见 [compressed row format], [compression], [file format], [.ibd file][ibd file], [ibdata file], [innodb_file_per_table], [row format], [system tablespace].

### <a name='glos_fill_factor'></a>fill factor: 填充因子
在InnoDB索引(***index***)中，在页(***page***)分裂前页中被索引数据占据的部分。在索引数据最初在页间划分时没有用到的空间允许那些用更长的字符串更新的行不再需要代价过高的索引维护操作。如果填充因子过小，索引需要消耗比所需更多的空间，导致在读索引时带来额外的I/O开销。如果填充因子过高，任何增加列值长度的更新都会导致因索引维护带来的额外的I/O负载。更多信息参考[第14.2.2.13.4节，InnoDB索引的物理结构]。

参见 [index], [page].

### <a name='glos_fixed_row_format'></a>fixed row format: 定长行格式
MyISAM引擎使用的行格式，InnoDB不用。如果你使用`row_format=fixed`选项创建一张InnoDB表，InnoDB会把这个选项转化成精简行格式(***compact row format***)来替代，不过`fixed`变量可能仍然出现在诸如`SHOW TABLE STATUS`报表中。

参见 [compact row format], [row format].

### <a name='glos_flush'></a>flush: 刷新
将变更写到数据库文件中，这些变量是已经缓冲在一个内存区或一个临时磁盘存储区。被定期刷新的InnoDB的存储结构体包括***redo log***. ***undo log***和***buffer pool***。

刷新会因为内存变满了和系统需要释放一些空间而发生，因为一个提交(***commit***)操作意味着来自事务的变更可以确定了，或因为一个缓慢关机(***slow shutdown***)操作意味着所有的未完成的工作应该确定了。在并不需要一次性将所有缓冲了的数据刷新时，`InnoDB`使用一种叫模糊检查点(***fuzzy checkpointing***)的技术刷新小批量的页来平滑I/O负载。

参见 [buffer pool], [commit], [fuzzy checkpointing], [neighbor page], [redo log], [slow shutdown], [undo log].

### <a name='glos_flush_list'></a>flush list: 刷新列表
一个InnoDB内部的用来跟踪***buffer pool***中脏页(***dirty page***)数据结构体：就是已经被变更的并且需要被写回到磁盘的页(***pages***)。这个数据结构体被InnoDB内部的迷你事务(***mini-transactions***)频繁更新，所以被自身的互斥锁(***mutex***)保护来允许对buffer pool的并发访问。

参见 [buffer pool], [dirty page], [LRU], [mini-transaction], [mutex], [page], [page cleaner].

### <a name='glos_foreign_key'></a>foreign key: 外键
不同InnoDB表的行之间的一种指针关系的类型。外键关系是在父表(***parent table***)和子表(***child table***)的一个列上建立的。

除了能快速查找相关相信外，外键可以防止指针因插入. 更新和删除变得无效，有助于强制引用一致性(***referential integrity***)。这种强制是一种约束(***constraint***)。如果相关联的外键值在其它表里不存在的话，指向它的行将不能插入。如果一行被删除了或它的外键值被修改了，并且其它表中的有行指向这个外键值，外键可以被设置为阻止删除. 让其它表中相符的的列值变为空或自动删除其它表中相符的行。

设计一个范式化(***normalized***)数据库的阶段之一是找出重复的数据，将这些数据分离到一个新表中，设置一个外键关系，使用关系操作，这样就可以像查询一张表一样来查询多张表了。

参见 [child table], [FOREIGN KEY constraint], [join], [normalized], [NULL], [parent table], [referential integrity], relational.

### <a name='glos_foreign_key_constraint'></a>FOREIGN KEY constraint: 外键约束
通过一个外键关系(***foreign key***)来维护数据库一致性的约束类型。像其它约束一样，如果数据可能会变得不一致时，它可以阻止数据的插入与更新；在这种情况下，被阻止的不一致性是在多个表的数据之间的。或者说，当一个***DML***操作被执行了，基于在创建外键时指定的`ON CASECADE`选项，外键约束可以导致字表中的行(***child rows***)被删掉. 变更为不同的值或设置为空。

参见 [child table], [constraint], [DML], [foreign key], [NULL].

### <a name='glos_frm_file'></a>.frm file: .frm file 
一个包含MySQL表的诸如表定义等元数据的文件。

对于备份来说，你得必须一直随着备份数据保存所有`.frm`文件的集合，这样可以恢复那些在备份后被修改或删掉的表。

尽管每张InnoDB表都有一个`.frm`文件，但InnoDB在系统表空间中维护了自己表的元数据；对于InnoDB来说操作InnoDB表不再需要`.frm`文件了。

这些文件会被MySQL企业备份产品(***MySQL Enterprise Backup***)备份。这些文件在正在备份时必须不被`ALTER TABLE`操作修改，这就是为什么包含非InnoDB表的备份要在备份.frm文件时执行一个`FLUSH TABLES WITH READ LOCK`操作来冻结这种活动的原因。

参见 [MySQL Enterprise Backup].

### <a name='glos_fts'></a>FTS: 全文搜索
在大多数据情况下，是全文搜索(***full-text search***)的首字母缩写。有时在讨论性能问题时，也是全表扫描(***full table scan***)的缩写。

参见 [full table scan], [full-text search].

### <a name='glos_full_backup'></a>full backup: 全备
包含一个MySQL实例(***instance***)中所有数据库，每个数据库(***database***)中所有表(***tables***)的备份(***backup**)。相对的是部分备份(***partial backup***)。

参见 [backup], [database], [instance], [partial backup], [table].

### <a name='glos_full_table_scan'></a>full table scan: 全表扫描
一个没有使用索引选择部分数据，而是需要读取整表内容的操作。通常是在小的查询表中执行，或在数据仓库环境下的大表中执行，其中所有有效的数据都要被聚合和分析。这些操作出现的频繁程度，以及这些表大小所对对应的可用内存，对于查询优化与管理buffer pool都有影响。

索引(***indexes***)的目录就是为了允许在大表中查找特定的值或一定范围的值，这样就避免了全表扫描。

参见 [buffer pool], [index], [LRU].

### <a name='glos_full_text_search'></a>full-text search: 全文搜索
在表数据中查找单词. 词组及单词布尔组合等的MySQL特性，比你使用SQL `LIKE`操作符或在自己应用层写搜索算法的方式要更快. 更方便和更灵活的方式。它使用SQL的`MATCH()`函数和全文索引(***FULLTEXT indexes***)。

参见 [FULLTEXT index].

### <a name='glos_fulltext_index'></a>FULLTEXT index: 全文索引
保存MySQL全文索引机制中搜索索引的特殊的索引类型。包含了列中删除停用词之后的单词。最早只在MyISAM表中可用，自MySQL 5.6.4起，InnoDB表中也可以使用了。

参见 [full-text search], [index], [InnoDB], [search index], [stopword].

### fuzzy checkpointing 模糊检查点刷新
一种从***buffer pool***中使用小批量刷新(***flush***)脏页(***dirty page***)，而不是使用可能会打断数据库进程的一次性刷新所有脏页的技术。

参见 [buffer pool], [dirty page], [flush].

## <a name="G"></a>G ##
### <a name="glos_ga"></a>GA: 一般可用(建议直接用 GA)
“一般可用(Generally available)”，是软件产品离开测试版并且可供销售. 官方支持及生产可用的阶段。

参见 [beta], [early adopter].

### <a name="glos_gap"></a>gap: 间隙
InnoDB索引(***index***)数据结构中新值插入的地方。当你使用诸如`SELECT ... FOR UPDATE`这样的语句锁定一个行集时，InnoDB会创建应用到间隙和真实值的锁。比如，如果你选定了大于10的所有值来更新，间隙锁会阻止其它事务插入大于10的新值。上确界记录(***supremum record***)与下确界记录(***infimum record***)代表了包含所有大于或小于所有当前索引值的间隙。

参见 [concurrency], [gap lock], [index], [infimum record], [isolation level], [supremum record].

### <a name="gap_lock"></a>gap lock: 间隙锁
索引记录之间间隙(***gap***)上的锁，或第一个索引前或最后一个索引后的间隙上的锁。比如，`SELECT c1 FOR UPDATE FROM t WHERE c1 BETWEEN 10 and 20`；阻止其它事务向t.c1列中插入15，不管列中是否有这样的值，因为在范围中存在的值之间的间隙被锁住了。对比记录锁(***record lock***)与行间隙锁(***next-key lock***)。

间隙锁是性能与并发(***concurrency***)之间的取舍的一部分，在有些事务隔离级别(***isolation levels***)上是有用的，有些则不然。

参见 [gap], [infimum record], [lock], [next-key lock], [record lock], [supremum record].

### <a name="glos_general_log"></a>general log: 数据库日志

参见 [general query log].

### <a name="glos_general_query_log"></a>general query log: 数据库日志
一种用来为MySQL服务处理过的SQL语句的诊断问题与排除故障的日志(***log***)。可以被存储在文件中或数据库表中。你必须通过`general_log`配置选项使其生效来使用它。你可以用`sql_log_off`配置选项为一个指定的连接禁用它。

记录比慢查询(***slow log***)日志更广泛的查询。不像用来做镜像的二进制日志(***binary log***)，数据库日志包括`SELECT`语句并且不会维护严格的顺序。如需更多信息，参见[第5.2.3节，数据库日志][05.02.03]。

参见 [binary log], [general query log], [log].

### <a name="glos_global_transaction"></a>global_transaction: 全局事务
分布式事务(***XA***)中的一种事务(***transactions***)。它由几个本身就是事务的动作组成，但这些事务又必须以一组的方式一起成功完成，或以一组的方式整体回滚。本质上来讲，这让***ACID***的属性拓展升级，为的是让多个ACID事务可以在做为一个全局的同时拥有ACID属性的事务来合作执行。对于这种分布式事务类型，你可以使用***SERIALIZABLE***隔离级别来获得ACID属性。

See Also ACID, SERIALIZABLE, transaction, XA.

### <a name="glos_group_commit"></a>group commit: 组提交
一个***InnoDB***的优化，以一次一组提交的方式执行一些低级I/O操作(***log write***, 写日志)，而不是单独为每次提交都做刷新与同步。

当二进制日志打开时，你一般也要设置`sync_binlog=0`，因为对二进制日志的组提交只有当它设置为0时才起作用。

参见 [commit], [plugin], [XA].

## <a name="H"></a>H ##
### <a name="glos_hash_index"></a>hash index: 哈希索引
一个用来做等于操作的索引类型，而不是用来做诸如大于或`BETWEEN`等范围操作的。它在MEMORY表中有效。尽管哈希索引因为历史原因成为了MEMORY表的默认索引，这种存储引擎也支持B树(***B-tree***)索引，B树索引在通用查询中常常是个不错的选择。

MySQL中有一种这类索引的变体，自适应哈希索引(***apaptive has index***)，它是在运行时按需为***InnoDB***表自动生成的。

参见 [adaptive hash index], [B-tree], [index], [InnoDB].

### <a name="glos_hdd"></a>HDD: 机械磁盘或不译
hard disk drive的首字母缩写。指的是使用旋转盘片的存储媒介，一般用来与固态硬盘(***SSD***)做比较与对照。它的性能特性会影响到基于磁盘(***disk-based***)工作的吞吐量。

参见 [disk-based], [SSD].

### <a name="glos_heartbeat"></a>heartbeat: 心跳
一个为表示系统功能正常的而发出的周期性的信息。在镜像(***replication***)环境中，如果主库(***master***)停止发送此类信息，其中一个从库(***slave***)会替代它的位置。类似的技术可以被用到集群环境中的两台服务器之间，用来确保它们都正常运转。

参见 [replication].

### <a name="glos_high_water_mark"></a>high-water mark: 上限
一个表示上限的值，要么是运行时不许超越的硬性限制，要么实际中到达的最大记录值。与之对应的是下限(low-water mark)。

参见 [low-water mark].

### <a name="glos_history_list"></a>history list: 清除链表
含有被标为删除的记录的事务(***transaction***)列表，这些记录会被`InnoDB`清除(***purge***)操作有计划地处理。记录在***undo log***。清除链表的长度可以在`SHOW ENGINE INNODB STATUS`命令的报表中看到。如果清除链表增长到超过[innodb_max_purge_lag]配置选项的值，每个***DML***操作会被静默延迟，以让清除操作完成刷新(***flush***)删除的记录。

也叫 ***purge lag***.

参见 [flush], [purge], [purge lag], [rollback segment], [transaction], [undo log].

### <a name="glos_hot"></a>hot: 热
一行. 一张表或内部数据结构被访问得非常频繁的一种情况，需要某些模式下的锁和互斥，它会带来性能与扩展性上的问题。

虽然“热”一般指的是不受欢迎的情况，但热备(***hot backup***)却是备份中的较好的选择。

参见 [hot backup].

### <a name="glos_hot_backup"></a>hot backup: 热备
种在数据库在运行且应用在读写它的情况下的备份。这种备份涉及的不是简单的拷贝文件：它必须包括任何在备份进行时插入或更新的数据；它必须排除掉任何在血仇进行时被删除的数据；它必须忽略任何没有提交的变更。

Orcale的执行热备的产品，尤其是对InnoDB表，还有对MyISAM或其它存储引擎表，叫MySQL企业备份(***MySQL Enterprise Backup***)。

热备过程由两个阶段组成。最初的拷贝数据生成一个原始备份(***raw backup***)。应用(***apply***)步骤合将任何在备份运行过程中发生的变更都合并到数据中。应用变更会生与一个一致备份(***prepared backup***)；这些文件已经为随时恢复做好准备。

参见 [apply], [MySQL Enterprise Backup], [prepared backup], [raw backup].


## <a name="I"></a>I ##
### <a name="glos_io_bod"></a>I/O-bound: I/O带宽
参见[disk-bound]

### <a name="glos_ib_file_set"></a>ib-file set: ib文件集
MySQL数据库内部由InnoDB管理的一组文件：系统表空间(***system tablespace***). 任何***file-per-table***表空间以及***redo log***文件(一般有两个)。为了避免不同DBMS产品之间对数据库(***database***)含义以及MySQL数据库中非InnoDB文件的部分产生歧义，有时用在InnoDB文件结构与格式的细节讨论上。

参见 [database], [file-per-table], [redo log], [system tablespace].

### <a name="glos_ib_logfile"></a>ib_logfile: redolog文件或不译
构成***redo log***的一组文件，一般以`ib_logfile0`和`ib_logfile1`来命名。有时也被称为日志组(***log group***)。这些文件记录了尝试更改InnoDB表中数据的语句。在崩溃后的重启中，这些语句会自动重放到被未完成的事务写过的正确的数据中。

这些数据不能被用来做手动恢复；对于这种情况，使用二进制日志(***binary log***)。

参见 [binary log], [log group], [redo log].

### <a name="glos_ibbackup_logfile"></a>ibbackup_logfile: 不译
在热备(***hot bakcup***)操作中由MySQL企业备份(***MySQL Enterprise Backup***)产品创建的补充备份文件。它包含任何在备份运行时发生的变更的信息。这些包含`ibbackup_logfile`的初始备份文件叫做原始备份(***raw backup***)，因为在备份操作时间产生的变改尚未收入。当你向原始备份文件执行了应用(***apply***)步骤后，生成文件的确包含了那些最终的变量，这叫一执备份(***prepared backup***)。在这个阶段，`ibbackup_logfile`就没有用了。

参见 [apply], [hot backup], [MySQL Enterprise Backup], [prepared backup], [raw backup].

### <a name="glos_ibd_file"></a>.ibd file: .ibd文件
每个使用***file-per-table***模式创建的InnoDB表(***table***)会进入到数据库目录下自己的表空间(***tablespace***)文中，以`.ibd`为后缀名。这个文件包含表的数据和表的任何索引。file-pre-table模式由***innodb_file_per_table***选项来控制，影响InnoDB存储的使用量与性能，在MySQL 5.6.7及更高版本中默认开启。

这个后缀不适用于由ibdata文件(***ibdata files***)组成的系统表空间(***system tablespace***)。

当一个`.ibd`文件包含在MySQL企业备份(***MySQL Enterprise Backup***)产生的压缩备份中时，对应的压缩文是一个`.ibz`文件。

在MySQL 5.6或更高版本中，如果一个表使用DATA DIRECTORY ＝ 字句创建表时，.ibd文件会定位到正常数据库目录之外，并用一个.isl文件来指向它。

参见 [database], [file-per-table], [ibdata file], [.ibz file][ibz file], [index], [innodb_file_per_table], [.isl file][isl file], [MySQL Enterprise Backup], [system tablespace], [table], [tablespace].

### <a name="glos_ibdate_file"></a>ibdata file: ibdata文件
像`ibdata1`. `ibdata2`等等这样命名的一组文件，它们组成InnoDB的系统表空间(***system tablespace***)。这些文件包含InnoDB表的元数据(***data dictionary***，数据字典)和为***undo log***. 变更缓冲(***change buffer***)和双写缓冲(***doublewrite buffer***)等提供的存储区。它们也能包含一些或全部表的数据(取决于***file-per-table***模式是否开启)。当***innodb_file_per_table***选项生效，新为新表创建的数据和索引存储在单独的***.ibd***文件中，而不在系统表空间中。

`ibdata`文件的增长受`innodb_autoextend_increment`配置选项的影响。

参见 [change buffer], [data dictionary], [doublewrite buffer], [file-per-table], [.ibd file][ibd file], [innodb_file_per_table], [system tablespace], [undo log].

### <a name="glos_ibtmp_file"></a>ibtmp file: ibtmp文件
为非压缩InnoDB临时长或相关对象提供的InnoDB临时表空间数据文件。配置文件选项`innodb_temp_data_file_path`允许用户为临时数据文件定义对应的目录。如果`innodb_temp_data_file_path`没有定义，默认行为是在数据目录下的`ibdata1`文件边上创建一个名为`ibtmp1`的单独的数据文件，以12MB的大小自动递增。

参见 [temporary tablespace].

### <a name="glos_ibz_file"></a>.ibz file: .ibz文件
当MySQL企业备份产品(***MySQL Enterprise Backup***)执行一下压缩备份(***compressed backup***)时，它将每个由***file-per-table***选项产生的后缀为`.ibd`的表空间转换为后缀为`.ibz`的文件。

在备份过程中应用的压缩与在正常操作中保持数据压缩的压缩行格式(***compressed row format***)是不一样的。一个压缩备份操作会忽略掉那些已经是压缩行格式表空间的压缩步骤，二次压缩会延缓备份却很少带来空间上的节省。

参见 [compressed backup], [compressed row format], [file-per-table], [.ibd file][ibd file], [MySQL Enterprise Backup], tablespace.

### <a name="glos_ilist"></a>ilist: 索引词链表
InnoDB全文索引(***FULLTEXT index***)中，由文件编号和位置信息的标号(***token***)(也就是一个特定的词)组成的数据结构。

参见 [FULLTEXT index].

### <a name="glos_implicit_row_lock"></a>implicit row lock: 隐式行锁
一个为了确保数据一致性的InnoDB的行级锁，你不需要特别地请求它。

参见 [row lock].

### <a name="glos_in_memory_database"></a>in-memory database: 内存数据库
一种为了避免磁盘I/O负载和磁盘块与内存区之间传输负载而在内存中维护数据的一种数据库系统。一些内存数据库牺牲了持久性(ACID设计理念中的“D”)，易受硬件. 电源和其它类型的故障的影响，使得它们更适合于只读操作。

MySQL features that are address the same kinds of memory-intensive processing include the InnoDB buffer pool, adaptive hash index, and read-only transaction optimization, the MEMORY storage engine, the MyISAM key cache, and the MySQL query cache.

MySQL处理内存密集型进程的特性包括InnoDB ***buffer pool***. 自适应哈希索引(***adaptive hash index***). 只读事务(***read-only transaction***)优化. MEMORY存储引擎. MyISAM key cache以及MySQL查询缓存(***query cache***)。

参见 [ACID], [adaptive hash index], [buffer pool], [disk-based], [read-only transaction].

### <a name="glos_incremental_backup"></a>incremental backup: 增量备份
一种热备(***hot backup***)，由MySQL企业备份(***MySQL Enterprise Backup***)执行，它只保存某个时间点后改变了的数据。一个全量备份和一连串的增量备份可以让你在一个很长的时间段里重构你的备份数据，而没少手头上要保留多个全备份的存储压力。你可以先恢复全备份，然后连续应用每个增量备份，也可以应用每个增量备份让全备份保持更新状态，然后再执行一个单独的恢复操作。

The granularity of changed data is at the page level. A page might actually cover more than one row. Each changed page is included in the backup.

变更了的数据的粒度在页(***page***)层级。一个页可能实际上覆盖不至一行。每个变更了的行都包含在备份中。

参见 [hot backup], [MySQL Enterprise Backup], [page].

### <a name="glos_index"></a>index: 索引
一种数据结构，提供快速查找表(***table***)中行(***row***)的功能，通常是生成一棵树结构(***B-Tree***)，代表了一个特定列或一组列中的值。

InnoDB表一直拥有一个相当于主键(***primary key***)的簇索引(***clustered index***)。它们可以拥有定义在一列或多列上的一个或多个二级索引(***secondary key***)。依据二级索引的结构，它们可以划分为部分索引(***partial index***). 单列索引(***column index***)和组合索引(***composite index***)。

The ideal database design uses a covering index where practical;. 

索引是查询(***query***)性能的一个关键因素。数据库架构师设计表. 查询和索引以允许快速查找应用程序所需要的数据。理想的数据库设计使用实用的覆盖索引(***covering index***)；查询结果可以完全从索引中计算出来，而不用读实际的表数据。为了高效地检查值是否在父表(***parent table***)和子表(***child table***)中存在，每个外键约束(***foreign key***)也需要索引。

尽管B树索引最常用，但另一种数据结构被用来做哈希索引(***hash index***)，在`MEMORY`存储引擎和InnoDB自适应索引(***adaptive hash index***)中。

参见 [adaptive hash index], [B-tree], [child table], [clustered index], [column index], [composite index], [covering index], [foreign key], [hash index], [parent table], [partial index], [primary key], [query], [row], [secondary index], [table].

### <a name="glos_index_cache"></a>index cache: 索引缓存
为InnoDB全文搜索(***full-text search***)保存令牌数据的内存区。它在当是全文索引(***FULLTEXT index***)列中的数据被删除或更新时将该数据缓冲起来以减小磁盘I/O。在索引缓存变满时令牌数据会被写到磁盘上。每个InnoDB的全文索引都有各自独立的索引缓存，它的大小由配置选项`innodb_ft_cache_size`控制。

参见 [full-text search], [FULLTEXT index].

### <a name="glos_index_hint"></a>index hint: 索引提示
一个为了覆盖优化器推荐索引(***index***)使用的扩展SQL语法。例如，`FORCE INDEX`. `USE INDEX`和`IGNORE INDEX`字句。通常是在索引列上的值分布不均匀，导致基数(***cardinality***)评估不准确的情况下使用。

参见 [cardinality], [index].

### <a name="glos_index_prefix"></a>index prefix: 索引前缀
在一个多列索引(***composite index***，组合索引)中，索引(***index***)的初始列或前导列。一个引用组合索引中最前面的1. 2. 3等等列的查询可以使用到索引，即使这个查询没有引用到索引中的所有列。

参见 [composite index], [index].

### <a name="glos_index_statistics"></a>index statistics: 索引统计
参见 [statistics].

### <a name="glos_infimum_record"></a>infimum record: 下确界记录
索引(***index***)中假想的记录(***psesudo-index***)，代表这个索引中低于最小值的间隙(***gap***)。如果一个事务有一个诸如`SELECT ... FOR UPDATE ... WHERE col < 10;`的语句；并且这个列中最小值为5，它将锁住这个下确界记录以阻止其它事务插入更小的值，比如0啊. －10啊等等。

参见 [gap], [index], [pseudo-record], [supremum record].

### <a name="glos_information_schema"></a>INFORMATION_SCHEMA: 系统信息库
为MySQL数据字典(***data dictionary***)提供查询接口的数据库的名字。(此名由ANSI SQL标准定义。)为了检查数据库的信息(元数据)，你可以查询诸如`INFOMATION_SCHEMA.TABLES`和`INFOMATION_SCHEMA.COLUMNS`的表，而不使用产生没有结构化输出的`SHOW`命令。

信息系统库包含一些***InnoDB***特定的表，如`INNODB_LOCKS`和`INNODB_TRX`。你使用这些表不是用来看这个数据库是如何组织的，而是获取关系InnoDB表的实时信息来帮助做性能监控. 调优和故障排除的。实际上，这些表提供了关于MySQL压缩(***compression***). 事务(***transaction***)以及它们对应锁(***lock***)的特性的数据。

参见 [compression], [data dictionary], [database], [InnoDB], [lock], [transaction].

### <a name="glos_innodb"></a>InnoDB: InnoDB
一个MySQL组件，它高性能与事务(***transaction***)功能结合起来，提供可靠性. 鲁棒性与并发访问。它体现了***ACID***的设计理念。表示一个存储引擎(***storage engine***)；它可以用`ENGINE=INNODB`子句来处理表的创建与更改。架构细节和管理程序参见[第14.2节，InnoDB存储引擎][14.02.00]，性能建议参见[第8.5节，优化InnoDB表][08.05.00]。

在MySQL 5.5或更高版本中，InnoDB是新创建表的默认存储引擎，`ENGINE=INNODB`子句不是必需的了。仅在MySQL 5.1中，InnoDB的很多优势特性需要启用InnoDB Plugin组件。要考虑过渡到InnoDB表是默认的最近的版本，请参见[第14.2.1.1节，InnoDB作为默认的存储引擎][14.02.01.01]。

InnoDB表非常适合热备(***hot backup***)。要了解MySQL企业备份产品(***MySQL Enterprise Backup***)在不打断正常进程的情况下备份MySQL服务的信息，请参见[第24.2节，MySQL企业备份][24.02.00]。

参见 [ACID], [hot backup], [storage engine], [transaction].

### <a name="glos_innodb_autoinc_lock_mode"></a>innodb_autoinc_lock_mode: innodb参数，不用译
`innodb_autoinc_lock_mode`控制自增锁(***auto-increment locking***)所使用的算法。当你有一个自增主键(***primary key***)时，在设置`innodb_autoinc_lock_mode=1`的情况下，你只能使用基于语句的复制。这个设置也叫连续锁模式，因为一个事务中的多行插入会接收到连续的自增值。如果你使用了允许更高并发的插入操作`innodb_autoinc_lock_mode=2`，就要使用基于行的复制，而不是基于语句的复制。这个设计叫交错(***interleaved***)锁模式，因为同一时间运行的多个多行插入可以接到交错的自增值。设置`innodb_autoinc_lock_mode=0`是之前的(传统)的默认设置，在处理兼容时可能会被用到。

参见 [auto-increment locking], [mixed-mode insert], [primary key].
### <a name="glos_innodb_file_format"></a>innodb_file_format: innodb参数，不用译
在你指定了`innodb_file_format`选项的一个值以后，所有创建InnoDB表空间的文件格式(***file format***)都取决于这个选项。要创建不同于系统表空间(***system tablespace***)的表空间(***tablespace***)，你也必须使用***file-per-table***选项。目前，你可以指定***Antelope***和***Barracuda***文件格式。

参见 [Antelope], [Barracuda], [file format], [file-per-table], [innodb_file_per_table], [system tablespace], [tablespace].

### <a name="glos_innodb_file_per_table"></a>innodb_file_per_table: innodb参数，不用译
这是一个影响InnoDB文件存储. 功能可用性及I/O好多方面的非常重要的配置。在MySQL 5.6.7之前，它是默认关闭的。`innodb_file_per_table`选项打开了file-per-table模式，它将每个新创建的InnoDB表和关联的索引存储在系统表空间(***system tablespace***)之外自己的.ibd文件(***.ibd file***)中。

这个选项会影响到一些SQL语句的性能与存储方面的考虑，比如`DROP TABLE`和`TRUNCATE TABLE`。

很多InnoDB的其它特性也需要它来充分发挥优势，比如表压缩(***compression***)或用MySQL企业备份(***MySQL Enterprise Backup***)来备份指定的表。

这个选项曾经是静态的，不过现在可以用`SET GLOBAL`命令来设置了。

如需参考信息，参考[innodb_file_per_table]。如需使用信息，参见[第14.2.6.2节，InnoDB File-Per-Table模式][14.02.06.02]。

参见 [compression], [file-per-table], [.ibd file][ibd file], [MySQL Enterprise Backup], [system tablespace].

### <a name="glos_innodb_lock_wait_timeout"></a>innodb_lock_wait_timeout: innodb参数，不用译
innodb_lock_wait_timeout选项在等待被共享的资源变得可用与放弃并在你的应用中处理错误. 重试或做替代处理二者之间设置一个平衡。任何等待获取锁超过指定时间的InnoDB事务都会被回滚。这在处理由更新多个不同存储引擎表时引起的死锁时非常有用；这类死锁是没法自动检测的。

参见 [deadlock], [deadlock detection], [lock], [wait].

### <a name="glos_innodb_strict_mode"></a>innodb_strict_mode: innodb参数，不用译
The innodb_strict_mode option controls whether InnoDB operates in strict mode, where conditions that are normally treated as warnings, cause errors instead (and the underlying statements fail).
innodb_strict_mode选项控制InnoDB的操作是否在严格模式下，那些在普通模式下被视为警告的问，在严格模式下都会用错误来代替(及相关的语句错误)。

This mode is the default setting in MySQL 5.5.5 and higher.
该模式在MySQL 5.5.5及更高版本中是默认设置。

参见 [strict mode].

### <a name="glos_insert"></a>insert: 插入
SQL中一个主要的DML操作。将百万行数据加载进表中的数据仓库系统和很多可能向同一张表中插入无序行的并发连接的OLTP系统中，插入性能是一个关键因素。如果插入性能对于很重要，你可能要学习InnoDB诸如变量缓冲中所用到的插入缓冲和自增列等特性。

参见 [auto-increment], [change buffering], [data warehouse], [DML], [InnoDB], [insert buffer], [OLTP], [SQL].

### <a name="glos_insert_buffer"></a>insert buffer: 插入缓冲，变更缓冲以前的叫法
变更缓冲(***change buffer***)以前的叫法。现在变更缓冲技术(***change buffering***)包括删除缓冲. 更新缓冲以及插入缓冲，“变更缓冲”是首选术语。

参见 [change buffer], [change buffering].

### <a name="glos_insert_buffering"></a>insert buffering: 插入缓存技术
一种技术，将由`INSERT`操作引起的二级索引的变更存储在插入缓冲(***insert buffer***)中，而不是直接写它们，这样物理写就可以以最小的随机I/O来执行了。它是变更缓冲技术(***change buffering***)的一种；其它的为删除缓冲技术(***delete buffering***)与清除缓冲技术(***purge buffering***)。

如果二级索引为唯一(***unique***)索引，插入缓冲技术是无用的，因为新值的唯一性在新的实体写入之前是无法验证的。其它变更缓冲技术对唯一索引有效。

参见 [change buffer], [change buffering], [delete buffering], [insert buffer], [purge buffering], [unique index].

### <a name="glos_instance"></a>instance: 实例
一个单独的***mysqld***后台驻留程序(***daemon***)，管理代表一个或多个数据库的一个数据目录(***data directory***)，每个数据库都包括一组表(***table***)。在开发. 测试和一些复制(***replication***)场景下，一台机器多个实例是很正常的事，每个管理自己的数据目录，监听各自的端口或套接字。在有一个实例运行在基于磁盘(disk-bound)性能的情况下，服务器应该还有额外的CPU和内存能力来运行更多的实例。

参见 [datdirectory], [database], [disk-bound], [mysqld], [replication], [server].

### <a name="glos_instrumentation"></a>instrumentation: 监测
为调优与调试收集性能数据而在源码级做的修改，通过监测收集到的数据使用`INFORMATION_SCHEMA`和`PERFORMANCE_SCHEMA`数据库通过SQL接口暴露出来。

参见 [INFORMATION_SCHEMA], [Performance Schema].

### <a name="glos_intention_exclusive_lock"></a>intention exclusive lock: 意向排它锁
参见 [intention lock].

### <a name="glos_intention_lock"></a>intention lock 意向锁
一种表级锁，常常指的是那种事务试图在表行上获取的锁。不同在事务可以在同一张表上获取到不同的意向锁，但第一个事务在表上获取一个意向排它锁(***intention exclusive***)以阻止其它事务再在该表上获取任何共享锁或排它锁。相反地，第一个事务在表上获取一个意向共享锁(***intention shared***)以阻止其它事务再在该表上获取任何排它锁。两阶段进程允许锁请求按序解决，而不用阻塞锁和兼容的相应的操作。如需各多此类锁机制的详情，请参考[第14.2.2.3节，InnoDB锁模式][14.02.02.03]。

参见 [lock], [lock mode], [locking].

### <a name="glos_intention_shared_lock"></a>intention shared lock: 意向共享锁
参见 [intention lock].

### <a name="glos_intention_inverted_index"></a>inverted index: 倒排索引
为文档索引系统优化的数据结构，用在InnoDB全文检索(***full-text search***)实现中。InnoDB全文索引(***FULLTEXT index***)，以倒排索引的方式实现，记录每个词在文档中的位置，而不是表中行的位置。单列的值(做为字符串存储的一个文档)可以由多个反向索引中的多个实体所表示。

参见 [full-text search], [FULLTEXT index], [ilist].

### <a name="glos_iops"></a>IOPS: 每秒读写次数，可不译
每次读写次数(***I/O operations per second***)的首字母缩写。繁忙系统，特别是***OLTP***应用的一个通用测。如果这个值接近存储设备可以处理的最大值，该应用会变成磁盘受限(***disk-bound***)，扩展性(***scalability***)也受到限制。

参见 [disbound], [OLTP], [scalability].

### <a name="glos_isl_file"></a>.isl file: .isl文件
在MySQL 5.6及更高版本中，一个用来指定由用`DATA DICRECTORY = `字句创建的InnoDB表的.ibd文件(***.ibd file***)位置的文件。它的作用就像符号链接，只是没有实际符号链接机制中平台限制。你可以在数据库(***database***)目录之外存储InnoDB表空间(***tablespace***)，例如，根据表的用途，可以放在特别大或特别快的存储设备上。如需更多详情，参参[第14.2.6.4节，指定表空间的位置][14.02.06.04]。

参见 [database], [.ibd file][ibd file], [table], [tablespace].

### <a name="glos_isolation_level"></a>isolation level: 事务隔离级别
数据库进程基础之一。隔离性是缩写***ACID***中的I；隔离级别是在多个事务(***transaction***)在同一时间产生变更与执行查询的情竞下，对性能与可靠性. 一致性和结果再生性之间进行微调的设置。

一致性与保护制度从高到低，InnoDB所支持的隔离级别为：***SERIALIZABLE***. ***REPEATABLE READ***. ***READ COMMITTED***和***READ UNCOMMITTED***。

对于InnoDB表，很多用户可以为所有的操作保留默认的隔离级别(***REPEATABLE READ***)。专家用户可以选择***read committed***级别，因为他们追求OLTP进程的扩展性极限，或在数据仓库操作中较小的不一致不会影响到大量数据的聚合结果。两头的级别(***SERIALIZABLE***和***READ UNCOMMITTED***)改变处理的行为的程度很大，所以很少用它们。

参见 [ACID], [READ COMMITTED], [READ UNCOMMITTED], [REPEATABLE READ], [SERIALIZABLE], [transaction].

## <a name="J"></a>J ##
### <a name="glos_join"></a>join: 关联
通过引用表中保存相同值的列，从超过一个表中取回数据的查询(***query***)。理想情况下，这些列是InnoDB外键(***foreign key***)关系中的一部分，它们确保参照完整性(***referential intgrity***)，并且关联的列上是有索引(***index***)的。经常用来节省空间和在范式(***normalized***)设计通过将重复的字符串用数据ID替换来提高性能。

参见 [foreign key], [index], [normalized], [query], [referential integrity].

## <a name="K"></a>K ##
### KEY_BLOCK_SIZE: InnoDB表选项
用来指定使用了压缩行格式(***compressed row format***)的InnoDB表中数据页大小的选项。默值为8KB。越小的值有达到内部限制的风险，该限制依赖于行大小和压缩比的组合。

参见 [compressed row format].


## <a name="L"></a>L ##

### <a name="glos_latch"></a>latch: 闩锁
InnoDB针对自己内部内存结构体实现锁(***lock***)的一个轻量级的结构体，通常保持毫秒或微秒级的短暂的时间。包含互斥(***mutex***，对于排它访问)和读写锁(***rw-lock***，对于共享访问)一般术语。某些闩锁的重点在性能调优上，比如数据字典(***data dictionary***)互斥。对于锁使用和竞争的统计可以通过Performance数据库(***Performance Schema***)接口获得。

参见 [data dictionary], [lock], [locking], [mutex], [Performance Schema], [rw-lock].

### <a name="glos_list"></a>list: buffer页面lru链表
InnoDB buffer pool相当于一个内部页的链表。这个链表在新页被访问或进入buffer pool. buffer pool中的页被再次访问和认为更新些以及长时间非被访问的页从buffer pool被逐出等情况下会被重新排序。buffer pool实际上被划分为子列表，并且替换策略是LRU机制的一个变种。

参见 [buffer pool], [eviction], [LRU], [sublist].

### <a name="glos_lock"></a>lock: 锁
控制访问诸如表. 行或内部数据结构等资源的对象的高级的概念，是锁(***locking***)机制中的一部分。针对进一步的性能调优，你可以探索实现了锁的真正的结构体，如互斥锁和闩锁(***latch***)。

参见 [latch], [lock mode], [locking], [mutex].

### <a name="glos_lock_escalation"></a>lock escalation 锁晋级
某些数据库系统使用的一种操作，将多行的锁合并为一个单独的表锁，节省内存空间，但降低对表的并发访问。InnoDB针对行锁使用一个空间高效的方式，所以不需要锁晋级。

参见 [locking], [row lock], [table lock].

### <a name="glos_lock_mode"></a>lock mode: 锁模式
一个共享锁(S)允许事务读一行。多个事务可以在同一时间在同一行上获取一个S锁。

一个排它锁允许事务更新或删除一行。其它的事务在同一时刻不再能获得任何类型的锁。

意向锁适用于表级，并且常常指的是事务试图在表行上获取的那种锁。不同在事务可以在同一张表上获取到不同的意向锁，但第一个事务在表上获取一个意向排它锁(***intention exclusive***)以阻止其它事务再在该表上获取任何共享锁或排它锁。相反地，第一个事务在表上获取一个意向共享锁(***intention shared***)以阻止其它事务再在该表上获取任何排它锁。两阶段进程允许锁请求按序解决，而不用阻塞锁和兼容的相应的操作。

参见 [intention lock], [lock], [locking].

### <a name="glos_locking"></a>locking: 锁机制
防止一个事务(***transaction***)查询或变更正在被其它事务查询或变更的数据的系统。锁策略一定要衡量数据库操作的可靠性及一致性(***ACID***理念的原则)与良好的并发(***concurrency***)所需的性能之间关系。微调锁策略往往会涉及选择一个隔离级别(***isolation level***)并保证你所有的数据库操作对于该隔离级别都是安全的和可靠的。

参见 [ACID], [concurrency], [isolation level], [latch], [lock], [mutex], [transaction].

### <a name="glos_locking_read"></a>locking read: 加锁读
在一个InnoDB表上同时执行了加锁(***locking***)操作的`SELECT`语句。无论是`SELECT ... FOR UPDATE`或是`SELECT LOCK IN SHARE MODE`。取决于事务的隔离级别(***isolation level***)，它有产生死锁(***deadlock***)的潜在可能性。与它对应的是无锁读(***non-locking read***)。在只读事务中不允许对全局表做此类操作。

参见 [deadlock], [isolation level], [locking], [non-locking read], [read-only transaction].

### <a name="glos_log"></a>log: 日志
在InnoDB语境中，“log”和“log files”通常指的是表示为ib_logfile*文件的redo日志(***redo log***)。另一个log区是undo日志(***undo log***)，它是物理系统表空间(***system tablespace***)的一部分。

其它MySQL很重要的日志就是错误日志(***error log***，用来诊断启动与运行时错误). 二进制日志(***binary log***，用来做复制和执行定点恢复). 数据库常规日志(***general query log***，用来诊断应用错误)和慢查询日志(***slow query log***，用来诊断性能问题)。

参见 [binary log], [error log], [general query log], [ib_logfile], [redo log], [slow query log], [system tablespace], [undo log].

### <a name="glos_log_buffer"></a>log buffer: 日志缓冲
一个内存区，保存要写到由redo日志(***redo log***)组成的日志文件(***log file***)中的数据。由配置选项[innodb_log_buffer_size]控制。

参见 [log file], [redo log].

### <a name="glos_log_file"></a>log file: 日志文件
组成redo日志的ib_logfileN中的一个文件。数据从日志缓冲内存区写入到这些文件中。

参见 [ib_logfile], [log buffer], [redo log].

### <a name="glos_log_group"></a>log group: 日志组
组成redo日志(***redo log***)的文件集合，通常以`ib_logfile1`和`ib_logfile2`。(由于这个原因，有是统称为***ib_logfile***。)

参见 [ib_logfile], [redo log].

### <a name="glos_logical"></a>logical: 逻辑
涉及高层的. 诸如表. 查询. 索引以及其它SQL概念的抽象角度的操作。通常地，逻辑角度对于数据库管理和应用部署的易用性与实用性都是非常重要的。与它对应的是物理(***physical***)。

参见 [logical backup], [physical].

### <a name="glos_logical_backup"></a>logic backup: 逻辑备份
一个不用拷贝实际的数据文件，重新生成表结构与数据的备份(***backup***)。例如，`mysqldump`命令会产生一个逻辑备份，因为它的输出包含诸如可以重建表的`CREATE TABLE`和`INSERT`语句。与它相应的是物理备份(***physical backup***)。逻辑备份提供了灵活性(比如，你可以在恢复前修改表的定义或插入语句)，但要比物理备份花销更长的时间。

参见 [backup], [mysqldump], [physical backup], [restore].

### <a name="glos_loose"></a>loose_: 一个前缀，不译
在MySQL 5.1中，在服务启动后安装InnoDB Plugin时，加在InnoDB配置选项前的一个前缀，这样避免了任何当前版本中没有注册过的新配置选项所导致的启动失败。如果该前缀后面的部分不是一个注册过的选项，MySQL在处理此前缀开始的配置选项时，会给出一个警告，而不是启动失败。

参见 [plugin].

### <a name="glos_low_water_mark"></a>low-water mark: 下限
一个代表着低值的限制的数值.一般来说,是一个阈值,该阈值的作用是一旦达到这个阈值,一些纠错动作会开始或者变得更活跃。与它对应的是上限(***high-water mark***)。

参见 [high-water mark].

### <a name="glos_lru"></a>LRU: 最近最少使用
最近最少使用(***least recently used***)的首字母缩写，一个管理存储空间的常用方法。当空间中需要缓存新的项目时，那些最近没有被使用到的项目会被驱逐出去。InnoDB默认使用LRU机制管理***buffer pool***中的页(***page***)，但在一个页可能只读一次的情况下会有个例外，比如在一次全表扫描(***full table scan***)过程中。LRU算法的变体叫中值插入策略。buffer pool的管理方法与传统的LRU算法不同之处在于它是通过[innodb_old_blocks_pct]. [innodb_old_blocks_time]和MySQL 5.6中的选项[innodb_lru_scan_depth]及[innodb_flush_neighbors]来微调的。

参见 [buffer pool], [eviction], [full table scan], [midpoint insertion strategy], [page].

### <a name="glos_lsn"></a>LSN: 日志序号
日志序列号的首字母缩写。这个单调递增的值代表了redo日志中所记录的操作所对应的时间点。(这个时间点不会理会事务边界；它可以落在一个或多个事务的中间。)它用在InnoDB内部的崩溃恢复和管理buffer pool中。

在MySQL 5.6.3之前，LSN是一个4字节无符号整型值，在MySQL 5.6.3中，当redo日志的大小限制从4GB变到512GB时，LSN变成8字节无符号整型值，附加的字节被用来存储额外的大小信息。在MySQL 5.6.3或更晚的版本上编译的应用可能会用到64位，而不是32位变更来存储和比较LSN的值。

在MySQL企业备份产品中，你可以指定一个相当于时间点的LSN来生成一个增量备份。相关的LSN会在mysqlbackup命令的输出中显示。一旦你有了一个全备的相当于时间点的LSN，你就可以指定一个值来生成一个后续的增量备份，它的输入中包含另一个下次增量备份的所需的LSN。

参见 [crash recovery], [incremental backup], [MySQL Enterprise Backup], [redo log], [transaction].


## <a name="M"></a>M ##

### <a name="glos_master_server"></a>master server: 主服务器
经常简称为“master”。复制(***replication***)环境中的一个数据库服务机器，用来处理对数据的最初的插入. 更新和删除请求。这些数据被传送到并在其上重复执行的其它服务器叫做从服务器(***slave servers***)。

参见 [replication], [slave server].

### <a name="glos_master_thread"></a>master thread: 主线程
一个在后台执行各种任务的InnoDB线程(***thread***)。大多数情况是I/O相关的，比如从插入缓冲(***insert buffer***)中往相关的二级索引中写入变更。

为了提高并发(***concurrency***)，有时候行为会从主线程转移到单独的后台线程中。比如，在InnoDB 5.6及更高版本中，脏页(***dirty pages***)会由页清理器(***page cleaner***)从***buffer pool***中刷新，而不是由主线程执行。

参见 [buffer pool], [dirty page], [flush], [insert buffer], [page cleaner], [thread].

### <a name="glos_mdl"></a>MDL: 元数据锁
metadata lock的简称。

参见 [metadata lock].

### <a name="glos_memcached"></a>memcached: 不译
一个众多MySQL和***NoSQL***软件栈中流行的组件，允许快速读写单值并将结果完整地缓存在内存中。传统上，应用需要额外的逻辑往MySQL数据库中写入相同的数据来达到持久化，或者在数据还没有在内存中缓存时需要从MySQL数据库中读取数据。现在，应用可以使用简单的**memcached**协议来直接使用***InnoDB***或MySQL集群的表来与MySQL服务通信了，大多数据语言都有支付该协议的客户端。这些MySQL表的NoSQL接口允许应用达到比直接使用SQL命令更高的读写性能，并且可以简化那些已经为内部缓存收纳了**memcached**的系统的应用逻辑与部署配置。

InnoDB表的memcached接口在MySQL 5.6及更高版本中可能；参考[第14.2.17节，InnoDB集成memcached][14.02.17]；细节参考[http://dev.mysql.com/doc/ndbapi/en/ndbmemcache.html]。

参见 [InnoDB], [NoSQL].

### <a name="glos_merge"></a>merge: 合并
将变更应用到内存中缓存的数据上，比如当一个页被加载到***buffer pool***中时，以及任何在变更缓冲(***change buffer***)中记录的可应用的变更纳入进buffer pool中。更变过的数据最终由刷新(***flush***)机制写入到表空间(***tablespace***)中。

参见 [buffer pool], [change buffer], [flush], [tablespace].

### <a name="glos_metadata_lock"></a>metadata lock: 元数据锁
一种锁(***lock***)类型，为了防止同一时间另一事务(***transaction***)正在使用表时的***DDL***操作。如需更多细节，参考[第8.10.4节，元数据锁][08.10.04]。

特别是在MySQL 5.6及更高版本中，对在线(***online***)操作的改进都集中在减少元数据锁的量上。目的是当某表被其它事务查询以及更新等时，对于不改变表结构的DDL操作(诸如针对InnoDB表的`CREATE INDEX`和`DROP INDEX`操作)可以继续。

参见 [DDL], [lock], [online], [transaction].

### <a name="glos_metrics_counter"></a>metrics counter: 计数器
在MySQL 5.6及更高版本中，一个由information_schema库中`innodb_metrics`实现的特性。你可以查询低级别的InnoDB操作的次数(***counts***)和总数，以及使用这些结果结合***performance_schema***库中的数据来进行性能调优。

参见 [counter], [INFORMATION_SCHEMA], [Performance Schema].

### <a name="glos_midpoint_insertion_strategy"></a>midpoint insertion strategy: 中间插入策略
是将最初的页不加载到InnoDB ***buffer pool***中“最新”列表的最后，而是放在中间某个位置的技术。具体的位置点可以不同，基于[innodb_old_blocks_pct]选项的设定。意图是只读
一次的块，诸如在全表扫描(***full table scan***)过程中，可以比根据严格的***LRU***算法更快地老化出buffer pool。

参见 [buffer pool], [full table scan], [LRU], [page].

### <a name="glos_mini_transaction"></a>mini-transaction: 迷你事务
在***DML***操作中，在物理(***physical***)层对内部数据结构进行变更时InnoDB所处理的一个内部阶段。迷你事务没有回滚(***roll back***)的概念；多个迷你事务可以发生在一个事务(***transaction***)中。迷你事务的信息写入到崩溃恢复(***crash recovery***)期间使用的redo日志(***redo log***)中。迷你事务也可以发生在常事务环境之外，例如在后台线程所处理的清除(***purge***)操作期间。

参见 [commit], [crash recovery], [DML], [physical], [purge], [redo log], [rollback], [transaction].

### <a name="glos_mixed_mode_insert"></a>mixed-mode insert: 混合模式插入
一个对新行指定了部分但没有指定所有自增(***auto-increment***)值的`INSERT`语句。例如，一个多值`INSERT`可能在一些情况下为自增列指定值，在别的情况下为`NULL`值。`InnoDB`在自增列被指定为`NULL`时会生成自增值。另一个例子是`INSERT ... ON DUPLICATE KEY UPDATE`语句，其中自增值可以生成但用不到，任何重复的行都会以`UPDATE`语句来处理，而不是以`INSERT`语句。

可以导致复制配置中的主库和从部数据不一致。可以要求调整innodb_autoinc_lock_mode配置选项的值。

参见 [auto-increment], [innodb_autoinc_lock_mode], [master server], [replication], [slave server].

### <a name="glos_mrg_file"></a>.MRG file: .MRG文件
MERGE存储引擎使用的一个文件，包含对其它表的引用情况。此后缀的文件总是包含在由MySQL企业备份产品(***MySQL Enterprise backup***)中mysqlbackup命令(***mysqlbackup command***)所生成的备份中。

参见 [MySQL Enterprise Backup], [mysqlbackup command].

### <a name="glos_multi_core"></a>multi-core: 多核
可以利用多线程程序(如MySQL服务)优势的一种处理器。

### <a name="glos_multiversion_concurrency_control"></a>multiversion concurrency control: 多版本并发控制
见 [MVCC].

### <a name="glos_mutex"></a>mutex: 互斥
“互斥量(***mutex variable***)”的非式缩写。(Mutex自身是mutual exclusion的缩写。)是InnoDB对内部内存中的数据结构体用来表示或强制排它访问锁(***lock***)的低级对象。当这个锁被获取，任何其它的进程. 线程以及其它都被阻止获取相同的锁。与之相对的读写锁(***rw-lock***)，是允许共享访问的。互斥与读写锁一并称为闩锁(***latch***)。

参见 [latch], [lock,] [Performance Schema], [Pthreads], [rw-lock].

### <a name="glos_mvcc"></a>MVCC: 多版本并发控制
“multiversion concurrency control”的首字母缩写。这种技术让InnoDB事务可以在一定的隔离级别(***isolation levels***)写执行一致性读(***consistent read***)操作；也就是说，查询那些正在被其它事务更新的行，并且能看到那些更新发生前的值。这对于提高并发来说是一个强大的功能，它在不用等待其它事务持有的锁的情况下允许查询继续执行。

这种技术在数据库界并不常见。一些数据库产品，以及一些其它的MySQL存储引擎都不支持它。

参见 [ACID], [concurrency], [consistent read], [isolation level], [lock], [transaction].

### <a name="glos_my_cnf"></a>my.cnf: 配置文件(Unix/Linux)
Unix或Linuxt系统下MySQL配置文件名。

参见 [my.ini], [option file].

### <a name="glos_my_ini"></a>my.ini: 配置文件(Windows)
Windows系统下MySQL配置文件名。

参见 [my.cnf], [option file].

### <a name="glos_myd_file"></a>.MYD file: .MYD文件
MySQL用来存储MyISAM表数据的文件。

参见 [.MYI file][myi file], [MySQL Enterprise Backup], [mysqlbackup command].

### <a name="glos_myi_file"></a>.MYI file: .MYI文件
MySQL用来存储MyISAM表索引的文件。

参见 [.MYD file][myd file], [MySQL Enterprise Backup], [mysqlbackup command].

### <a name="glos_mysql"></a>mysql: mysql(客户端)
`mysql`程序是MySQL数据库的命令行解释器。它通过请求***mysqld***后台驻留程序来处理***SQL***语句和一些MySQL特定的命令，诸如`SHOW TABLES`。

参见 [mysqld], [SQL].

### <a name="glos_mysql_enterprise_backup"></a>MySQL Enterprise Backup: MySQL企业备份
一个执行MySQL数据库热备(***hot backup***)的授权产品。它提供最高效可靠的***InnoDB***表备份，但也能备份MyISAM和其它类型的表。

参见 [hot backup], [InnoDB].

### <a name="glos_mysqlbackup_command"></a>mysqlbackup command: mysqlbackup命令
一个MySQL企业备份(***MySQL Enterprise Backup***)的命令行工具。它对InnoDB表执行热备(***hot backup***)操作，并对MyISAM和其它类型表执行温备(***warm backup***)操作。如需更多关于该命令行的信息，请参考[第24.2节，MySQL企业备份][24.02.00]。

参见 [hot backup], [MySQL Enterprise Backup], [warm backup].

### <a name="glos_mysqld"></a>mysqld: MySQL daemon(Unix)或MySQL service(Windows)
`mysqld`程序是MySQL数据库的数据库引擎。它以Unix后台驻留程序或Windows服务的型式运行，在后台持续等待请求并执行维护工作。

参见 [mysql].

### <a name="glos_mysqldump"></a>mysqldump: mysqldump命令
一个执行数据库. 表和表数据混合体逻辑备份(***logical backup***)的命令。结果是可以重现原始结构对象. 数据或两都的SQL语句。对于大量的数据，像MySQL企业备份(***MySQL Enterprise Backup***)这样的物理备份(***physical backup***)解决方案是非常快速的，特别是对于恢复(***restore***)操作来说。

参见 [logical backup], [MySQL Enterprise Backup], [physical backup], [restore].

## <a name="N"></a>N ##
### <a name="glos_natural_key"></a>natural key: 自然主键
一个索引列，通常是主键(***primary key***)，其中的值是有现实意义的。通常不建议这么做，因为：

* 如果值万一变了，会有许多潜在的索引维护工作来重排簇索引(***clustered index***)，并且更新在每一个二级索引(***secondary index***)里重复出现的主键拷贝。

* 即使看似稳定的值也会以一种不可预测的方式改变，很难在数据库中正确地表示改变。举个例子，一个国家可以变成两个或更多，这会让之前的国家码过时。或者，唯一值的规则可能发生异常。举个例子，即使纳税人的身份证号的初衷是一人一个，但数据库可能需要处理违犯规则的记录，如身份证被盗这种事儿。纳税人的身份证和其它敏感ID也很少做为主键，因为它们需要被保护. 加密以及其它不同于它列的对待。

因此，使用任意数字来组成一个人造(***synthetic key***)的键通常来说是更好的选择，比如使用自增列(***auto-increment***)。

参见 [auto-increment], [primary key], [secondary index], [synthetic key].

### <a name="glos_neighbor_page"></a>neighbor page: 相邻页
相同簇(***extend***)中的任何一个页。当一个页(***page***)被选中用来刷新(***flush***)时，作为传统硬盘的I/O优化器会将任何相邻的脏页(***dirty page***)通常也被刷新。在MySQL 5.6及更高版本中，该行为可以被配置变量[innodb_flush_neighbors]所控制；你可以为SSD磁盘关掉该选项，它在写更小批量数据的随机查找上不会产生相同的负载。

参见 [dirty page], [extent], [flush], [page].

### <a name="glos_next_key_lock"></a>next-key lock: 行间隙锁
一个索引记录(***index record***)上记录锁和索引记录前间隙上间隙锁(***gap lock***)的组合。

参见 [gap lock], [locking], [record lock].

### <a name="glos_non_blocking_io"></a>non-blocking I/O: 同AIO
专业术语，异步I/O(***asynchronous I/O***)的同义词。

参见  [asynchronous I/O].

### <a name="glos_non_blocking_read"></a>non-locking read: 不加锁读
没有使用`SELECT ... FROM UPDATE`或`SELECT ... LOCK IN SHARE MODE`子句的查询(***query***)。在只读事务(***read-only transaction***)中全局表所允许的唯一的查询类型。与之相对的是加锁读(***locking read***)。

参见 [locking read], [query], [read-only transaction].

### <a name="glos_non_repeatable_read"></a>non-repeatable read: 非重复读
这种情况下，一个查询检索了数据，随后一个查询在同一个事务(***transaction***)中检打算检索相同的数据，但是却返回了不同的结果(期间被另一个事务的提交所变更)。

这种操作类型与数据库设计的***ACID***理念相违背。在一个事务中，数据应该是一致的，有可预知和稳定的关系。

Among different isolation levels, non-repeatable reads are prevented by the serializable read and repeatable read levels, and allowed by the consistent read, and read uncommitted levels.

在不同的隔离级别(***isolation levels***)中，非重复读可以通过可序列化读(***serializable read***)和可重复读(***repeatable read***)来避免，在一致性读(***consistent read***)，也就是未提交读(***read uncommitted***)级别中是允许的。

参见 [ACID], [consistent read], [isolation level], [READ UNCOMMITTED], [REPEATABLE READ], [SERIALIZABLE], [transaction].

### <a name="glos_normalized"></a>normalized: (符合)范式的
一个数据库设计策略，其中数据分拆到多个表中，并且重复的值简化为由一个ID代表的行，来避免存储. 查询和更新冗余或冗长的值。它通常用联机事务处理(***OLTP***)应用中。

举个例子，一个地址可能会给定一个唯一ID，这样一个普查的数据库可以通过将一个家庭中的每个成员与地址ID关联在一起来表现住在该地址下(***lives at this address***)的关系，而不用存储一个复杂值的多个拷贝，如中国北京前门外大街皮条胡同(***123 Main Street, Anytown, USA***)。

再举个例子，虽然一个电话本应用会把每个人的名字和地址连同电话号码存到同一张表中，但一个电话公司的数据库可能会给每个电话号码一个指定的ID，并将号码和ID存到一个独立的表中。这种范式的表现方式可以简化在区号分拆时的大范围的更新。

范式化也不总是推荐使用。主要用来查询且只在完全删除和加载时被更新的数据常常保存在更少. 更大的表中，重复的值存在冗余拷贝。这种数据表现方式叫反范式(***denormalized***)，在数据仓库应用中十分常见。

参见 [denormalized], [foreign key], [OLTP], [relational].

### <a name="glos_nosql"></a>NoSQL: NoSQL
表示一组数据访问技术的广泛的术语，它不使用***SQL***语句作为它们读写数据的主要途径。一些NoSQL技术是键-值存储，只接受单值的读写；一些放松了***ACID***方法的限制；还有一些不需要预先认定的结构(***schema***)。MySQL用户可以通过使用***memcached*** API直接访问一些类型的MySQL表，将NoSQL风格进程的快速与简单和SQL操作的灵活与方便结合起来。针对InnoDB表的***memcached***接口在MySQL 5.6及更高版本中可能；如需更多细节，参考[第14.2.16节，InnoDB集成***memcached***][14.02.16]。针对MySQL Cluster的memached接口在MySQL CLuster 7.2版中可用，如果更多细节，请参考[http://dev.mysql.com/doc/ndbapi/en/ndbmemcache.html]。

参见 [ACID], [InnoDB], [memcached], [schema], [SQL].

### <a name="glos_not_null_constraint"></a>NOT NULL constraint: 非空约束
具体指定一列(***column***)不能包含任何空(***NULL***)值的一类约束(***constraint***)。它有助于保护引用一致性(***referential integrity***)，数据库服务器可以识别错误遗漏值的数据。它也可以让优化器来预计一个列上索引中实体的数目，而有助于查询优化器中的算法。

参见 [column], [constraint], [NULL], [primary key], [referential integrity].

### <a name="glos_null"></a>NULL: 空
一个***SQL***中特殊的值，用来指代数据的缺失。任何算术运算或等于测试都会引起一个空值，反过来会产生一个空的结果。(因此它类似于IEEE浮点原则中的NaN，“不是一个数据(***not a number***)”。)任何诸如`AVG()`这样的聚集计算在决定多少行需要做除数时会忽略掉含有空值的行。唯一可以测试空值的SQL语句是`IS NULL`或`IS NOT NULL`。

空值在索引操作中发挥作用，因为对于性能来说，一个数据库必须最小化为了保持跟踪缺失值的负载。通常地，空值不存在索引中，因为在一个在索引列上使用标准比较操作查询是不可能匹配到该列上含有空值的行。因为同样的原因，唯一索引不阻止空值；那些值根本不在索引中。在一个列上定义一个非空约束提供了一个没有行从索引中漏掉的保证，可以更好地查询优化(行的精确行数和评估是否使用索引)。

因为主键(***primary key***)必须能唯一地标识表中的每一行，一个单列主键不能包含任何空值，多列主键在所有列中都不能包含空值。

虽然Orcale数据库允许一个空值可以和字符串连结，但是InnoDB会把这样的操作结果视为空。

参见 [index], [primary key], [SQL].

## <a name="O"></a>O ##
### <a name="glos_off_page_column"></a>off-page column 跨页列
一个包含变长数据(诸如BLOB和VARCHAR)的列，其中数据太长而不能适用于B树(***B-tree***)页。数据存储在溢出页(***overflow page***)中。InnoDB ***Barracuda***文件格式中的动态(`DYNAMIC`)行格式对于这种存储来说，会比老的精简(`COMPACT`)行格式更有效。

参见 [B-tree], [Barracuda], [overflow page].


### <a name="glos_oltp"></a>OLTP: 在线联机查询
“在线联机查询(***Online Transaction processing***)”的简写。一个数据库系统，或一个数据库应用，运行很多事务(***transaction***)，伴随频繁的读写，通常一次只影响小部的数据。举个例子，一个航线预订系统或一个处理银行存款的应用。考虑到***DML***(insert/update/delete)效率和查询(***query***)效率的平衡，数据可能会以范式(***normalized***)形式组织。与之相对的是数据仓库(***data warehouse***)。

凭借其行级锁与事务能力，InnoDB是在应用中使用MySQL表的理想存储引擎。

参见 [data warehouse], [DML], [InnoDB], [query], [row lock], [transaction].

### <a name="glos_online"></a>online: 在线
一类不会引起宕机. 阻塞或限制操作数据库的操作。通常适用于***DDL***。缩短限制操作的操作，诸如快速索引创建(***fast index creation***)，在MySQL 5.6中已经大量引入了在线DDL操作(***online DDL***)。

在备份环境中，热备(***hot backup***)是一个在线操作，温备(***warm backup***)的一部分是在线操作。

参见 [DDL], [Fast Index Creation], [hot backup], [online DDL], [warm backup].

### <a name="glos_online_ddl"></a>online DDL: 在线DDL
一个在***DDL***(主要是`ALTER TABLE`)期间提高InnoDB表性能. 并发和可用性的特性。更多细节请参考[第14.2.11节，`InnoDB`和在线DDL]。

具体细节因操作类型的不同而不同。在某些情况下，表可以在ALTER TABLE运行的同时被并发修改。操作可能可以在不做表拷贝的情况下执行，或使用一个特殊优化类型的表拷贝。空间使用量由配置选项[innodb_online_alter_log_max_size]控制。

这个特征是MySQL 5.5和MySQL 5.1 InnoDB Plugin中快速索引创建(***Fast Index Creation***)的加强版。

参见 [DDL], [Fast Index Creation], [online].

### <a name="glos_opt_file"></a>.OPT file: .OPT文件
一个多包含数据库配置信息的文件。带有这个后缀名的文件总是包含在MySQL企业备份产品(***MySQL Enterprise Backup***)的mysqlbackup命令(***mysqlbackup command***)生成的备份中。

参见 [MySQL Enterprise Backup], [mysqlbackup command].

### <a name="glos_optimistic"></a>optimistic: 乐观的
一个引导关系型数据库系统低层实现决策的方法。在一个关系型数据库中对性能和并发(***concurrency***)的要求意味着操作必须快速启动或调度。对一致性和参照完整性(***referential integrity***)的要求意味着任何操作都有可能失败：一个事务可能回滚，一个***DML***操作可能违反约束，一个对锁的请求可能导致死锁，一个网络错误可能导致超时。乐观策略假设大多数请求或尝试都会成功，所以只做相对来说很小的工作来对付失败的情况。当这个假设为真时，数据库做少许不必要的操作；当请求失败了时，必须要额外的工作来清理和撤消变更。

InnoDB为锁(***locking***)和提交等操作采用乐观策略。例如，事务产生的数据变更会在提交(***commit***)发生前就写到数据文件中，使得提交本身非常快，但如果事务回滚时需要做更多的荏来撤消变更。

与乐观策略相对的是悲观(***pessimistic***)策略，其中的系统优化为处理不可靠靠或频繁失败的操作。这种方法在数据库系统中很罕见，因为更多关注选择可靠的硬件. 网络和算法。

参见 [commit], [concurrency], [DML], [locking], [pessimistic].

### <a name="glos_optimizer"></a>optimizer: 优化器
MySQL基于相关表(***table***)的特点与数据分布用，来决定为查询(***query***)采用最优索引(***index***)和关联(***join***)顺序的组件。

参见 [index], [join], [query], [table].

### <a name="glos_option"></a>option: 选项
一个MySQL的配置参数，既存在配置文件(***option file***)中，又可以通过命令行命令传递。

对于应用到(***InnoDB***)表上的选项，每个选项名都以前缀`innodb_`开头。

参见 [InnoDB], [option file].

### <a name="glos_option_file"></a>option file: 选项文件
保存MySQL实例配置选项(***option***)的文件，一般来说，在Linux和UNIX上，这个文件叫`my.cnf`，在Windows上，这个文件叫`my.ini`。

参见 [configuration file], [my.cnf], [option].

### <a name="glos_overflow_page"></a>overflow page 溢出页
单独申请用来存储因太长而不能放置B树(***B-tree***)页(***page***)的变长列(如`BLOB`和`VARCHAR`)的磁盘页。这些相关的列也叫页外列(***off-page column***)。

参见 [B-tree], [off-page column], [page].

## <name="P"></a>P ##
### <a name="glos_page"></a>page: 页
一个数据单元，表示InnoDB任何时刻在磁盘(数据文件，***data files***)与内存(***buffer pool***)之间传输的数据量。一个页可以包含一行或多行，取决于每行有多少数据。如果一行不能完整放到单个页中，InnoDB会设置一个指针类型数据结构，这样行的信息能存到一个页中。

让每行中可以放置更多数据的一种方法是使用压缩行格式(***compressed row format***)。对于使用BLOB或大文本段列的表，精简行格式(***compact row format***)可以让这些大列跟行中的其它内容分开来存储，针对那些没有引用到那些列的查询降低I/O负载和内存使用。

当InnoDB为了提高吞吐量而批量读写一组页时，它会一次读写一个簇(***extend***)。

一个MySQL实例中所有的InnoDB磁盘数据结构都使用同样的页大小(***page size***)。

参见 [buffer pool], [compact row format], [compressed row format], [data files], [extent], [page size], [row].

### page cleaner 页清理器(页清理线程)
一个InnoDB后台线程(***thread***)，用来从***buffer pool***中刷新脏页(***dirty page***)。在MySQL 5.6之前的版本中，该行为由主线程(***master thread***)执行。

参见 [buffer pool], [dirty page], [flush], [master thread], [thread].

### <a name="glos_page_size"></a>page size: 页大小
对于发布到MySQL 5.5版本，包括MySQL 5.5，每个InnoDB页(***page***)固定为16KB。这个值代表一个平衡：对于保存绝大多数行来说足够大，对减小加载不必要的数据到内存中的性能开销来说也足够小。其它值未经测试或不支持。

从MySQL 5.6开始，InnoDB实例(***instance***)的页大小可以是4KB. 8KB或16KB，由[innodb_page_size]配置选项控制。你在创建MySQL实例的时候设置这个值，之后它会一直保持不变。相同的页大小会应用到所有的InnoDB表空间(***tablespace***)中，无论是系统表空间(***system tablespace***)还是在***file-per-table***模式下创建的任何独立表空间。

更小的页大小有提升使用比较小的块大小的存储设备，特别是对磁盘受限系统(***disk-bound***)中的***SSD***设备来说，比如***OLTP***应用。当单独的行被更新时，更少的数据被拷贝到内存中. 写到磁盘. 重组及锁定等等。

参见 [disbound], [file-per-table], [instance], [OLTP], [page], [SSD], [system tablespace], [tablespace].

### <a name="glos_par_file"></a>.PAR file: .PAR文件
分区定义表。此后缀命的文件常常包含在由MySQL企业备份(***MySQL Enterprise Backup***)中mysqlbackup命令(***mysqlbackup command***)生产的备份中。

参见 [MySQL Enterprise Backup], [mysqlbackup command].

### <a name="glos_parent_table"></a>parent table: 父表
外键(***foreign key***)关系中保存从子表(***child table***)中指向初始列的值的表。在父表中删除或更新行的结果依赖于外键定义中的`ON UPDATE`和`ON DELETE`子句。子表中符合条件的值会被自动依次删除或更新，或这些列被设置为`NULL`，或操作被拒绝。

参见 [child table], [foreign key].

### <a name="glos_partial_backup"></a>partial backup: 部分备份
一个包含MySQL数据库中部分表(***table***). 或包含MySQL实例中部分数据库的备份。与之相对的是全备份(***full backup***)。

参见 [backup], [full backup], [table].

### <a name="glos_partial_index"></a>ppartial index: 部分索引
只一部分表示列值的索引，一般来说是长VARCHAR值的前N个字符(前缀，***prefix***)。

参见 [index], [index prefix].

### <a name="glos_performance_schema"></a>Performace Schema: 性能库
在MySQL 5.5及以上版本中，性能库(***performance_schema***)提供一组表，你通过它们可以查询到很多MySQL服务内部性能特性。

参见  [latch], [mutex], [rw-lock].

### <a name="glos_persistent_statistic"></a>persistent statistic: 持久统计
MySQL 5.6的特性，将InnoDB表(***table***)的索引(***index***)统计存储到磁盘上，为查询(***query***)提供更好的执行计划稳定性(***plan stability***)。

参见 [index], [optimizer], [plan stability], [query], [table].

### <a name="glos_pessimistic"></a>pessimistic: 悲观
一种牺牲性能或并发来获得安全的方法。它适用等请求或尝试可能失败的占比很高或失败请求的后果很严重的情况。InnoDB使用悲观锁(***locking***)机制来最小化死锁(***deadlock***)的机会。在应用层，你可以在通过在一开始就申请事务所需要的所有锁的悲观策略来避免死锁。

很多内置的数据库机制使用与它相对的乐观(***optimistic***)方法。

参见 [deadlock], [locking], [optimistic].

### <a name="glos_phantom"></a>phantom: 幻(读)
一个出现在查询结果集中，却没有在之前该查询结果集中出现的行。例如，如果一个查询在一个事务(***transaction***)中运行了两次，期间，另一个事务在新插入一行或更新一行后提交了所以在这个查询的`WHERE`子句中匹配到了。

这种情况叫幻读。这要比非重复读(***non-repeatable read***)要更难防御一些，因为锁住第一次查询结果集中的所有行并不能阻止导致幻读出现的变更。

在不同的隔离级别(***isolation level***)中，幻读在可序列化读(***serializable read***)级别是被阻止的，但在可重复读(***repeatable read***). 一致性读(***consistent read***)和未提交读(***read uncommitted***)级别是允许的。

参见 [consistent read], [isolation level], [non-repeatable read], [READ UNCOMMITTED], [REPEATABLE READ], [SERIALIZABLE], [transaction].

### <a name="glos_physical"></a>physical: 物理
涉及硬件相关方面的一类操作，如磁盘块. 内存页. 文件. 位及读盘等等。一般情况下，物理层面在专家级性能调优和问题诊断中是很重要的。与之相对的是逻辑(***logical***)。

参见 [logical], [physical backup].

### <a name="glos_physical_backup"></a>physical backup: 物理备份
一个拷贝实际数据文件的备份(***backup***)。例如，MySQL企业备份(***MySQL Enterprise Backup***)产品的mysqldump命令生成的就是物理备份，因为它的输出包含可以被mysqld直接使用的数据文件，这让恢复(***restore***)操作变得更快。与之相对的是逻辑备份(***logical backup***)。

参见 [backup], [logical backup], [MySQL Enterprise Backup], [restore].

### <a name="glos_pitr"></a>PITR: 定点恢复
定点恢复(***point-in-time recovery***)的简写。

参见 [point-in-time recovery].

### <a name="glos_plan_stability"></a>plan stability: 执行计划稳定性
一个查询执行计划(***query execution plan***)的属性，其中优化器对于给定的查询(***query***)总是做出相同的选择，这样性能就是不变的和可预知的了。

参见 [query], [query execution plan].

### <a name="glos_plugin"></a>plugin: 插件
在MySQL 5.1及更早的版本中，一个包含了对InnoDB存储引擎的特性与性能改善的独立可安装形式，这些改善在那些发行版中的内置InnoDB中并未包括。

在MySQL 5.5及更高版本中，MySQL分发版包含最新的InnoDB特性与性能的改善，即InnoDB 1.1，它不再是一个单独的InnoDB插件了。

差别主要在MySQL 5.1中，其中一个特性或bug修复可能要应用到InnoDB插件中，但不是内置的InnoDB中，反之亦然。

参见 [built-in], [InnoDB].

### <a name="glos_point_in_time_recovery"></a>point-in-time recovery: 定点恢复
通过恢复备份(***backup***)将数据库的状态重建到一个指定的日期与时间点的进程。通常简写为***PITR***。因为指定的时间点不太可能恰好就是备份的时间点，所以这项技术常常需要一个物理备份(***physical backup***)和一个逻辑备份(***logical backup***)的组合。例如，利用MySQL企业备份(***MySQL Enterprise Backup***)产品，你恢复了指定时间点前的最近一个备份，然后重放备份时间点与定点恢复时间点之间的二进制日志(***binary log***)中的变更。

参见 [backup], [logical backup], [MySQL Enterprise Backup], [physical backup], [PITR].

### <a name="glos_prefix"></a>prefix: 前缀

参见 [index prefix].

### <a name="glos_prepared_backup"></a>prepared backup: 一致备份
在所有二进制日志(***binary log***)与增量备份(***incremental backup***)应用阶段都完成后的一组备份文件，由MySQL企业备份(***MySQL Enterprise Backup***)产品生成。结果文件已为恢复(***restore***)做好准备。在应用步骤之前，这些文件叫原始备份(***raw backup***)。

参见 [binary log], [hot backup], [incremental backup], [MySQL Enterprise Backup], [raw backup], [restore].

### <a name="glos_primary_key"></a>primary key: 主键
可以在表中唯一确定每一行的一组列(注：基于这组列的索引)。因此，它必须是一个不含`NULL`值的唯一索引。

InnoDB要求每张表都有这样一个索引(也叫簇索引，***clustered index***或***cluster index***)，并且基于主键的列值组织表存储。

当选择一个主键值时，考虑使用任意值(人造键，***synthetic key***)，而依靠其它来源得出的值(自然键，***natural key***)。

参见 [clustered index], [index], [natural key], [synthetic key].

### <a name="glos_process"></a>process: 进程
一个正在执行的程序的实例。操作系统在多个运行的进程之间切换，允许一定级别的并发(***concurrency***)。在大多数据操作系统上，进程可以包含多个执行共享资源的线程(***thread***)。线程之间的上下文切换要快于进程之间的等效切换。

参见[concurrency], [thread].

### <a name="glos_pseudo_record"></a>pseudo-record: 伪记录
一个索引中人造的记录，用来锁定(***locking***)当前不存在的键值或范围。

参见 [infimum record], [locking], [supremum record].

### <a name="glos_pthread"></a>Pthread: 不译
POSIX线程标准，定义了UNIX和Linux系统上线程和锁操作API。在UNIX和Linux系统上，InnoDB使用为互斥(***mutex***)的使用它的实现。

参见 [mutex].

### <a name="glos_purge"></a>purge: 清除
由独立线程执行的一类垃圾回收，按周期表运行。清除包含这些动作：从索引中删去过期的值；物理删除被之前的`DELETE`语句标记为删除的行。

参见 [crash recovery], [delete], [doublewrite buffer].

### <a name="glos_purge_buffering"></a>purge buffering: 清除缓冲
在将在`DELETE`操作中的索引变更存储到插入缓冲(***insert buffer***)中而不是直接写盘的技术，这样物理写可以最小化随机I/O。(因为删除是两步操作，所以这个操作缓冲了正常清除之前标记为删除的索引记录的写操作。)它是变更缓冲(***change buffering***)的一种类型；其它类型为插入缓冲(***insert buffering***)和删除缓冲(***delete buffering***)。

参见 [change buffer], [change buffering], [delete buffering], [insert buffer], insert buffering.

### <a name="glos_purge_lag"></a>purge lag: 清除链表
InnoDB清除链表(***history list***)的另一种叫法。与[innodb_max_purge_lag]配置选项有关。

参见 [history list], [purge].

### <a name="glos_purge_thread"></a>purge thread: 清除线程
InnoDB进程中一个专门用来定期执行清除操作的线程。在MySQL 5.6及更高版本中，多清除线程可以用innodb_purge_thread配置选项来使其生效。

参见 [purge], [thread].

## <a name="Q"></a>Q ##
### <a name="glos_query"></a>query: 查询
在***SQL***中，一个从一张或多张表(***table***)中读取信息的操作。根据数据的组织和查询的参数不同，查找可能会通过查询(***index***)索引而优化。如果涉及多表，这个查询就叫做关联(***join***)。

因为历史原因，有时“查询”在更广义上被用作内部进程讨论的语句上，包括其它类型的MySQL语句，读如***DDL***和***DML***语句。

参见 [DDL], [DML], [index], [join], [SQL], [table].

### <a name="glos_query_execution_plan"></a>query execution plan: 查询执行计划
优化器关于如何最有效执行一个查询(***query***)的决策集，包括使用哪个或哪些索引(***index***)，以及其中表的关联(***join***)顺序。执行计划稳定性(***plan stability***)使得对于一个给定的查询，一直会选择相同的计划。

参见 [index], [join], [plan stability], [query].

### query log 查询日志

参见 [general query log].

### <a name="glos_quiesce"></a>quiesce: 系统静默状态
为了减少数据库的活动量，常常为诸如`ALTER TABLE`. 备份(***backup***)或关机(***shutdown***)而准备。有可能会引起尽可能多刷新(***flush***)，也有可能不会，因此InnoDB不能继续做后台I/O操作。

在MySQL 5.6及更高版本中，语法`FLUSH TABLES ... FOR EXPORT`为`InnoDB`表往磁盘写一些数据，确保易于通过拷贝数据来备份那些表。

参见 [backup], [flush], [InnoDB], [shutdown].

## <a name="R"></a>R ##
### <a name="glos_raid"></a>RAID: 磁盘阵列
“廉价冗余磁盘阵列(Redundant Array of Inexpensive Drives)”的首字母缩写。通过在多个磁盘上分散I/O操作在硬件层获得更大的并发，并且改善低层写操作，否则它们将以顺序执行。

参见 [concurrency].

### <a name="glos_random_dive"></a>random dive: 随机取样
一种用来快速估计一列中不同值个数(列的基数，***cardinality***)的技术。InnoDB从索引中随机取样页，并且使用这些数据来估算不同值的个数据。这个操作在每张表首词打开时发生。

起初，取样的页数固定为8；现在，此值取决于设置[innodb_stats_sample_pages]参数。

如何随机取页的方法取决于设置innodb_use_legacy_cardinality_algorithm参数。默认设置(OFF)比老版本拥有更优的随机性。

参见 [cardinality].

### <a name="glos_raw_backup"></a>raw backup: 原始备份
在二进制日志(***binary log***)与任何增量备份(***incremental backup***)中的变更被应用之前，MySQL企业备份(***MySQL Enterprise Backup***)产品生成的初始的备份文件集。在这个阶段，文件尚未为恢复(***restore***)做好准备。当这些变更被应用后，文件就叫一致性备份(***prepared backup***)。

参见 [binary log], [hot backup], [ibbackup_logfile], [incremental backup], [MySQL Enterprise Backup], [prepared backup], [restore].

### <a name="glos_read_committed"></a>READ COMMITTED: 隔离级别，不译 
为了性能，使用放宽事务(***transaction***)之间部分保护的锁(***locking***)策略的一种隔离级别(***isolation level***)。事务不能看到其它事务未提交的数据，但他们可以看到当前事务之后启动的另一个事务所提交的数据。所以，事务从来看不到任何错误数据，但数据能不能看到，一定程度上取决于其它事务的时间。

在这个隔离级别下，当一个事务执行`UPDATE ... WHERE`或`DELETE ... WHERE`操作，其它事务可能不得不等待。事务可以执行`SELECT ... FOR UPDATE`和不会造成其它事务等待的`LOCK IN SHARE MODE`操作。

参见 [ACID], [isolation level], [locking], [REPEATABLE READ], [SERIALIZABLE], [transaction].

### <a name="glos_read_uncommitted"></a>READ UNCOMMITTED: 隔离级别，不译
提供事务之间最小量保护的隔离级别(***isolation level***)。查询使用的锁(***locking***)策略使它们能够在通常会等待另一个事务的情况下继续。尽管如此，额外的性能是用不可靠结果的代价换来的，包括其它其它更正了但尚未提交的数据(被称为脏读，***dirty read***)。使用这个隔离级别要格外小心，要注意结果集可能会不一致或不能重现，取决于同一时刻其它事务在做什么。一般来说，这个隔离级别下的事务只做查询，没有插入. 更新或删除操作。

参见 [ACID], [dirty read], [isolation level], [locking], [transaction].

### <a name="glos_read_view"></a>read view: 读视图
InnoDB的***MVCC***机制所使用的一个内部快照。取决于其隔离级别(***isolation***)，某些事务(***transaction***)可以看到那些在事务(某些情况下是语句)启动时刻可以看到的数据值。使用读视图的隔离级别有***REPEATABLE READ***. ***READ COMMITTED***和***READ UNCOMMITTED***。

参见 [isolation level], [MVCC], [READ COMMITTED], [READ UNCOMMITTED], [REPEATABLE READ], [transaction].

### <a name="glos_read_ahead"></a>read-ahead: 预读
异步提前获取一组页(***pages***)(一整个簇，***extend***)到***buffer pool***中的一种I/O请求，在预期中这些页很快就被用到。线性预读技术基于上一个区中对页访问的模式，提前获取区中的所有页，并且这是自MySQL 5.1 InnoDB Plugin始的所有MySQL版本的一部分。随机预读技术在同一个区中有一定数量的页存在于buffer pool的情况下，将提前获取该区中的所有页。随机预读不是MySQL 5.5的一部分，但在MySQL 5.6中由配置选项[innodb_random_read_ahead]重新引入。

参见 [buffer pool], [extent], [page].

### <a name="glos_read_only_transaction"></a>read-only transaction: 只读事务
一类事务，可以通过排除一些涉及为每个事务(***transaction***)创建一个读视图(***read view***)的簿记来达到为InnoDB表的优化。只能执行无锁读(***non-locking read***)的查询。它可以明确地用使用语法s`TART TRANSACTION READ ONLY`来启动，或在某些条件下自动完成。更多细节参考[第14.2.12.2.3，优化只读事务][14.02.12.02.03]。

参考 [non-locking read], [read view], [transaction].

### <a name="glos_record_lock"></a>record lock: 索引记录锁
一个索引记录上的锁(***lock***)。例如，`SELECT C1 FROM UPDATE FROM T WHERE C1=10;` 阻止其它事务的插入. 更新或删除那些`tc.1`是10的行。与之对应的是间隙锁(***gap lock***)和行记录锁(***next-key lock***)。

参见 [gap lock], [lock], [next-key lock].

### <a name="glos_redo"></a>redo: 重做，不译
当***DML***语句对InnoDB表产生变更时记录在redo日志(***redo log***)中的以记录为单位的数据。它在崩溃恢复(***crash recovery***)中用于校正于不完整的事务(***transaction***)写入的数据。单调递增的***LSN***值代表通过redo日志的redo数据的积累量。

参见 [crash recovery], [DML], [LSN], [redo log], [transaction].

### <a name="glos_redo_log"></a>redo log: 重做日志，不译
崩溃恢复(***crash recovery***)过程中使用一种基于磁盘的数据结构，用于校正由不完整事务(***transaction***)写入的数据。在正常操作过程中，它将变更InnoDB表数据的请求编码，这些请求由SQL语句或低层的API调用NoSQL接口产生。在异常关机(***shutdown***)之前完有完成更新数据文件(***data files***)的修改会被自动重放。

redo log在物理上表现为一组文件，通常命名为`ib_logfile0`和`iblogfile1`。redo日志中的数据根据受影响的记录编码；这些数据统称为***redo***。redo日志中通过的数据表现为单调递增的***LSN***值。在MySQL 5.6.3中，之前redo日志大小4GB的上限升至512G。

redo log在磁盘上的布局取决于配置选项[innodb_log_file_size]. [innodb_log_group_home_dir]及[innodb_log_files_in_group](基本不用)。redo日志操作的性能也受日志缓冲的影响，由配置选项[innodb_log_buffer_size]控制。

参见 [crash recovery], [data files], [ib_logfile], [log buffer], [LSN], [redo], [shutdown], [transaction].

### <a name="glos_redundant_row_format"></a>redundant row format: 冗余行格式
最早的InnoDB行格式，对于使用Antelope文件格式的表有效。在MySQL 5.0.3之前，它是InnoDB中唯一有效的行格式。在MySQL 5.0.3及更高版本中，默认为精简行格式。你仍然可以指定冗余行格式以兼容较老的InnoDB表。

如需更多关于InnoDB冗余行格式的信息，请参考[第14.2.9.4节，精简与冗余行格式][14.02.09.04]。

参见 [Antelope], [compact row format], [file format], [row format].

### <a name="glos_referential_integrity"></a>referential integrity: 参照完整性 
维护数据一直处于一致格式的技术，***ACID***理念的一部分。实际上，不同表中的数据通过使用外键约束(***FOREIGN KEY constraint***)来保持一致，它能阻止变更发生或自动像变更传递到关联的表中。关联机制包括阻止即将误插入重复值的唯一约束(***unique constraint***)和阻止即将误插入空白值的非空约束(***NOT NULL constraint***)。

参见 [ACID], [FOREIGN KEY constraint], [NOT NULL constraint], [unique constraint].

### <a name="glos_relational"></a>relational: 关系
现代数据库系统很重要的一部分。数据库服务编码并强制实施关系，如一对一. 一对多和唯一性。例如，一个人在一个地址本数据库中可能拥有零个. 一个或多个手机号；单个电话号码可能与多个家庭成员关联。在财务数据库中，一个人可能要求刚好拥有一个纳税人ID，并且任何纳税人ID只能与一个人关联。

数据库服务可以利用这些关系来阻止错误数据被插入，并且找到高效查询信息的方法。例如，如果一个值被定义为唯一，那么服务可以在找到第一个匹配项之后就停止搜索，并且他可以拒绝试图插入相同值的第二份拷贝。

在数据库层面，这些关系通过SQL特性来表示，诸如表中的列(***column***). 唯一约束. 非空约束(***NOT NULL constarnts***). 外键(***foreign key***)及不同类型的关联操作等。复杂的关系一般会引用数据分拆到多个表中。通常，数据是范式化(***normalized***)的，所以一对多关系中的重复的值只被存储一次。

在数学语境中，数据库中的关系起源于集合论。比如，`WHERE`子句中的`OR`和`AND`操作表现为并集和交集的概念。

参见 [ACID], [constraint], [foreign key], [normalized].

### <a name="glos_relevance"></a>relevance: 相关度
在全文搜索(***full-text search***)特性中，一个表示搜索字符串与全文索引(***FULLTEXT index***)中数据相似度的数字。例如，当你搜索一个单词时，该词出现多次的行相比只出现一次的行，单词与它的相关性要更大一些。

参见 [full-text search], [FULLTEXT index].

### <a name="glos_repeatable_read"></a>REPEATABLE READ: 隔离级别，不译
InnoDB默认的隔离级别(***isolation level***)。它阻止查询任何正在被其它事务修改的行，从而阻断了非重复读(***non-repeatable read***)但不能阻断幻(***phantom***)读。它使用了一个适度严格的锁(***locking***)策略，所以所有在同一个事务中的查询能从同一个快照上读到数据，也就是说，数据跟事务启动时一样的。

当一个事务在这个隔离级别下执行`UPDATE ... WHERE`. `DELETE ... WHERE`. `SELECT ... FOR UPDATE`和`LOCK IN SHARE MODE`操作时，其它事务可能需要等待。

参见 [ACID], [consistent read], [isolation level], [locking], [phantom], [SERIALIZABLE], [transaction].

### <a name="glos_replication"></a>replication: 复制
从主库(***master database***)发送变更到一个或多个从库(***slave database***)的做法，这样所有的数据库拥有相同的数据。这个技术有着广泛的应用，如为更好的扩展性而做的负载均衡. 容备以及测试软件升级与配置变更。变更在数据库之间发送的方法有基于行的复制(***row-based replication***)与基于语句的复制(***statement-based replication***)。

参见 [row-based replication], [statement-based replication].

### <a name="glos_restore"></a>restore: 恢复
将一组文件从MySQL企业备份产品(***MySQL Enterprise Backup***)中放置到MySQL中的进程。执行这个操作可以修改损坏了的数据库. 返回到早期某个时间点或设置一个新的从库(在复制(***replication***)环境下)。在MySQL企业备份产品(***MySQL Enterprise Backup***)中，这个操作由mysqlbackup命令(***mysqlbackup command***)的`copy-back`选项来执行。

参见 [hot backup], [MySQL Enterprise Backup], [mysqlbackup command], [prepared backup], [replication].

### <a name="glos_rollback"></a>rollback: 回滚
一个结束一个事务(***transaction***)，撤消任何由该事务生成的变更的***SQL***语句。它与提交相对(***commit***)，提交是让该事务产生的变更保持持久。

默认情况下，MySQL使用自动提交(***autocommit***)设置，它在每条SQL语句之后自动执行提交。如果你要使用回滚技术的话，必须要变更这个设置。

参见 [ACID], [commit], [transaction].

### <a name="glos_rollback_segment"></a>rollback segment: 回滚段
包含undo日志(***undo log***)的存储区，是系统表空间(***system tablespace***)的一部分。

参见 [system tablespace], [undo log].

### <a name="glos_row"></a>row: 行
有一组列(***column***)定义的逻辑数据结构。一组行组成一张表(***table***)，在InnoDB数据文件(***data files***)中，每个页可以包含一行或多行。

尽管InnoDB为了与MySQL语法保持一致而使用了术语行格式(***row format***)，但行格式是每张表的一个属性并且应用到了表中的所有行上。

参见 [column], [data files], [page], [row format], [table].

### <a name="glos_row_format"></a>row format: 行格式
InnoDB表(***table***)中行(***row***)的磁盘存储格式。当InnoDB有了如压缩等新的功能时，新的行格式会被引进，以支持存储在效率与性能方面的改善。

每一张表都有自己的行格式，通过`ROW_FORMAT`选项来指定。要查看每张InnoDB表的行格式，执行命令`SHOW TABLE STATUS`。因为系统表空间中的所有表使用同一种行格式，所以要利用其它行格式的优势的话，一般要求打开[innodb_file_per_table]选项，以便每张表都存储在独立的表空间中。

参见 [compact row format], [compressed row format], [dynamic row format], [fixed row format], [redundant row format], [row], [table].

### <a name="glos_row_lock"></a>row lock: 行锁
一种锁(***lock***)，阻止一行被别一个事务(***transaction***)以互斥的方式访问。同一个表中的其它行则可以被其它事务自由的写入。这是在***InnoDB***表上做***DML***操作产生的一类锁(***locking***)。

与之对应的是MyISAM对应的表级锁(***table lock***)，或***DDL***操作期间的用在不能做在线DDL(***online DDL***)操作的InnoDB表上的锁；这些锁阻止对表的并发访问。

参见 [DDL], [DML], [InnoDB], [lock], [locking], [online DDL], [table lock], [transaction].

### <a name="glos_row_based_replication"></a>row-based replication: 行复制
一种复制(***replication***)的形式，其中事件从主库(***master***)传播到从库(***slave***)上，并说明独立的行如何发生变更。它对于[innodb_autoinc_lock_mode]选项的所有设置都是安全的。

参见 [auto-increment locking], [innodb_autoinc_lock_mode], [master server], [replication], [slave server], [statement-based replication].

### <a name="glos_row_level_locking"></a>row-level locking: 行级锁
***InnoDB***表使用的锁(***locking***)机制，依靠行锁(***row lock***)而非表锁(***table lock***)。多个事务(***transaction***)可以同时修改同一张表。只有当两个事务试图修改同一行数据时让其中一个事务等待其它事务完成(并且释放它的行锁)。

参见 [InnoDB], [locking], [row lock], [table lock], [transaction].

### <a name="glos_rw_lock"></a>rw-lock: 读写锁
InnoDB低级对象，用来表示和强制对内部内存结构体共享访问锁(***lock***)。一旦这个锁被获取了，任何其它的进程和线程等等能读到数据结构，但是没有一个可以写它。与之对应的是互斥锁(***mutex***)，它强制排它访问。互斥锁和读写锁统称为闩锁(***latch***)。

参见 [latch], [lock], [mutex], [Performance Schema].

## <a name="S"></a>S ##

### <a name="glos_savepoint"></a>savepoint: 保存点
保存点有助于实现嵌套事务(***transaction***)。它们常用来提供在表上操作的范围，该表是大事务的一部分。例如，在预订系统中安排一个旅行可能会涉及到预订几个不同的航班；如果一个中意的航班不可用，你可以只回滚(***rollback***)预订中涉及单程的变更，而不必将之前成功预约的航班都回滚。

参见 [rollback], [transaction].

### <a name="glos_scalability"></a>scalability: 可扩展性
往一个系统中增加更多工作，以及处理更多并发请求的能力，并在突破系统容量上限期间并无性能的突然下降。软件架构. 硬件配置. 应用编码以及负载类型都在可扩展性中扮演重要角色。当系统到达最大容量，提高可扩展性的流行的做法是垂直扩展(***scale up***，提升已有软硬件的能力)和水平扩展(***scale out***，增加新的服务器和更多MySQL实例)。常常与可用性(***availability***)搭配作为一个大规模部署中的关键组成部分。

参见 [availability], [scale out], [scale up].

### <a name="glos_scale_out"></a>scale out: 水平扩展 
通过增加新服务器和更多MySQL实例来提高可扩展性(***scalability***)的技术。例如，架设复制. MySQL集群. 连接池或其它通过一组机器来扩展工作能力的方面。与之对应的是垂直扩展(***scale up***)。

参见 [scalability], [scale up].

### <a name="glos_scale_up"></a>scale up: 垂直扩展
通过提升已有软硬件能力来提高可扩展性(***scalability***)的技术。例如，给一台服务器增加内存并调整与内存有关的参数，如[innodb_buffer_pool_size]和[innodb_buffer_pool_instances]。与之对应的是水平扩展(***scale out***)。

参见 [scalability], [scale out].

### <a name="glos_schema"></a>schema: 数据库(仅MySQL)
从概念上讲，schema指的是一组相互之间有关联的数据库对象，如表. 表列. 列的数据类型. 索引. 外键等等。这些对象通过SQL语法连在一起，因为这些列组成表，外键指向表和列等。理想情况下，它们在逻辑上也是连在一起的，做为统一的应用或灵活的框架的一部分来一起工作。例如，information_schema和performance_schema数据库在它们的名字中使用"schema"来强化它们所包含表与列之间的亲近关系。

在MySQL中，从物理上讲，一个schema等同于一个数据库。你可以在MySQL语法中，将关键字DATABASE用SCHEMA替代，例如，用CREATE SCHEMA来替代CREATE DATABASE。

一些其它的数据库产品会有区别。例如，在Oracle数据库产品中，schema只代表一部分数据库：属于一个单个用户的表和其它对象。

参见 [database], [ib-file set], [INFORMATION_SCHEMA], [Performance Schema].

### <a name="glos_search_index"></a>search index: 搜索索引
在MySQL中，全文搜索(***full-text search***)查询使用一种特殊的索引，全文索引(***FULLTEXT index***)。在MySQL 5.6.4及以上版本中，InnoDB和MyISAM表都支持全文索引了；在这之前，这些索引只在MyISAM表中可用。

参见 [full-text search], [FULLTEXT index].

### <a name="glos_secondary_index"></a>secondary index: 二级索引
相当于表列的子集的一类InnoDB索引(***index***)。一个InnoDB表可以拥有0个. 一个或多个二级索引。(与之对应的是聚集索引，***clustered index***，每个InnoDB都要用有这个索引，并且存储了表中所有的列。)

一个二级索引可以用来满足只从索引列中请求数据的查询。对于更加复杂的查询，它可以用来找到表中有关的行，这些行之后会通过查询聚集索引来获取。

创建和删除二级索引通常会因为拷贝所有InnoDB表的数据而带来的明显的性能负载。InnoDB Plugin的快速索引创建(***fast index creation***)特性会加速针对二级索引的`CREATE INDEX`和`DROP INDEX`语句。

参见 [clustered index], [Fast Index Creation], [index].

### <a name="glos_segment"></a>segment: 段
InnoDB表空间(***tablespace***)中主要组织结构。如果表空间像是一个目录的话，段就像是目录里的文件。段会增长，新段会被创建。

例如，在***file-per-table***的表空间中，表数据在一个段中，每个相关的索引在自己的段中。系统表空间(***system tablespace***)包含多个不同的段，因为它要保存多个表和它们相关的索引。系统表空间也包括最多由128个回滚段(***rollback segments***)组成的undo日志(***undo log***)。

段会随着数据的插入与删除会增大与缩小。当一个段需要更多空间，它会一次扩展一个簇(***extent***，1MB)。类似地，当某个簇中的数据不再需要时，段会释放掉这个簇中可利用的空间。

参见 [extent], [file-per-table], [rollback segment], [system tablespace], [tablespace], [undo log].

### <a name="glos_selectivity"></a>selectivity: 选择性
数据分布的一个属性，一个列中不同值的数(基数，***cardinality***)除以表中的记录数。高选择性意味着列中的值相对唯一，且可以高效地通过索引来获取数据。在你(或查询优化器)可以预测到一个尝试在WHERE子句只能匹配少量(或部分)表中的行的情况下，如果首先使用索引评估这个尝试，整个查询(***query***)往往是高效的。

参见 [cardinality], [query].

### <a name="glos_semi_consistent_read"></a>semi-consistent read: 半一致性读
`UPDATE`语句使用的一类读操作，是提交读(***read committed***)和一致性读(***consistent read***)的组合体。当一个`UPDATE`语句检查一个已经被锁了的行时，InnoDB返回给MySQL最近提交的版本以便MySQL可以判断此行是否满足`UPDATE`的`WHERE`条件。如果行匹配(必须要被更新)，MySQL重读该行，并且这次InnoDB会锁住它或等待为它上锁。这类读操作只有在事务在读提交隔离级别(***isolation level***)时发生，或在[innodb_locks_unsafe_for_binlog]选项开启时发生。

参见 [consistent read], [isolation level], [READ COMMITTED].

### <a name="glos_serializable"></a>SERIALIZABLE: 隔离级别，不译
使用最保守锁机制的隔离级别(***isolation level***)，阻止任何其它的事务插入或变更本事务读取的数据，直到它结束。这种情况下，同一个查询可以在一个事务里一遍又一遍地运行，并且每次都能确保读到相同的结果集。任何对被当前事务启动之后的事务所提交数据的变更尝试，都会导致当前事务的等待。

这是SQL标准指定的默认隔离级别。实际上，这么严格的级别是很少需要的，所以InnoDB的默认隔离级别是次严格的，可重复读(***repeatable read***)。

参迎 [ACID], [consistent read], [isolation level], [locking], [REPEATABLE READ], [transaction].

### <a name="glos_server"></a>server: 服务(器)
持续运行的一程序，等待接收并处理另一个程序(客户端，***client***)发来的请求。因为一整台计算机常常专门用于运行一个或多个服务(数据数据库服务. web服务. 应用服务或它们的组合)，所以这个术语***server***也用来指运行这个服务软件的计算机。

参见 [client], [mysqld].

### <a name="glos_shared_lock"></a>shared lock: 共享锁
一种锁(***lock***)，允许其它事务(***transaction***)读取锁定了的对象，也可以在它之上再加共享锁，但不能写它。与它相反的是排它锁(***exclusive lock***)。

参见 [exclusive lock], [lock], [transaction].

### <a name="glos_shared_tablespace"></a>shared tablespace: 共享表空间
同系统表空间(***system tablespace***)。

参见 [system tablespace]。

### <a name="glos_sharp_checkpoint"></a>sharp checkpoint: 清晰检查点
将所有buffer pool中的redo实体包含在redo日志(***redo log***)的某个地方的脏页(***dirty page***)全部刷新(***flush***)到磁盘的进程。发生在InnoDB重用一个log文件的一部分之前；log日志沿环性使用。通常发生在写敏感的工作负载下(***workload***)。

参见 [dirty page], [flush], [redo log], [workload].

### <a name="glos_shutdown"></a>shutdown: 关闭
停止MySQL服务的进程。默认情况下，这个进程对InnoDB表做清扫操作，所以它可以缓慢关闭，但是之后会很快启动。如果你略过了清扫操作，它很快关闭但在下次重启时必须做清扫工作。

快速关闭模式由[innodb_fast_shutdown]选项控制。

参见 [fast shutdown], [InnoDB], [slow shutdown], [startup].

### <a name="glos_slave_server"></a>slave server: 从服务器
常常简写为“slave”。复制(***replication***)环境下的一个数据库服务器(***server***)，从另一台服务器上接收变更并应用那些同样的变更。所以它维护着与主库(***master***)一样的数据，虽然它有一些延后。

在MySQL，从服务器常常通过替换崩溃了的主服务器来做灾难恢复。它们也常常用来做软件升级和新设置的测试，来确保数据库的配置变更不会给性能或可靠性带来问题。

从服务器通常有高的负载，因为它要处理所有的从主库同步过来的***DML***(写)操作和用户的查询。为了确保从服务器可以足够快速地应用从主库而来的变更，它们常常使用快速的I/O设备和足够的CPU和内存来运行同一台从服务器上的多个数据库实例。例如，主服务器可能使用机械硬盘，而从服务器使用固态硬盘(***SSD***)。

参见 [DML], [replication], [server], [SSD].

### <a name="glos_slow_query_log"></a>slow query log: 慢查询日志
一类用来针对MySQL服务处理过的SQL语句进行性能调优的日志(***log***)。日志信息存储在一个文件中。你可以启用这个特性来使用它。你控制记录哪种类型的“慢”SQL语句。如需更多信息，参考[第5.2.5节，慢查询日志][05.02.05]。

参见 [general query log], [log].

### <a name="glos_slow_shutdown"></a>slow shutdown: 慢关闭
在关闭操作之前还要做额外的InnoDB刷新操作的一类关闭(***shutdown***)。也叫***clean shutdown***。由配置参数``innodb_fast_shutdown=0``或命令`SET GLOBAL innodb_fast_shutdown=0`来指定；虽然关闭本身要花更长时间，但它却节省下来的是下次启动的时间。

参见 [clean shutdown], [fast shutdown], [shutdown].

### <a name="glos_snapshot"></a>snapshot: 快照
数据在一个具体时间点的表示，即使数据被其它事务(***transaction***)的变更提交(***commit***)了，它也保持着相同的数据。在某些隔离级别(***isolation level***)中用来做一致性读(***consitent read***)。

参见 [commit], [consistent read], [isolation level], [transaction].

### <a name="glos_space_id"></a>space ID: 表空间ID
MySQL实例中用来标志`InnoDB`表空间(***tablespace***)唯一标识。对于系统表空间(***system tablespace***)来说，表空间ID一直为0；系统表空间中所有的表都使用同一个ID。在[file-pre-table]模式下创建的每个表空间文件也拥有自己的空间ID。

在MySQL 5.6之前，硬编码的值使得在MySQL实例之间移动表空间变得困难重重。自MySQL 5.6始，你可以使用包含`FLUSH TABLES FOR EXPORT`，`ALTER TABLE ... DISCARD`和`ALTER TABLE ... IMPORT TABLESPACE`语句的可传输表空间(***transportable tablespace***)特性，在实例间拷贝表空间文件。需要调整的表空间ID的信息通过你与表空间一起拷贝的.cfg文件(***.cfg file***)传达。如果更多信息，参考[第14.2.5.5节，往另一台服务拷贝表空间(可传输表空间)]。

参见 [.cfg file][cfg file], [file-per-table], [.ibd file][ibd file], [system tablespace], [tablespace], [transportable tablespace].

### <a name="glos_spin"></a>spin: 自旋
持续尝试一个资源是否可用的一种等待。这种技术用在那些通常只在短时间内被持有的资源上，这种情况下在一个“繁忙的循环”下等待要比把一个线程推到休眠状态并执行一个上下文切换要高效得多。如果资源在短时间内没有变为有效，自旋循环终止，另一种等待技术上阵。

参考 [latch], [lock], [mutex], [wait].

### <a name="glos_sql"></a>SQL: 结构化查询语言
结构化查询语言是标准执行数据库操作的语言。常常分类为***DDL***. ***DML***和查询(***query***)。MySQL包含一些附加的语句类型，如复制(***replication***)。SQL语法基础参考[第9章，语言结构][9]，MySQL表的列所使用的数据类型参考[第11章，数据类型][11]，查询中所用到的标准的和MySQL特有的函数参考[第12章，函数与操作符][12]。

参见 [DDL], [DML], [query], [replication].

### <a name="glos_ssd"></a>SSD: 固态驱动器
固态驱动器(solid-state drive)的缩写。与传统硬盘驱动器(***HDD***)有着不同的性能特性的一类存储设备：更小的存储容量、更快的随机写、无移动部件以及大量为写性能所做的考虑。它的性能特性会对磁盘受限(***disk-bound***)的系统产生影响。

参见 [disk-bound], [HDD].

### <a name="glos_startup"></a>startup: 启动
启动MySQL服务的过程。一般由列在[第4.3节，MySQL服务和服务启动程序][04.03.00]中列出的程序来完成。与之对应为关机(***shutdown***)。

参见 [shutdown].

### <a name="glos_statement_based_replication"></a>statement-based replication: 语句复制 
一种复制(***replication***)的形式，其中语句从主库(***master server***)发出，在从库(***slave server***)上重放。为了避免由自增锁(***auto-increment locking***)带来潜在时间问题，在使用选项[innodb_autoinc_lock_mode]时要多加小心。

参见 [auto-increment locking], [innodb_autoinc_lock_mode], [master server], [replication], [row-based replication], [slave server].

### <a name="glos_statistics"></a>statistics: 统计信息
与每个`InnoDB`表(***table***)和索引(***index***)有关的评估值，用来构建一个高效的查询执行计划(***query execution plan***)。主要的值是基数(不重复的值数，***cardinality***)和表的行数或索引实体数。表的统计信息体现了它们主键索(***primary key***)引中的数据。二级索引(***secondary key***)的统计信息体现了索引覆盖的行。

因为时时刻刻不同的事务(***transaction***)都可以插入或删除表中的数据，所以这些值是评估的而不是准确的。为了避免这些值被频繁地重算，你可以启用持久统计(***presistent statistics***)，其中的值存在`InnoDB`的系统表中，而且只有当你执行`ANALYZE TABLE`语句时才会刷新。

你可以通过[innodb_stats_method]配置选项来控制在计算统计信息时如何处理NULL值。

针对数据库对象与数据库活动的其它类型的统计信息可以在***INFORMATION_SCHEMA***表和***PERFORMANCE_SCHEMA***表中找到。

参见 [cardinality], [index], [INFORMATION_SCHEMA], [NULL], [Performance Schema], [persistent statistics], [primary key], [query execution plan], [secondary index], [table], [transaction].

### <a name="glos_stemming"></a>stemming: 词干
针对一个常见词根的不同形式的搜索能力，比如单复数、过去时、将来时和将来时。目前MyISAM全文检索(***full-text search***)支持该特性，但InnoDB表的全文索引(***FULLTEXT index***)不支持。

参见 [full-text search], [FULLTEXT index].

### <a name="glos_stopword"></a>stopword: 停用词
在全文索引(***FULLTEXT index***)中，考虑到一个字太普通或太微不足道，所以它从搜索索引(***search index***)中被略过，并且在搜索查询中被忽略。针对不InnoDB表和MyISAM表，有不同的配置选项来控制对停用词的处理。更多细节请参考[第12.9.4节，全文停用词][12.09.04]。

参见 [FULLTEXT index], [search index].

### <a name="glos_storage_engine"></a>storage engine: 存储引擎
MySQL数据库的一个组件，用来执行低层的存储、更新与查询数据。在MySQL 5.5及更高版本中，***InnoDB***取代MyISAM，成为新表的默认存储引擎。不同的存储引擎都是为平衡各方面因素而设计，比如内存使用与磁盘使用、读可读与写速度以及速度与鲁棒性。每一种存储引擎管理指定的表，所以我们叫`InnoDB`表、`MyISAM`表等等。

MySQL企业备份针(***MySQL Enterprise Backup***)对InnoDB表的备份做了优化。它也可以备份MyISAM和其它引擎所处理的表。

参见 [InnoDB], [MySQL Enterprise Backup], [table type].

### <a name="glos_strict_mode"></a>strict mode: 严格模式
[innodb_strict_mode]选项的常用名。打开这个设置会导致在某些在正常情况下发出警告的场景，会被视为视为错误。例如，某些文件格式(***file format***)与行格式(***row format***)相关的选项的无效组合，正常情况下会产生一个报警，并且用默认值继续，而现在则会导致`CREATE TABLE`操作失败。

MySQL也有一些叫严格模式的东西。

参见 [file format], [innodb_strict_mode], [row format].

### <a name="glos_sublist"></a>sublist: 子列表
在表示buffer pool的列表结构体中，由不同的列表部分表示比如新的页和比较老的页。一组参数来控制这些部分的大小和新老页的分割点。

参见 [buffer pool], [eviction], [list], [LRU].

### <a name="glos_supremum_record"></a>supremum record: 上确界记录
一个索引中的伪造(***pseudo-record***)值，用来表示索引中最大值之上的间隙(***gap***)。如果一个事务有一个像`SELECT ... FOR UPDATE ... WHERE col >10`; 这样的语句，并且 这个列中的最大值是20，就会有一个在上确界记录上的锁来阻止其它事务插入像50、100等更大的值。

参见 [gap], [infimum record], [pseudo-record].

### <a name="glos_surrogate_key"></a>surrogate key: 代理键
人造键(***synthetic key***)的别称。

参见 [synthetic key].

### <a name="glos_synthetic_key"></a>synthetic key: 人造键
一个索引列，通常是主键，其中的值被随意分配。常常由一个自增列来完成。通过完全随意分配该值，你可以避免过于严格的规则和应用错误的假设。比如，如果批准一个员工雇用但从来这个员工实际没有加入过，表示员工号的数据序列可能会产生间隙。再比如，如果有人离开公司，后来又行话加入了，100号的员工的入职时间可能要比500号的员工要晚。数字值也会产生更短的可预计的值。例如，存储代表“马路”、“城市路”、“高速公路”等的代码值要比一遍又一遍地存储这些字串符来说，空间效率要更高一些。

也叫代理键(***surrogate key***)。相对应的是自然键(***natural key***)。

参见 [auto-increment], [natural key], [primary key], [surrogate key].

### <a name="glos_system_tablespace"></a>system tablespace: 系统表空间
一小集合包含InnoDB相关对象(数据字典，***data dictionary***)以及undo日志(***undo log***)、变更缓冲(***change buffer***)和双写缓冲(***doublewrite buffer***)存储区域的数据文件(即***ibdata files***)。根据[innodb_file_per_table]的选项，当表被创建时，它也可能包含部分或所有InnoDB表的数据和索引数据。系统表空间中的数据和元数据应用到MySQL实例(***instance***)中的所有数据库(***database***)中。

直到MySQL 5.6.7，默认情况是在系统表空间中保存所有InnoDB表和索引数据，常常导致这些文件变得非常大。因为系统表空间从不收缩，所以如果大量的临时数据被加载然后再被删除，就会出现存储空间问题。在MySQL 5.6.7以及更高版本中，默认就是file_per_table模式，其中每个表和它们关联的索引存储在一个独立的.ibd文件(***.ibd file***)中。新的默认值使得它更易于使用InnoDB依赖***Barracuda***文件格式的特性，如表压缩与动态(***DYNAMIC***)行格式。

在MySQL 5.6及更高版本中，为[innodb_undo_tablespace]选项设置一个值，会将undo日志(***undo log***)分裂到一个或多个独立的表空间文件中。这些文件也被认为是系统表空间的一部分。

保存所有表数据在系统表空间或独立的.ibd文件中一般会对存储管理带来影响。MySQL企业备份产品(***MySQL Enterprise Backup***)可能会备份一小组合的大文件，或很多更小的文件。在有上千表的系统中，文件系统处理上千的`.ibd`文件会引发瓶颈。

参见 [Barracuda], [change buffer], [compression], [data dictionary], [database], [doublewrite buffer], [dynamic row format], [file-per-table], [.ibd file][ibd file], [ibdata file], [innodb_file_per_table], [instance], [MySQL Enterprise Backup], [tablespace], [undo log].

## <a name="T"></a>T ##
### <a name="glos_trg_file"></a>.TRG file 
一个包含触发器参数的文件。该后缀名的文件一直包含在由MySQL企业备份(***MySQL Enterprise Backup***)产品的mysqlbackup命令(***mysqlbackup command***)生成的备份文件中。

参见 [MySQL Enterprise Backup], [mysqlbackup command], [.TRN file][TRN file].

### <a name="glos_trn_file"></a>.TRN file
一个包含触发器命名空间信息的文件。该后缀名的文件一直包含在由MySQL企业备份(***MySQL Enterprise Backup***)产品的mysqlbackup命令(***mysqlbackup command***)生成的备份文件中。

参见 [MySQL Enterprise Backup], [mysqlbackup command], [.TRG file][TRG file].

### <a name="glos_table"></a>table: 表
每一张MySQL表都与一种特定存储引擎(***storage engine***)相关联。***InnoDB***表有特定的物理(***physical***)与逻辑(***logcial***)特性，这些特性会影响性能、扩展性(***scalability***)、备份(***backup***)、管理和应用部署。

在文件存储术语中，如果表是在***file-per-table***模式下创建的，每一张InnoDB表既是单个大InnoDB系统表空间(***system tablespace***)的一部分，又是独立的`.ibd`文件的一部分。.ibd文件保存所有表和它的索引(***index***)的数据，也就是表空间(***tabelspace***)。

在file-per-table模式下创建的InnoDB表可以使用***Barracuda文***件格式。Barracuda表可以使用动态行格式(***DYNAMIC row format***)或压缩行格式(***COMPRESSED row format***)。这些对应的新设置启用了大量的InnoDB特性，比如压缩(***compression***)、快速索引创建(***fast index creation***)和溢出页列(***off-page columns***)。

为了向后兼容MySQL 5.1及更早版本，系统表空间中的InnoDB表必须使用***Antelope***文件格式，它支持精简行格式(***compact row format***)与冗余行格式(***redundant row format***)。

InnoDB的行(***row***)由叫聚集索引(***clustered index***)的的索引结构体组织起来，实体基于表的主键(***primary key***)列排序。在主键列上的过滤与排序的查询的数据访问是优化的，并且每个索引中包含每个实体对应的主键拷贝。更新主键列中的任何值都是一个开销很大的操作。因此InnoDB表设计的一个重要因素是将最重要查询的列选为主键，并保持主键短小，键值极少变更。

参见 [Antelope], [backup], [Barracuda], [clustered index], [compact row format], [compressed row format], [compression], [dynamic row format], [Fast Index Creation], [file-per-table], [.ibd file][ibd file], [index], [off-page column], [primary key], [redundant row format], [row], [system tablespace], [tablespace].

### <a name="glos_table_lock"></a>table lock: 表级锁
一个阻止其它事务(***transaction***)访问表的锁(***lock***)。InnoDB做了很大的努力，通过在线DDL(***online DDL***)、行锁(***row lock***)和针对处理***DML***语句和查询(***query***)的一致性读(***consistent read***)等技术，使得这种锁不再需要。你可以通过使用`LOCK TABLE`的SQL语句来创建一个这样的锁；从其它数据库系统和MySQL存储引擎迁移数据的步骤之一就是删除这样的语句，不管实不实用。

参见 [consistent read], [DML], [lock], [locking], [online DDL], [query], [row lock], [table], [transaction].

### <a name="glos_table_scan"></a>table scan: 全表扫描

参见 [full table scan].

### <a name="glos_table_statistics"></a>table statistics: 表统计

参见 [statistics].

### <a name="glos_table_statistics"></a>table type 表(引擎)类型
淘汰了的存储引擎的别称。我们用来指InnoDB表、MyISAM表等。

参见 [InnoDB], [storage engine].

### <a name="glos_tablespace"></a>tablespace: 表空间
一个可以保存一个或多个InnoDB表(***table***)和对应索引(***index***)数据的文件。系统表空间(***system tablespace***)包含构成数据字典(***data dictionary***)的表，在MySQL 5.6之前默认保存所有其它的InnoDB表。[innodb_file_per_table]选项在MySQL5.6及更高版本中默认为打开状态，打开这个选项允许所新建的表都拥有息的表空间，每个表一个独立的数据文件(***data file***)。

通过打开[innodb_file_per_table]选项来使用多个表空间，这对于使用像压缩和可传输表空间以及管理磁盘使用是必不可少的。参见[第14.2.5.2节，InnoDB File-Per-Table模式][14.02.05.02]。

由内置的InnoDB存储引擎创建的表空间向上兼容InnoDB Plugin。如果表空间使用***Antilope***文件格式，由InnoDB Plugin创建的表空间向下兼容内置的InnoDB存储引擎。 

MySQL集群也把它的表归组到表空间中，如需更多细节，参见[17.5.12.1节，MySQL集群数据对象][17.05.12.01]。

参见 [Antelope], [Barracuda], [compressed row format], [data dictionary], [data files], [file-per-table], [index], [innodb_file_per_table], [system tablespace], [table].

### <a name="glos_tablespace_dictionary"></a>tablespace dictionary: 表空间数据字典
InnoDB表空间中，一个表数据字典(***data dictionary***)元数据的体现。当表被打开后，该元数据可以通过.frm文件(***.frm file***)检查一致性，来诊断由过期的.frm文件引起的错误。该信息为在系统表空间(***system tablespace***)中的表而准备，也为因***file-per-table***选项而拥有它们自己.ibd文件(***.ibd file***)的表而准备。

参见 [data dictionary], [file-per-table], [.frm file][frm file], [.ibd file][ibd file], [system tablespace], [tablespace].

### <a name="glos_temporary_table"></a>temporary table: 临时表
一张表(***table***)，它的数据不需要做执久化。例如，临时表可能被作是复杂计算或变换中间结果的存储区域；这个中间数据可能不需要在崩溃后恢复。通过减少对数据写盘的严谨性与其它在重启时保护数据的措施，数据产品可以采取多种便捷来提高在临时表上操作的性能。

有时，数据自己会在一个设定的时候自动删除，比如在事务结束时或在会话结束时。在一些数据库产品中，表自己也会自动删除。

参见 [table].

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
### victim 牺牲(死锁检测，牺牲影响最少行的事物) 

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

[ACID]: #glos_acid
[.ARM file]: #glos_arm_file
[.ARZ file]: #glos_arz_file
[Antelope]: #glos_antelope
[B-tree]: #glos_b_tree
[Barracuda]: #glos_barracuda
[DCL]: #glos_dcl
[DDL]: #glos_ddl
[DML]: #glos_dml
[FOREIGN KEY constraint]: #glos_foreign_key_constraint
[FULLTEXT index]: #glos_fulltext_index
[Fast Index Creation]: #glos_fast_index_creation
[GA]: #glos_ga
[INFORMATION_SCHEMA]: #glos_information_schema
[InnoDB]: #glos_innodb
[LRU]: #glos_lru
[LSN]: #glos_lsn
[MVCC]: #glos_mvcc
[MYD file]: #glos_myd_file
[MYI file]: #glos_myi_file
[MySQL]: #glos_mysql
[MySQL Enterprise Backup]: #glos_mysql_enterprise_backup
[NOT NULL constraint]: #glos_not_null_constraint
[NULL]: #glos_null
[NoSQL]: #glos_nosql
[OLTP]: #glos_oltp
[Performance Schema]: #glos_performance_schema
[Pthreads]: #glos_pthreads
[READ]: #glos_read
[READ COMMITTED]: #glos_read_committed
[READ UNCOMMITTED]: #glos_read_uncommitted
[REPEATABLE]: #glos_repeatable
[REPEATABLE READ]: #glos_repeatable_read
[SERIALIZABLE]: #glos_serializable
[SQL]: #glos_sql
[SSD]: #glos_ssd
[TRG file]: #glos_trg_file
[TRN file]: #glos_trn_file
[XA]: #glos_xa
[adaptive hash index]: #glos_adaptive_hash_index
[apply]: #glos_apply
[asynchronous I/O]: #glos_asynchronous_io
[atomic]: #glos_atomic
[auto-increment]: #glos_auto_increment
[auto-increment locking]: #glos_auto_increment_locking
[autocommit]: #glos_autocommit
[availability]: #glos_availability
[backup]: #glos_backup
[beta]: #glos_beta
[binary log]: #glos_binary_log
[binlog]: #glos_binlog
[bottleneck]: #glos_bottleneck
[buffer]: #glos_buffer
[buffer pool]: #glos_buffer_pool
[buffer pool instance]: #glos_buffer_pool_instance
[built-in]: #glos_built_in
[cardinality]: #glos_cardinality
[cfg file]: #glos_cfg_file
[change buffer]: #glos_change_buffer
[change buffering]: #glos_change_buffering
[checkpoint]: #glos_checkpoint
[child table]: #glos_child_table
[clean page]: #glos_clean_page
[clean shutdown]: #glos_clean_shutdown
[client]: #glos_client
[clustered index]: #glos_clustered_index
[cold backup]: #glos_cold_backup
[column]: #glos_column
[column index]: #glos_column_index
[commit]: #glos_commit
[compact row format]: #glos_compact_row_format
[composite index]: #glos_composite_index
[compressed backup]: #glos_compressed_backup
[compressed row format]: #glos_compressed_row_format
[compression]: #glos_compression
[concurrency]: #glos_concurrency
[configuration file]: #glos_configuration_file
[consistent read]: #glos_consistent_read
[constraint]: #glos_constraint
[counter]: #glos_counter
[crash]: #glos_crash
[crash recovery]: #glos_crash_recovery
[cursor]: #glos_cursor
[data]: #glos_data
[data dictionary]: #glos_data_dictionary
[data directory]: #glos_data_directory
[data files]: #glos_data_files
[data warehouse]: #glos_data_warehouse
[database]: #glos_database
[deadlock]: #glos_deadlock
[deadlock detection]: #glos_deadlock_detection
[delete]: #glos_delete
[delete buffering]: #glos_delete_buffering
[denormalized]: #glos_denormalized
[dirty page]: #glos_dirty_page
[dirty read]: #glos_dirty_read
[disk-based]: #glos_sk_based
[disk-bound]: #glos_disk_bound
[doublewrite buffer]: #glos_doublewrite_buffer
[drop]: #glos_drop
[dynamic row]: #glos_dynamic_row
[dynamic row format]: #glos_dynamic_row_format
[early adopter]: #glos_early_adopter
[error log]: #glos_error_log
[eviction]: #glos_eviction
[exclusive lock]: #glos_exclusive_lock
[extent]: #glos_extent
[fast shutdown]: #glos_fast_shutdown
[file format]: #glos_file_format
[file-per-table]: #glos_file_per_table
[fixed]: #glos_fixed
[flush]: #glos_flush
[foreign key]: #glos_foreign_key
[frm file]: #glos_frm_file
[full backup]: #glos_full_backup
[full table scan]: #glos_full_table_scan
[full-text search]: #glos_full_text_search
[fuzzy checkpointing]: #glos_fuzzy_checkpointing
[gap]: #glos_gap
[gap lock]: #glos_gap_lock
[general query log]: #glos_general_query_log
[hash index]: #glos_hash_index
[high-water mark]: #glos_high_water_mark
[history list]: #glos_history_list
[hot backup]: #glos_hot_backup
[ib-file set]: #glos_ib_file_set
[ib_logfile]: #glos_ib_logfile
[ibbackup_logfile]: #glos_ibbackup_logfile
[ibd file]: #glos_ibd_file
[ibdata]: #glos_ibdata
[ibdata file]: #glos_ibdata_file
[ibtmp file]: #glos_ibtmp_file
[ibz file]: #glos_ibz_file
[ilist]: #glos_ilist
[implicit row lock]: #glos_implicit_row_lock
[in-memory database]: #glos_in_memory_database
[incremental backup]: #glos_incremental_backup
[index]: #glos_index
[index hint]: #glos_index_hint
[index prefix]: #glos_index_prefix
[infimum record]: #glos_infimum_record
[innodb_autoinc_lock_mode]: #glos_innodb_autoinc_lock_mode
[innodb_lock_wait_timeout]: #glos_innodb_lock_wait_timeout
[innodb_strict_mode]: #glos_innodb_strict_mode
[insert]: #glos_insert
[insert buffer]: #glos_insert_buffer
[insert buffering]: #glos_insert_buffering
[instance]: #glos_instance
[intention lock]: #glos_intention_lock
[isolation level]: #glos_isolation_level
[join]: #glos_join
[latch]: #glos_latch
[list]: #glos_list
[lock]: #glos_lock
[lock mode]: #glos_lock_mode
[locking]: #glos_locking
[locking read]: #glos_locking_read
[log]: #glos_log
[log buffer]: #glos_log_buffer
[log file]: #glos_log_file
[log group]: #glos_log_group
[logical]: #glos_logical
[logical backup]: #glos_logical_backup
[low-water mark]: #glos_low_water_mark
[master server]: #glos_master_server
[master thread]: #glos_master_thread
[memcached]: #glos_memcached
[metadata lock]: #glos_metadata_lock
[metrics counter]: #glos_metrics_counter
[midpoint insertion strategy]: #glos_midpoint_insertion_strategy
[mini-transaction]: #glos_mini_transaction
[mixed-mode insert]: #glos_mixed_mode_insert
[mutex]: #glos_mutex
[mycnf]: #glos_mycnf
[myini]: #glos_myini
[mysql]: #glos_mysql
[mysqlbackup command]: #glos_mysqlbackup_command
[mysqld]: #glos_mysqld
[mysqldump]: #glos_mysqldump
[natural key]: #glos_natural_key
[neighbor page]: #glos_neighbor_page
[next-key lock]: #glos_next_key_lock
[non-blocking I/O]: #glos_non_blocking_io
[non-locking read]: #glos_non_locking_read
[non-repeatable read]: #glos_non_repeatable_read
[normalized]: #glos_normalized
[off-page column]: #glos_off_page_column
[online]: #glos_online
[online DDL]: #glos_online_ddl
[optimistic]: #glos_optimistic
[optimizer]: #glos_optimizer
[option]: #glos_option
[option file]: #glos_option_file
[overflow page]: #glos_overflow_page
[page]: #glos_page
[page cleaner]: #glos_page_cleaner
[page size]: #glos_page_size
[parent]: #glos_parent
[parent table]: #glos_parent_table
[partial backup]: #glos_partial_backup
[persistent statistics]: #glos_persistent_statistics
[pessimistic]: #glos_pessimistic
[phantom]: #glos_phantom
[physical]: #glos_physical
[physical backup]: #glos_physical_backup
[plan stability]: #glos_plan_stability
[plugin]: #glos_plugin
[point-in-time recovery]: #glos_point_in_time_recovery
[prepared]: #glos_prepared
[prepared backup]: #glos_prepared_backup
[primary key]: #glos_primary_key
[process]: #glos_process
[pseudo-record]: #glos_pseudo_record
[purge]: #glos_purge
[purge buffering]: #glos_purge_buffering
[purge lag]: #glos_purge_lag
[query]: #glos_query
[query execution plan]: #glos_query_execution_plan
[raw]: #glos_raw
[raw backup]: #glos_raw_backup
[read view]: #glos_read_view
[read-ahead]: #glos_read_ahead
[read-only]: #glos_read_only
[read-only transaction]: #glos_read_only_transaction
[record lock]: #glos_record_lock
[redo]: #glos_redo
[redo log]: #glos_redo_log
[redundant row format]: #glos_redundant_row_format
[referential integrity]: #glos_referential_integrity
[relational]: #glos_relational
[replication]: #glos_replication
[restore]: #glos_restore
[rollback]: #glos_rollback
[rollback segment]: #glos_rollback_segment
[row]: #glos_row
[row format]: #glos_row_format
[row lock]: #glos_row_lock
[row-based replication]: #glos_row_based_replication
[rw-lock]: #glos_rw_lock
[scalability]: #glos_scalability
[scale out]: #glos_scale_out
[scale up]: #glos_scale_up
[schema]: #glos_schema
[search index]: #glos_search_index
[secondary index]: #glos_secondary_index
[server]: #glos_server
[shared lock]: #glos_shared_lock
[shutdown]: #glos_shutdown
[slave server]: #glos_slave_server
[slow]: #glos_slow
[slow shutdown]: #glos_slow_shutdown
[space ID]: #glos_space_id
[spin]: #glos_spin
[startup]: #glos_startup
[statement-based replication]: #glos_statement_based_replication
[stopword]: #glos_stopword
[storage engine]: #glos_storage_engine
[strict mode]: #glos_strict_mode
[sublist]: #glos_sublist
[supremum]: #glos_supremum
[supremum record]: #glos_supremum_record
[surrogate key]: #glos_surrogate_key
[synthetic key]: #glos_synthetic_key
[system]: #glos_system
[system tablespace]: #glos_system_tablespace
[table]: #glos_table
[table lock]: #glos_table_lock
[table type]: #glos_table_type
[tablespace]: #glos_tablespace
[temporary tablespace]: #glos_temporary_tablespace
[thread]: #glos_thread
[transaction]: #glos_transaction
[transportable tablespace]: #glos_transportable_tablespace
[truncate]: #glos_truncate
[two-phase commit]: #glos_two_phase_commit
[undo]: #glos_undo
[undo log]: #glos_undo_log
[unique]: #glos_unique
[unique constraint]: #glos_unique_constraint
[unique index]: #glos_unique_index
[unique key]: #glos_unique_key
[victim]: #glos_victim
[wait]: #glos_wait
[warm backup]: #glos_warm_backup
[warm up]: #glos_warm_up
[workload]: #glos_workload


[04.02.03.03]: ./Chapter_04/04.02.03_Specifying_Program_Options.md#04.02.03.03
[05.02.02]: ./Chapter_05/05.02.02_The_Error_Log.md
[05.02.03]: ./Chapter_05/05.02.03_The_General_Query_Log.md
[05.02.04]: ./Chapter_05/05.02.04_The_Binary_Log.md
[14.02.02.04]: ./Chpater_14/14.02.02_InnoDB_Concepts_and_Architecture.md#14.02.02.04
[14.02.02.10]: ./Chpater_14/14.02.02_InnoDB_Concepts_and_Architecture.md#14.02.02.10
[14.02.02.11]: ./Chpater_14/14.02.02_InnoDB_Concepts_and_Architecture.md#14.02.02.11
[14.02.08]: ./Chapter_14/14.02.08_InnoDB_Compressed_Tables.md
[14.02.09]: ./Chapter_14/14.02.09_InnoDB_Integration_with_memcached.md
[16.01.04.04]: ./Chapter_16/16.01.04_Replication_and_Binary_Logging_Options_and_Variables.md#16.01.04.04
[binlog_checksum]: ./Chapter_16/16.01.04_Replication_And_Binary_Logging_Options_And_Variables.md#sysvar_binlog_checksum 
[innochecksum]: ./Chapter_04/04.06.01_Innochecksum_Offline_InnoDB_File_Checksum_Utility.md
[innodb_adaptive_hash_index]: ./Chpater_14/14.02.06_InnoDB_Startup_Options_and_System_Variables.md#sysvar_innodb_adaptive_hash_index
[innodb_change_buffer_max_size]: ./Chapter_14/14.02.14_InnoDB_Startup_Options_and_System_Variables.md#sysvar_innodb_change_buffer_max_size
[innodb_change_buffering]: ./Chpater_14/14.02.06_InnoDB_Startup_Options_and_System_Variables.md##sysvar_innodb_change_buffering
[innodb_checksum]: ./Chapter_14/14.02.14_InnoDB_Startup_Options_and_System_Variables.md#sysvar_innodb_checksum
[innodb_file_format]: ./Chpater_14/14.02.06_InnoDB_Startup_Options_and_System_Variables.md#sysvar_innodb_file_format
[master_verify_checksum]: ./Chapter_16/16.01.04_Replication_And_Binary_Logging_Options_And_Variables.md#sysvar_master_verify_checksum: 
[SHOW ENGINE INNODB STATUS]: ./Chapter_15/13.07.05_SHOW_Syntax.md#13.07.05.16
[slave_sql_verify_checksum]: ./Chapter_16/16.01.04_Replication_And_Binary_Logging_Options_And_Variables.md#sysvar_slave_sql_verify_checksum