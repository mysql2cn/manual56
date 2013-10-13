## E.09.00_插件式认证的约束
 
 第一节描述了可插入式认证框架的一些通用性限制，可参考[Section 6.3.7, “Pluggable Authentication”。](./06.03.07_Pluggable_Authentication.md)第二节描述了第三方的插入式认证框架对于MySQL认证带来的好处以及如何变得兼容性更好。
 
 “(MySQL原生认证)native authentication”是指使用存储在`mysql.user`表中的`Password`列的密码进行用户验证的方法，即使使用了可插入式认证方式后，也是MySQL默认的认证方法。“(Windows原生认证)Windows native authentication”是指的使用已登录Windows平台的用户使用的凭证。
 
### 一般认证约束限制 
 
* Connector/C, Connector/C++:  这些连接器只能通过native authentication进行
  
    例外情况：若以上的连接器能够动态将验证模块链接至`libmysqlclient`(或者源代码编译)，则可以支持其加载的验证方法。
 
* Connector/J: 客户端帐户验证只能使用native authentication进行验证。
 
* Connector/Net: 在Connector/Net 6.4.4 以前，客户端帐户验证只能使用native authentication进行验证。对于6.4.4，客户端还能使用Windows native authentication进行帐户验证。
 
* Connector/ODBC: 在Connector/ODBC 3.51.29 and 5.1.9 以前，客户端帐户验证只能使用native authentication进行验证。对于3.51.29 and 5.1.9, 客户端使用二进制发行版本还能够使用Windows native authentication或者PAM进行帐户验证。(能够进行这样灵活的验证，是因为`libmysqlclient`中的Connector/ODBC 二进制文件是通过在MySQL 5.5.16中支持Windows或PAM认证的文件来生成的)
 
* Connector/PHP: 客户端使用MySQL native driver 编译时(mysqlnd)帐户验证只能使用native authentication进行验证。

* MySQL Proxy: MySQL Proxy 0.8.2以前，客户端帐户验证只能使用native authentication进行验证，对于0.8.2，客户端还可以通过插入式PAM进行帐户验证，对于0.8.3，客户端又添加了Windows native authentication进行帐户验证。 
 
* MySQL Enterprise Backup: MySQL Enterprise Backup 在3.6.1版本时，只支持使用native authentication进行验证，对于3.6.1， 已经支持了nonnative authentication。

* Windows native authentication:  使用Windows plugin要求帐户为域帐户，若无域帐户，则使用NTLM进行验证，且客户端和服务器只能位于同一台机器上。 
 
* Proxy users: Proxy user 支持插件(plugin)认证 （插件可能返回一个用户，此用户并非连接的用户），例如： native authentication 不支持 Proxy User，但 PAM和Windows plugins 支持。
 
* 复制中的限制: MySQL 5.6.4以前, 从库服务器只能够通过native authentication 连接主服务器，对于5.6.4，默认客户端插件(`libmysqlclient`)还支持nonnative authentication用户认证，从库服务器便可以支持 nonnative authentication进行用户认证，否则需要设置从服务器 slave plugin_dir 系统变量，将插件文件放在slave plugin_dir[538]所处位置。
 
* FEDERATED tables:一个 FEDERATED table 访问远程表只能通过native authentication进行帐户验证。
 
 
### 插件式认证和第三方连接器
 
第三方连接器开发使用人员可能遵循以下步骤去准备和检查连接器的扩展和更好的兼容性
 
 * 当前的连接器无须做任何改动便可以使用native authentication进行帐户验证，但是，读者最好在最新的版本上进行测试，确保没有问题。
 
    例外：连接器默认情况下，会使用当前版本的libmysqlclient去进行插入式认证。默认情况下动态链接至libmysqlclient，无须任何改动，且连接正常。
 
 * 为增强插件式安全功能，一个连接器可链接至最新的libmysqlclient，从而支持客户端内置的验证方式（如明文的PAM验证和Windows native authentication)。同时让连接器支持MySQL MySQL plugin directory（一般位于本地服务器的plugin_dir[538]系统变量中)。
 
    连接器若动态链接至`libmysqlclient`，要保证`libmysqlclient`安装在客户端上，且连接器进行用户认证时，要加载`libmysqlclient`。

* 让连接器支持给定的认证方式，还可以采取直接使用client/server 协议， Connector/Net 使用这种方法来支持 Windows native authentication.
 
* 若客户端连接器未从默认插件位置进行相应加载，则客户端必须有命令行或系统变量的功能获得文件位置，标准的MySQL客户端mysql and mysqladmin 使用--plugin-dir 选项，也可参考 [Section 22.8.14, “C API Client Plugin Functions”](./22.08.04_Building_and_Running_C_API_Client_Programs.md)  
 
* Proxy user 用户连接器在第一节中已经描述过，连接器的认证方法取决于Proxy user所支持的认证方法
 
