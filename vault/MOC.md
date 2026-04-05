---
title: Map of Content
updated: 2026-04-04
---

# 🗺️ Map of Content

*最后更新: 2026-04-04*

## 基础概念

- [[虚拟内存]] — 地址空间抽象、隔离与保护
- [[页表机制]] — 虚拟地址到物理地址的翻译
- [[多级页表]] — 页表的层次化结构，减少内存开销
- [[分页与分段对比]] — 两种内存管理方式的区别
- [[x86 内存模型与 TLB]] — 硬件层面的内存管理
- [[x86 实模式与保护模式]] — x86 模式切换
- [[gdt-与段描述符]] — 全局描述符表
- [[x86 特权级]] — Ring 0-3 的保护机制
- [[x86 调用约定 cdecl]] — 函数调用 ABI
- [[栈帧结构]] — 函数调用时的栈布局

## 汇编 — 寄存器与标志

- [[x86-寄存器概述]] — 寄存器分类总览
- [[x86-通用寄存器详解]] — EAX/EBX/ECX/EDX/ESI/EDI/EBP/ESP
- [[段寄存器]] — CS/DS/SS/ES/FS/GS
- [[标志寄存器-eflags]] — CF/ZF/SF/OF/PF 等标志位
- [[控制寄存器-cr0-cr4]] — 分页、保护模式控制
- [[调试寄存器]] — DR0-DR7 硬件断点

## 汇编 — 指令集

- [[x86-指令编码格式]] — Prefix→Opcode→ModR/M→SIB→Disp→Imm
- [[内存寻址模式]] — 立即/寄存器/直接/间接/SIB 寻址
- [[数据传输指令-mov]] — MOV/MOVZX/MOVSX/LEA/XCHG
- [[栈操作-push-pop]] — PUSH/POP/PUSHAD/PUSHFD
- [[算术运算指令]] — ADD/SUB/MUL/DIV/INC/DEC
- [[逻辑运算指令]] — AND/OR/XOR/NOT/TEST
- [[移位与循环指令]] — SHL/SHR/SAR/ROL/ROR
- [[比较与测试指令]] — CMP/TEST 标志位变化
- [[条件跳转指令]] — JE/JNE/JG/JL/JA/JB
- [[无条件跳转与调用-jmp-call]] — JMP/CALL/RET
- [[字符串操作指令]] — MOVSB/CMPSB/SCASB + REP
- [[循环指令-loop]] — LOOP/LOOPE/LOOPNE/JECXZ
- [[条件设置指令-setcc]] — SETZ/SETG/SETL 系列
- [[条件传送-cmovcc]] — CMOVcc 消除分支
- [[中断与异常指令]] — INT/INT3/IRET/BOUND
- [[系统调用指令-syscall]] — INT 0x80/SYSENTER/SYSCALL
- [[原子操作指令]] — XCHG/LOCK/CMPXCHG/XADD
- [[内存屏障指令]] — SFENCE/LFENCE/MFENCE
- [[CPUID 指令]] — CPU 特性检测

## 汇编 — SIMD 与浮点

- [[SIMD 概念]] — 单指令多数据并行
- [[SSE 指令集]] — XMM 128 位 SIMD
- [[AVX 指令集]] — YMM 256 位 SIMD、AVX-512
- [[x87-浮点指令-fpu]] — ST 寄存器栈、浮点运算
- [[浮点数表示与运算]] — IEEE 754 格式

## 汇编 — 工具链与语法

- [[gas-汇编语法]] — AT&T 语法详解
- [[nasm-汇编语法]] — Intel 语法详解
- [[at-t-与-intel-语法对比]] — 两种语法的差异
- [[内联汇编]] — GCC 扩展内联、约束符号
- [[汇编程序结构]] — .text/.data/.bss 段
- [[汇编与链接过程]] — 汇编器/链接器流程
- [[重定位与符号解析]] — ELF 重定位、PLT/GOT

## 汇编 — 高级主题

- [[保护模式基础]] — GDT、段描述符、门描述符
- [[长模式-x86-64]] — 64 位扩展、RIP 相对寻址
- [[缓存与缓存行]] — 缓存层次、伪共享
- [[汇编优化技巧]] — CMOV、循环展开、SIMD、寄存器分配

## 设计模式 — 概述与原则

