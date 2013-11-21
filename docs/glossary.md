# MySQL专业词汇表 #

这些术语在MySQL数据库服务器中经常被用到。此词汇表源于InnoDB存储引擎的专业术语手册，并且主要的释义都是InnoDB相关的。

## <a name="A"></a>A ##
### <a name='glos_acid' /></a>ACID: ACID 
原子性(atomicity)、 一致性(consistency)、隔离性(isolation)和持久性(durability)的首字母缩写。这些属性是一个数据库系统全部具备的，并且与事务(***transaction***)的概念紧紧绑在一起。InnoDB的事务特性遵守ACID原则。

事务是可以提交或回滚的原子(***atomic***)工作单元。当一个事务造成数据库的多处更改，所有的更改要么在事务提交(***committed***)后全部成功，要么在事务回滚(***rolled back***)后全部撤消。

数据库在任何时候都处于一致的状态——在每一次提交或回滚后，以及事务在进行中时。如果相关的数据正在被跨表更新，查询看到的是所有的旧值或所有的新值，而不会是新旧兼有的。

当事务在进行时它们之间是被保护(被隔离)的；它们之间不能互相干涉或看到其它事务未提交的数据。这种隔离是靠锁(***locking***)机制实现的。有经验的用户可以调整隔离级别(***isoloation level***)，当他们可以确认事务真的不会相互干涉时，牺牲少许保护换取性能和并发(***concurrency***)的提升。

事务的结果是持久的：一旦提交操作成功了，在掉电、系统崩溃、资源竞争或其它非数据库应用所引起的潜在危险等情况下，事务引起的更改是安全的。持久性通常需要写到磁盘存储上，具有一定冗余量来防止在写操作过程中的掉电故障或软件崩溃。(在InnodDB中，双写缓冲(***doublewrite buffer***)来帮助完成一致性。)

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

 一个函数或程序集合。一个API为函数、程序、参数和返回值提供一组稳定名字与类型。

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

对MySQL、操作系统或硬件故障及因为维护行为而引起宕机等主机故障的处理能力，以及在必要情况下从上述所有故障中恢复的能力。经常与扩展性(`scalability`)配合使用，成为大规模部署中的一个关键因素。

参见 [scalability].

## <a name='B'></a>B ##

### <a name='glos_b_tree'></a>B-tree: B树

数据库索引上很流行使用的树形数据结构。该数据结构一直保持排序状态，保证快速精确查找(等于操作)和范围查找(比如大于、小于和BETWEEN操作)。这种类型的索引在绝大多数的存储引擎中是可用的，如InnoDB和MyISAM。

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

热备(***hot backup***)、温备(***warm backup***)和冷备(c***old backup***)因它们干涉数据库操作的多少而有很大不同。(热备最少干涉，冷备最多。)

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

一个用来做临时存储的内存或磁盘空间。数据被缓存在内存中，以便更高效地写磁盘(使用少而大的I/O操作代替多而小)。数据缓存在磁盘上以获得更高的可靠性，这样即使在极端情况下发生崩溃或其它故障发生时也可以恢复。InnoDB主要的缓冲类型就是***buffer pool***、***doublewrite buffer***和***insert buffer***。
参见 [buffer pool], [crash], [doublewrite buffer], [insert buffer].

### <a name='glos_buffer_pool' /></a>buffer pool: 缓冲池 (或不译)

保持缓存了的InnoDB表和索引的内存区域。为了获得高容量的读操作的效率，buffer pool被分为页页(***page***)以持有多行。为了获得更高缓存管理的效率，buffer pool实现为一个页面链接；很少使用的数据利用***LRU***算法的变体从将其老化并从缓存中剔出。在大内存的系统中，你可以通过将buffer pool分割为多个buffer pool实例(***buffer pool instance***)来提高并发。

好几种`InnoDB`的状态变量、`information_schema`表及`performance_schema`表都能帮助你监测buffer pool的内部工况。自MySQL 5.6始，你还可以在通过诸如`innodb_buffer_pool_dump_at_shutdown`和`innodb_buffer_pool_load_at_startup`的InnoDB的配置变量，在启动和关闭服务时导出或恢复buffer bool中的内容，也可以在任何时间手工操作。

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

例如，一个员工离职可能会触发一系列人力资源部门的行为。人力资源数据库也可能具备能描述一个已受雇但尚未开始工作的员工数据的灵活性。在一个在线服务中关闭一个账户可能会导致数据从数据库中删除，或数据被移走或被标志以便以后在该账户重新启用时恢复。一个公司可能要制定政策除了要考虑如工资不能为负数等合理性检查之外，还要考虑工资的最大值、最小值及如何调整等。一个零售业数据库可能不允许相同序列号被返回一次以上的采购，或当、不允许信用卡购买超过某个金额，而一个用来检测欺诈行为的数据库则允许这些行为。

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

一个记录二级索引(***secondary indexes***)中页(***pages***)上变化的特殊的数据结构。这些值可能是用SQL中的`INSERT`、`UPDATE`或`DELETE`语句(***DML***)引起的。这些特性加上变更缓冲区叫做变更缓冲，由插入缓冲(***insert buffer***)、删除缓冲(***delete buffer***)和清除缓冲(***purge buffer***)组成。

当不在buffer pool中的二级索引中的相关页发生时，变更只被记录在变更缓冲区中。当相关的索引页被加载到buffer pool中且关联的变更还在变更缓冲区中时，这些page的变更会利用变更缓冲区中的数据应用到buffer pool(***merged***)中。在系统几近空闲或在缓慢关机时，清除(***purge***)操作会周期性地执行，将新的索引页写到硬盘上。清除操作可以将一个序列的索引值一起写到硬盘块中，这样做比将每一个值立即写到硬盘上要更有效。