- [[设计模式-概述]] — GoF 23 种、SOLID 原则

## 设计模式 — 创建型

- [[设计模式-单例模式]] — Meyers' Singleton、call_once
- [[设计模式-工厂方法模式]] — 简单工厂/工厂方法/注册表
- [[设计模式-抽象工厂模式]] — 跨平台 UI 工厂
- [[设计模式-建造者模式]] — Fluent API、Director + Builder
- [[设计模式-原型模式]] — clone()、原型注册表
- [[设计模式-创建型模式对比]] — 五种模式决策指南

## 设计模式 — 结构型

- [[设计模式-适配器模式]] — 类/对象适配器、STL 适配器
- [[设计模式-桥接模式]] — 抽象与实现分离、Pimpl
- [[设计模式-组合模式]] — 树形结构、透明/安全模式
- [[设计模式-装饰器模式]] — 动态职责添加、std::ostream
- [[设计模式-外观模式]] — 统一高层接口
- [[设计模式-享元模式]] — 共享细粒度对象
- [[设计模式-代理模式]] — 虚代理、保护代理、智能引用

## 设计模式 — 行为型

- [[设计模式-责任链模式]] — 请求沿链传递
- [[设计模式-命令模式]] — 请求封装、撤销/重做
- [[设计模式-解释器模式]] — 语法表示与解释
- [[设计模式-迭代器模式]] — STL 迭代器、range-based for
- [[设计模式-中介者模式]] — 封装对象间交互
- [[设计模式-备忘录模式]] — 状态捕获与恢复
- [[设计模式-观察者模式]] — 信号槽、事件系统
- [[设计模式-状态模式]] — 状态机、TCP 连接
- [[设计模式-策略模式]] — 算法族、std::function
- [[设计模式-模板方法模式]] — NVI、CRTP 编译时替代
- [[设计模式-访问者模式]] — double dispatch、std::variant+visit

## C++ 惯用法与模式

- [[cpp-raii-惯用法]] — 资源获取即初始化
- [[cpp-pimpl-惯用法]] — 编译防火墙
- [[cpp-crtp-奇异递归模板模式]] — 编译时多态
- [[cpp-类型擦除]] — std::function 原理
- [[cpp-策略设计]] — 模板参数策略、Concepts 约束
- [[cpp-nvi-非虚接口]] — 公有非虚 + 私有虚函数
- [[cpp-sfinae-与编译期多态]] — enable_if、type_traits
- [[cpp-标签分发]] — integral_constant、重载决议
- [[cpp-scope-guard]] — 作用域退出清理
- [[cpp-移动语义]] — 右值引用、完美转发、5/3/0 法则
- [[cpp-智能指针详解]] — unique_ptr/shared_ptr/weak_ptr
- [[cpp-对象池模式]] — 内存池、Arena 分配器
- [[cpp-表达式模板]] — 延迟求值、Eigen 核心
- [[cpp-函数式编程模式]] — Lambda、Ranges、函数组合
- [[设计模式-cpp-选型指南]] — 运行时 vs 编译时多态选型

## 算法 — 基础

- [[算法-时间复杂度与空间复杂度]] — Big-O、主定理、摊还分析
- [[算法-递归与分治]] — 递归三要素、分治范式
- [[算法-双指针]] — 快慢指针、对撞指针
- [[算法-滑动窗口]] — 固定/变长窗口模板
- [[算法-前缀和]] — 一维/二维前缀和、差分数组
- [[算法-位运算技巧]] — 位操作、子集枚举

## 算法 — 排序与查找

- [[算法-排序算法比较]] — 9 种排序全面对比
- [[算法-快速排序]] — Partition、随机化 pivot
- [[算法-归并排序]] — 分治合并、外部排序
- [[算法-堆排序]] — heapify、原地排序
- [[算法-冒泡排序与插入排序]] — 简单排序、希尔排序
- [[算法-二分查找]] — 左/右边界、旋转数组

## 算法 — 数据结构

- [[算法-哈希表]] — 冲突解决、负载因子
- [[算法-链表]] — 反转、快慢指针、判环
- [[算法-栈与队列]] — LIFO/FIFO、单调栈/队列
- [[算法-二叉树]] — 遍历、深度、直径
- [[算法-二叉搜索树]] — BST 性质、插入删除
- [[算法-avl-树]] — 自平衡、四种旋转
- [[算法-红黑树]] — 着色规则、工程应用
- [[算法-b-树与-b-树]] — 多路搜索树、数据库索引
- [[算法-堆与优先队列]] — 二叉堆、Top-K
- [[算法-trie-字典树]] — 前缀树、自动补全
- [[算法-线段树]] — 区间查询、懒惰传播
- [[算法-树状数组-bit]] — lowbit、区间和
- [[算法-并查集]] — union/find、路径压缩

## 算法 — 图论

- [[算法-图的表示]] — 邻接矩阵/表/边列表
- [[算法-图的遍历-bfs-dfs]] — BFS/DFS、连通分量
- [[算法-最短路径-dijkstra]] — 贪心、堆优化
- [[算法-最短路径-bellman-ford]] — 负权边、负权环检测
- [[算法-最小生成树]] — Prim/Kruskal
- [[算法-拓扑排序]] — Kahn 算法、DFS 后序

## 算法 — 高级策略

- [[算法-动态规划基础]] — 最优子结构、状态转移
- [[算法-背包问题]] — 0-1/完全背包
- [[算法-最长公共子序列-lcs]] — DP 填表
- [[算法-最长递增子序列-lis]] — DP + 贪心二分
- [[算法-贪心算法]] — 局部最优、霍夫曼编码
- [[算法-回溯法]] — 搜索树、剪枝
- [[算法-字符串匹配-kmp]] — 前缀函数、线性匹配
- [[算法-单调栈与单调队列]] — 柱状图、接雨水
- [[算法-概率与随机算法]] — 蓄水池抽样、布隆过滤器

## xv6 内核

- [[xv6 启动流程]] — 从 bootloader 到第一个进程
- [[xv6 进程管理]] — 进程状态机与调度
- [[xv6 exec 详解]] — 系统调用 exec 的实现
- [[xv6 ELF 与进程加载]] — ELF 格式和进程加载流程
- [[xv6 内存分配]] — kalloc/kfree 物理页管理
- [[xv6 内核栈]] — 每个进程的内核栈
- [[xv6 系统调用]] — syscall 接口
- [[xv6 中断与陷阱]] — trap 处理机制
- [[xv6 调度器实现]] — Round-Robin 调度
- [[xv6 锁与同步]] — 自旋锁与睡眠锁
- [[xv6 睡眠与唤醒]] — sleep/wakeup 机制
- [[xv6 文件系统]] — 文件系统层次结构
- [[xv6 文件描述符]] — fd 三层结构与 I/O 抽象
- [[xv6 缓冲区缓存]] — 磁盘块缓存
- [[xv6 日志系统]] — crash recovery
- [[xv6 磁盘驱动]] — IDE 磁盘 I/O
- [[xv6 管道]] — 管道通信
- [[xv6 shell 工作原理]] — shell 的管道和重定向
- [[cow-写时复制]] — fork 优化

## 同步与并发

- [[信号量]] — P/V 操作与经典同步问题
- [[死锁]] — 四个必要条件与处理策略
- [[原子指令与内存屏障]] — CAS、LL/SC、内存序
- [[无锁数据结构]] — CAS-based 并发数据结构
- [[调度算法比较]] — RR、优先级、MLFQ、CFS
- [[上下文切换]] — swtch.S 的实现
- [[信号机制]] — Unix 信号处理
- [[xv6 睡眠与唤醒]] — 等待队列机制

## 硬件与中断

- [[idt-与中断机制]] — 中断描述符表
- [[中断向量与-apic]] — 中断路由
- [[lapic-与-ioapic]] — 本地和 I/O APIC
- [[内存映射 I/O]] — MMIO 访问设备寄存器
- [[DMA 与总线架构]] — 直接内存访问
- [[设备驱动模型]] — 设备抽象
- [[多处理器启动]] — AP 启动流程
- [[汇编与 C 混合编程]] — inline asm

## 其他

- [[elf-文件格式]] — ELF 规范
- [[x86 系统调用演进]] — int 80h → syscall
- [[系统调用实现]] — 系统调用的通用框架

---

## C++ — 语言基础