从物理角度看，变更缓冲区是系统表空间(***system tablespace***)中的一部分，所以在数据库重启过程中索引的变更是被保持缓冲的。变量只有在页面因为其它读操作而被加载到buffer pool中时才会被应用(***merged***)。

存储在变更缓冲区中的数据的数量与类型由[innodb_change_buffering]和[innodb_change_buffer_max_size]配置选项来决定。要观察关于当前变更缓冲区中的数据，可以执行[SHOW ENGINE INNODB STATUS]命令。

以前叫插入变更区(***insert buffer***)。

参见 [buffer pool], [change buffering], [delete buffering], [DML], [insert buffer], [insert buffering], [merge], [page], [purge], [purge buffering], [secondary index], [system tablespace].

### <a name='glos_change_buffering'></a>change buffering: 变更缓冲

有关变更缓冲区(***change buffer***)功能的总称，由插入缓冲(***insert buffering***、删除缓冲(***delete buffering***)和清除缓冲(***purge buffering***)构成。索引变更是由SQL语句引起，通常会带来随机I/O操作，变更会被“憋住”并用后台线程(***thread***)来周期性地执行。这种顺序操作可以将一个序列的索引值一起写到硬盘块中，这样做比将每一个值立即写到硬盘上要更有效。由[innodb_change_buffering]和[innodb_change_buffer_max_size]配置选项控制。

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

### client 客户端

发送请求到服务器，并解释或处理结果的一种程序类型。客户端软件只能运行一段时间(如邮件或聊天软件)，可能以交互方式运行(如`mysql`命令处理器)。

参见 [mysql], [server].

### clustered index 聚集索引

InnoDB主键(***primary key***)索引术语。InnoDB表存储是基于主键列中的值来组织的，用来加速涉及主键列的查询与排序。为了得到最优性能，请基于最关键性能的查询谨慎选择主键列。因为修改聚集索引是一个非常昂贵操作，请选择很少或从来不被修改的列为主键列。

在Orcale的数据库产品中，这种表的类型被称为索引组织的表(***index-organized table***)。

参见 [index], [primary key], [secondary index].

### cold backup 冷备份
### column 列
### column index 单列索引
### column prefix 列的前缀
### commit 提交
### compact row format 紧凑(compact)的行格式
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
### CRUD (不译)
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
### <a name="GA"/>GA 一般可用(建议直接用 GA)
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
### my.cnf 配置文件(Unix/Linux)
### my.ini 配置文件(Windows)
### .MYD file .MYD文件
### .MYI file .MYI文件
### mysql mysql(客户端)
### MySQL Enterprise Backup MySQL企业备份
### mysqlbackup command mysqlbackup命令
### mysqld MySQL daemon(Unix)或MySQL service(Windows)
### mysqldump mysqldump命令

## N ##
### natural key 自然主键
### neighbor page 相邻页
### next-key lock 行间隙锁
### non-blocking I/O 同AIO
### non-locking read 不加锁读
### non-repeatable read 非重复读
### normalized (符合)范式的
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
### page cleaner 页清理器(页清理线程)
### page size 数据页大小
### .PAR file .PAR文件
### parent table 父表
### partial backup 部分备份
### partial index 部分索引
### Performace Schema 性能库
### persistent statistic 持久统计
### pessimistic 悲观锁
### phantom 幻(读)
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
### schema 数据库(仅MySQL)
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
### spin 自旋(锁) 
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
### table type 表(引擎)类型
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
[disk-based]: #glos_disk_based
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

[14.02.09]: ../Chapter_14/14.02.09_InnoDB_Integration_with_memcached.md
[innodb_adaptive_hash_index]: ../Chpater_14/14.02.06_InnoDB_Startup_Options_and_System_Variables.md#sysvar_innodb_adaptive_hash_index
[innodb_file_format]: ../Chpater_14/14.02.06_InnoDB_Startup_Options_and_System_Variables.md#sysvar_innodb_file_format
[05.02.04]: ./05.02.04_The_Binary_Log.md
[16.01.04.04]: ../Chapter_16/16.01.04_Replication_and_Binary_Logging_Options_and_Variables.md#16.01.04.04
[innodb_change_buffering]: ../Chpater_14/14.02.06_InnoDB_Startup_Options_and_System_Variables.md##sysvar_innodb_change_buffering
[innodb_change_buffer_max_size]: ../Chapter_14/14.02.14_InnoDB_Startup_Options_and_System_Variables.md#sysvar_innodb_change_buffer_max_size
[SHOW ENGINE INNODB STATUS]: ../Chapter_15/13.07.05_SHOW_Syntax.md#13.07.05.16
[innodb_checksum]: ../Chapter_14/14.02.14_InnoDB_Startup_Options_and_System_Variables.md#sysvar_innodb_checksum
[innochecksum]: ../Chapter_04/04.06.01_Innochecksum_Offline_InnoDB_File_Checksum_Utility.md
[binlog_checksum]: ../Chapter_16/16.01.04_Replication_And_Binary_Logging_Options_And_Variables.md#sysvar_binlog_checksum 
[master_verify_checksum]: ./Chapter_16/16.01.04_Replication_And_Binary_Logging_Options_And_Variables.md#sysvar_master_verify_checksum: 
[slave_sql_verify_checksum]: ./Chapter_16/16.01.04_Replication_And_Binary_Logging_Options_And_Variables.md#sysvar_slave_sql_verify_checksum