- [[cpp-基本数据类型]] — 类型体系、sizeof、整数提升
- [[cpp-const与constexpr]] — const 正确性、constexpr、consteval
- [[cpp-引用与指针]] — 左值引用、右值引用、转发引用
- [[cpp-类型转换]] — static_cast、dynamic_cast、const_cast、reinterpret_cast
- [[cpp-auto与类型推导]] — auto 推导规则、decltype、尾置返回类型
- [[cpp-lambda表达式]] — 捕获、泛型 lambda、递归 lambda
- [[cpp-枚举类型]] — enum class vs enum、位标志枚举
- [[cpp-结构化绑定]] — C++17 多返回值解包
- [[cpp-命名空间]] — 嵌套命名空间、匿名命名空间、内联命名空间
- [[cpp-sizeof与内存对齐]] — 对齐规则、padding、alignas
- [[cpp-编译模型与ODR]] — 编译过程、声明 vs 定义、单一定义规则
- [[cpp-堆与栈内存]] — 栈分配 vs 堆分配、性能对比
- [[cpp-string深入]] — SSO、string_view、常用操作
- [[cpp-string_view注意事项]] — 生命周期陷阱、安全用法
- [[cpp-字符串字面量与原始字符串]] — 前缀、R"()"、自定义后缀
- [[cpp-函数重载与默认参数]] — 重载决议、const 重载
- [[cpp-异常处理]] — try-catch、异常安全级别、noexcept
- [[cpp-预处理器]] — 宏、条件编译、include guard
- [[cpp-位运算深入]] — 位操作技巧、bitset、popcount
- [[cpp-与C互操作]] — extern "C"、POD 类型接口
- [[cpp-常见陷阱与反模式]] — 最常见错误、vector<bool>、map::operator[]

## C++ — 面向对象

- [[cpp-类与对象]] — 特殊成员函数、初始化列表、Rule of Five
- [[cpp-继承与多态]] — 虚函数、vtable、override/final
- [[cpp-运算符重载]] — 成员 vs 非成员、比较运算符、流运算符
- [[cpp-多重继承与虚继承]] — 菱形问题、虚基类
- [[cpp-RTTI与typeid]] — 运行时类型识别、type_info
- [[cpp-友元与静态成员]] — friend、static 成员函数
- [[cpp-转换构造函数与转换运算符]] — explicit、隐式转换
- [[cpp-this指针与成员指针]] — this、成员指针、deducing this
- [[cpp-union与匿名联合]] — C union、C++11 改进
- [[cpp-引用限定成员函数]] — & 与 && 限定、右值成员函数
- [[cpp-Rule-of-Zero与Rule-of-Five]] — 特殊成员函数管理
- [[cpp-深拷贝与浅拷贝]] — 拷贝语义、值语义 vs 指针语义
- [[cpp-EBO与no_unique_address]] — 空基类优化、空类不占空间
- [[cpp-设计模式选型]] — 运行时 vs 编译时多态选型

## C++ — 模板与泛型

- [[cpp-模板编程基础]] — 函数模板、类模板、特化、SFINAE
- [[cpp-可变参数模板]] — 参数包、展开、完美转发
- [[cpp-concepts]] — C++20 概念约束、requires 表达式
- [[cpp-模板模板参数]] — 模板作为模板参数
- [[cpp-折叠表达式]] — C++17 四种折叠形式
- [[cpp-if-constexpr]] — 编译期分支、替代 SFINAE
- [[cpp-type-traits]] — 类型检查、类型变换、void_t
- [[cpp-sfinae与编译期多态]] — enable_if、SFINAE 原理
- [[cpp-标签分发]] — 编译期函数选择
- [[cpp-编译期计算与constexpr深入]] — constexpr 演进、consteval、constinit
- [[cpp-模板元编程]] — 编译期计算、类型计算
- [[cpp-别名模板与using]] — using vs typedef、模板别名
- [[cpp-CTAD类模板参数推导]] — 类模板参数自动推导
- [[cpp-编译期字符串哈希]] — FNV-1a、switch on string
- [[cpp-CRTP应用场景汇总]] — 静态多态、Mixin、计数器

## C++ — 标准库（STL 容器）

- [[cpp-vector深入]] — 扩容策略、迭代器失效、emplace_back
- [[cpp-string深入]] — SSO、string_view、常用操作
- [[cpp-map与set]] — 红黑树、有序遍历、范围查询
- [[cpp-unordered-map]] — 哈希表、自定义哈希、桶管理
- [[cpp-unordered容器的哈希与桶]] — 哈希函数质量、rehash、负载因子
- [[cpp-deque与list]] — 分段连续内存、双向链表
- [[cpp-栈队列与优先队列]] — 容器适配器、最大/最小堆
- [[cpp-array与std-array]] — 固定大小数组、零开销
- [[cpp-emplace操作]] — 原地构造、完美转发
- [[cpp-容器选择指南]] — 决策流程、性能特性对比
- [[cpp-迭代器失效规则汇总]] — 各容器的失效规则
- [[cpp-flat-map与flat-set]] — C++23 基于有序 vector 的关联容器
- [[cpp-mdspan]] — C++23 多维数组视图

## C++ — 标准库（STL 算法与迭代器）

- [[cpp-stl算法总览]] — 查找、排序、变换、归约、集合操作
- [[cpp-迭代器类别与适配器]] — 迭代器五种类别、反向/插入/移动迭代器
- [[cpp-数值算法与归约]] — accumulate、reduce、transform_reduce、前缀和
- [[cpp-并行算法]] — C++17 execution policy、par、par_unseq
- [[cpp-lambda在STL算法中的应用]] — 排序谓词、查找条件、聚合

## C++ — 智能指针与内存管理

- [[cpp-智能指针详解]] — unique_ptr、shared_ptr、weak_ptr（已有）
- [[cpp-智能指针对比与最佳实践]] — 选择指南、参数传递
- [[cpp-new与delete深入]] — operator new、placement new
- [[cpp-allocator与PMR]] — 自定义分配器、多态分配器
- [[cpp-小对象优化]] — SSO/SBO、栈上存储
- [[cpp-内存泄漏检测]] — ASan、valgrind、heaptrack
- [[cpp-悬垂指针与use-after-free]] — 常见来源、防御手段
- [[cpp-异常处理性能开销]] — 零开销模型、table-based

## C++ — 移动语义与值类别

- [[cpp-右值引用与移动语义]] — std::move、完美转发、5/3/0 法则
- [[cpp-move-only类型]] — 独占所有权、不可拷贝
- [[cpp-拷贝省略与RVO]] — RVO、NRVO、C++17 强制省略
- [[cpp-emplace操作]] — 原地构造
- [[cpp-function实现原理]] — 类型擦除、小对象优化

## C++ — 并发与多线程

- [[cpp-thread与线程管理]] — thread 创建、jthread、线程管理
- [[cpp-mutex与lock]] — mutex、lock_guard、unique_lock、scoped_lock
- [[cpp-condition-variable]] — 条件变量、生产者-消费者
- [[cpp-future与async]] — future、promise、packaged_task
- [[cpp-atomic与内存序]] — 原子操作、六种内存序
- [[cpp-递归互斥锁与读写锁深入]] — recursive_mutex、shared_mutex
- [[cpp-call_once与thread_local]] — 恰好一次初始化、线程局部存储
- [[cpp-信号量与屏障]] — counting_semaphore、latch、barrier
- [[cpp-jthread与协作式取消]] — 自动 join、stop_token
- [[cpp-内存模型与数据竞争]] — happens-before、可见性
- [[cpp-内存屏障与CPU重排]] — fence、SFENCE/LFENCE/MFENCE
- [[cpp-线程安全与数据竞争检测]] — TSan、线程安全级别
- [[cpp-并发队列与线程池]] — 线程池实现、带返回值的任务
- [[cpp-并发模式总览]] — 各层次并发抽象选型
- [[cpp-异步编程模型对比]] — callback、future、协程对比

## C++ — 现代 C++ 特性

- [[cpp-cpp11特性汇总]] — auto、lambda、移动语义、智能指针
- [[cpp-cpp14特性汇总]] — 泛型 lambda、make_unique、constexpr 增强
- [[cpp-cpp17特性汇总]] — 结构化绑定、if constexpr、optional、variant
- [[cpp-cpp20特性汇总]] — Concepts、Ranges、协程、Modules
- [[cpp-cpp23新特性]] — print、deducing this、expected、mdspan
- [[cpp-range库]] — 管道操作、惰性视图
- [[cpp-协程]] — co_await、co_yield、generator
- [[cpp-modules]] — import/export、替代头文件
- [[cpp-spaceship运算符]] — <=>、自动生成比较运算符
- [[cpp-optional]] — 可选值、monadic 操作
- [[cpp-variant]] — 类型安全联合体、visit
- [[cpp-any]] — 任意类型容器
- [[cpp-expected]] — C++23 值或错误
- [[cpp-span]] — 连续数据视图
- [[cpp-format]] — 类型安全格式化
- [[cpp-print与println]] — C++23 直接输出
- [[cpp-filesystem]] — 路径、目录遍历、文件操作
- [[cpp-属性]] — nodiscard、maybe_unused、likely
- [[cpp-deducing-this]] — C++23 显式对象参数
- [[cpp自定义字面量]] — operator""、编译期哈希

## C++ — 函数式与设计

- [[cpp-函数指针与function]] — 函数指针、std::function
- [[cpp-函数对象]] — functor、预定义函数对象
- [[cpp-类型擦除]] — type erasure 原理、实现
- [[cpp-函数式编程模式深入]] — 高阶函数、管道、Option 模式
- [[cpp-any与variant对比]] — 选型指南
- [[cpp-异常vs错误码]] — 错误处理策略选择
- [[cpp-异常安全深入]] — 基本/强保证、copy-and-swap
- [[cpp-const正确性]] — const 成员函数、const 引用
- [[cpp-代码规范与最佳实践]] — 命名、接口设计、内存管理
- [[cpp-代码审查清单]] — 安全、资源、类型、并发检查点
- [[cpp-常见陷阱与反模式]] — vector<bool>、map::operator[] 等

## C++ — 模板进阶

- [[cpp-模板特化与偏特化]] — 全特化、偏特化、函数模板重载替代
- [[cpp-ADL参数依赖查找]] — 参数依赖查找、swap 惯用法
- [[cpp-编译期控制流]] — if constexpr、constexpr 循环、递归模板
- [[cpp-if-consteval]] — 编译期/运行时分支

## C++ — 并发进阶

- [[cpp-内存序实际应用示例]] — 自旋锁、双重检查锁、生产者消费者
- [[cpp-并发安全的数据结构设计]] — 粗粒度锁、细粒度锁、无锁 CAS

## C++ — STL 深入

- [[cpp-counted-iterator与ranges视图]] — counted_iterator、iota_view、repeat
- [[cpp-容器适配器深入]] — 适配器本质、自定义适配器

## C++ — 工具链与工程

- [[cpp-编译器内联决策]] — 自动内联启发式、帮助编译器内联
- [[cpp-编译器警告指南]] — -Wall/-Wextra、常见警告及修复
- [[cpp-CMake基础]] — 现代 CMake、target-based
- [[cpp-编译优化与链接优化]] — -O2、LTO、PGO、内联
- [[cpp-编译时间优化]] — Pimpl、前向声明、显式实例化
- [[cpp-内联函数深入]] — inline 的现代含义
- [[cpp-编译器内建函数]] — __builtin_popcount、__builtin_expect
- [[cpp-调试技术与断言]] — assert、static_assert、ASan、UBSan
- [[cpp-宏与调试输出]] — 调试宏、条件日志
- [[cpp-clang-tidy与静态分析]] — 代码质量自动化检查
- [[cpp-测试基础]] — Google Test、编译期测试
- [[cpp-性能分析与基准测试]] — profiling、Google Benchmark
- [[cpp-性能优化速查]] — 算法、数据结构、缓存、编译器
- [[cpp-缓存友好设计]] — 数据局部性、false sharing、SoA vs AoS
- [[cpp-随机数与分布]] — mt19937、uniform/normal 分布
- [[cpp-多态容器与类型擦除容器]] — variant vs any vs OOP
- [[cpp-时间库chrono]] — duration、time_point、clock

## C++ — 设计模式与惯用法

- [[cpp-Pimpl惯用法]] — 编译防火墙、pointer to implementation
- [[cpp-Scope-Guard]] — 作用域守卫、异常安全清理
- [[cpp-对象池模式]] — placement new、内存复用

## C++ — 工程实践

- [[cpp-前向声明与减少依赖]] — 前向声明规则、fwd.h
- [[cpp-智能指针与容器]] — vector<unique_ptr>、多态容器
- [[cpp-字符串拼接与性能]] — reserve、ostringstream、std::format
- [[cpp-函数返回多个值]] — struct/pair/optional/expected 选型
- [[cpp-异常与构造函数]] — 构造函数异常、部分构造析构规则
- [[cpp-模板友元]] — 模板类的友元声明
- [[cpp-编译期类型列表与类型操作]] — TypeList、Head/Tail、IndexOf

## C++ — 并发与线程安全

- [[cpp-并发中的死锁与避免]] — 锁顺序、scoped_lock、锁层级
- [[cpp-线程安全的懒初始化]] — static局部变量、call_once、双重检查锁
- [[cpp-unordered-multimap与multiset]] — 多键哈希容器

## C++ — 编译期编程

- [[cpp-编译期校验与static_assert]] — 编译期断言、禁止实例化
- [[cpp-constinit]] — 编译期初始化但可修改
- [[cpp-编译期字符串处理]] — constexpr string、编译期哈希

## C++ — 进阶设计

- [[cpp-变量生命周期与存储期]] — 自动/静态/线程/动态存储期
- [[cpp-嵌套类与局部类]] — 嵌套类访问权限、局部类限制
- [[cpp-位字段]] — struct 位域、内存布局
- [[cpp-表达式模板]] — 延迟求值、Eigen 核心技术

## C++ — 语法与语义

- [[cpp-尾置返回类型]] — auto 返回类型、decltype
- [[cpp-委托构造函数]] — 构造函数链、代码复用
- [[cpp-移动语义与异常安全]] — noexcept 移动、vector 扩容决策
- [[cpp-ABI与二进制兼容]] — ABI 稳定、Pimpl 与接口
- [[cpp-编译期整数序列]] — index_sequence、参数包展开
- [[cpp-lambda与递归]] — 递归 lambda 四种方案
- [[cpp-pair与tuple]] — pair/tuple 操作、结构化绑定
- [[cpp-ranges管道与适配器]] — 管道机制、自定义适配器
- [[cpp-编译器特定扩展]] — GCC/Clang/MSVC 扩展封装
- [[cpp-ODR-use与未使用变量]] — ODR-use、maybe_unused

## C++ — 模板进阶（续）

- [[cpp-模板特化选择规则]] — 偏序规则、全特化 vs 偏特化
- [[cpp-模板显式实例化]] — extern template、显式实例化定义
- [[cpp-sizeof参数包]] — sizeof... 运算符

## C++ — 工程实践（续）

- [[cpp-预编译头PCH]] — PCH 创建与使用、CMake 集成
- [[cpp-浮点数精度与比较]] — 浮点比较、epsilon、ULP
- [[cpp-零初始化与值初始化]] — 初始化规则、统一初始化
- [[cpp-reference-wrapper]] — 可拷贝引用、容器中的引用
- [[cpp-std-byte]] — 原始字节类型、位操作
- [[cpp-function与lambda性能对比]] — 调用开销、内联
- [[cpp-if-constexpr最佳实践]] — 使用模式、常见陷阱
## C++ — 深入剖析（新增）

- [[cpp-协程机制深入]] — 协程帧、promise_type、awaitable、状态机
- [[cpp-memory-order实战剖析]] — 六种内存序的真实场景选择
- [[cpp-类型擦除深度剖析]] — std::function 内部实现、SBO
- [[cpp-自旋锁与排队自旋锁]] — TAS/Ticket/MCS 三种锁对比
- [[cpp-shared_ptr控制块揭秘]] — 控制块结构、make_shared 优势与陷阱
- [[cpp-完美转发与引用折叠]] — 转发引用、引用折叠规则、std::forward
- [[cpp-epoll与高性能服务器模型]] — epoll 原理、LT/ET、Reactor 框架
- [[cpp-variant访问的四种模式]] — visit、overload set、模式匹配
- [[cpp-编译期字符串hash与switch-string]] — FNV-1a、consteval、switch-string
- [[cpp-copy-and-swap惯用法]] — 异常安全赋值、强异常保证

- [[cpp-虚表布局与多重继承]] — vtable 内部结构、多重继承 vptr 偏移
- [[cpp-无锁SPSC队列实现]] — 单生产者单消费者无锁队列完整实现
- [[cpp-异常处理的零开销模型]] — table-based 异常、landing pad、栈展开
- [[cpp-move-if-noexcept与强异常保证]] — 条件移动、vector 扩容异常安全
- [[cpp-SFINAE的现代替代方案]] — concepts vs if constexpr vs requires
- [[cpp-placement-new与内存管理分层]] — operator new 分层、arena 分配器
- [[cpp-structured-binding与自定义类型支持]] — tuple-like 协议、自定义解构
- [[cpp-constexpr-分配与编译期容器]] — C++20 编译期 vector/string/排序
- [[cpp-lambda-闭包对象的内存布局]] — lambda 编译器展开、捕获的底层
- [[cpp-Rust风格Result在C++中的实践]] — std::expected 链式操作、and_then

## Linux — 文件系统与目录

- [[linux-文件系统层次标准]] — FHS 目录结构规范
- [[linux-目录操作基础命令]] — cd/ls/pwd/mkdir/rmdir
- [[linux-文件操作基础命令]] — cat/cp/mv/rm/touch

## Linux — 权限与用户

- [[linux-文件权限与-chmod]] — rwx 权限、SUID/SGID/Sticky
- [[linux-用户与用户组管理]] — useradd/groupadd/passwd

## Linux — Shell 与文本

- [[linux-管道与重定向]] — stdin/stdout/stderr、管道、xargs
- [[linux-文本处理三剑客]] — grep/sed/awk
- [[linux-shell-基础语法]] — 变量、条件、循环、脚本结构

## Linux — 进程管理

- [[linux-进程基础与-ps-命令]] — ps/top/proc 文件系统
- [[linux-信号与-kill-命令]] — 信号机制、kill/killall

## Linux — 网络

- [[linux-网络基础命令]] — ip/ss/ping/curl/dig

- [[linux-硬链接与软链接]] — hard link vs symlink 对比
- [[linux-后台任务与-nohup]] — nohup/disown/screen/tmux
- [[linux-find-命令]] — 按名称/类型/大小/时间查找文件
- [[linux-grep-高级用法]] — PCRE、上下文、多模式、提取
- [[linux-sed-高级用法]] — 地址范围、保持空间、多命令
- [[linux-awk-高级用法]] — 数组统计、流程控制、自定义函数
- [[linux-crontab-定时任务]] — cron 格式、环境变量、示例
- [[linux-systemctl-与-systemd]] — 服务管理、journalctl、unit 文件
- [[linux-SSH-配置与安全]] — 密钥、config、隧道、安全加固
- [[linux-磁盘与分区管理]] — lsblk/fdisk/mount/LVM/fstab

- [[linux-包管理-apt-与-yum]] — apt/dpkg vs yum/dnf
- [[linux-内存管理基础]] — free/swap/OOM Killer
- [[linux-TCP-连接状态与排查]] — TIME_WAIT/CLOSE_WAIT 排查
- [[linux-防火墙-iptables]] — filter/nat 表、NAT、规则管理
- [[linux-inode-与文件系统原理]] — inode 结构、ext4 布局
- [[linux-正则表达式速查]] — BRE/ERE/PCRE 语法
- [[linux-sudo-与提权机制]] — sudoers 配置、安全策略
- [[linux-ACL-访问控制列表]] — setfacl/getfacl 细粒度权限
- [[linux-日志系统-rsyslog-与-journal]] — journalctl、日志管理
- [[linux-内核模块管理]] — modprobe/lsmod/黑名单

- [[linux-启动流程与-initramfs]] — BIOS/UEFI→GRUB→initramfs→systemd
- [[linux-性能分析工具]] — top/vmstat/iostat/perf/sar
- [[linux-LVM-逻辑卷管理]] — PV/VG/LV 创建、扩展、快照
- [[linux-Shell-函数与脚本进阶]] — 函数、trap、数组、调试
- [[linux-DNS-解析与配置]] — resolv.conf/systemd-resolved/dig
- [[linux-虚拟内存与-mmap]] — 进程地址空间、mmap、COW
- [[linux-cgroup-资源限制]] — CPU/内存/进程数限制
- [[linux-namespace-隔离机制]] — PID/NET/MOUNT namespace
- [[linux-systemd-timer-定时器]] — OnCalendar、Persistent
