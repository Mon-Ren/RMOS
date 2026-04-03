---
title: "xv6 shell 工作原理"
tags: [xv6, shell, parser, pipe, redirect]
aliases: ["Shell", "命令解析器", "sh.c"]
created: 2026-04-04
updated: 2026-04-04
---

# xv6 shell 工作原理

xv6 的 shell（sh.c）是一个精简的命令解析器，将命令行解析为**命令树**（command tree），然后递归执行。它展示了管道、重定向和后台执行的底层原理。

## 核心机制

### 命令树数据结构

xv6 shell 不使用传统的 token 流，而是构建**递归命令树**：

```c
// sh.c:14 — 基础命令
struct execcmd {
  int type;              // ' '
  char *argv[MAXARG];
  char *eargv[MAXARG];
};

// sh.c:26 — 重定向命令
struct redircmd {
  int type;              // '<' 或 '>'
  struct cmd *cmd;       // 被包装的子命令
  char *file;
  int mode;
  int fd;
};

// sh.c:35 — 管道命令
struct pipecmd {
  int type;              // '|'
  struct cmd *left;      // 左侧命令
  struct cmd *right;     // 右侧命令
};
```

示例：`ls | grep foo > output.txt`

```
redircmd (>)
  ├─ file: "output.txt"
  ├─ fd: 1
  └─ cmd: pipecmd (|)
       ├─ left: execcmd (ls)
       └─ right: execcmd (grep foo)
```

### 命令执行（递归遍历）

```c
// sh.c:60 — runcmd 递归执行命令树
void runcmd(struct cmd *cmd) {
  switch(cmd->type){
  case ' ':  // 普通命令
    ecmd = (struct execcmd*)cmd;
    exec(ecmd->argv[0], ecmd->argv);
    printf(2, "exec %s failed\n", ecmd->argv[0]);
    break;

  case '>':  // 输出重定向
    rcmd = (struct redircmd*)cmd;
    close(rcmd->fd);
    open(rcmd->file, rcmd->mode);  // 打开文件，fd 自动为最低可用号
    runcmd(rcmd->cmd);              // 递归执行子命令
    break;

  case '|':  // 管道
    pcmd = (struct pipecmd*)cmd;
    pipe(p);
    if(fork1() == 0){              // 左子进程
      close(1);                    // 关闭 stdout
      dup(p[1]);                   // dup 到 fd=1
      close(p[0]); close(p[1]);
      runcmd(pcmd->left);
    }
    if(fork1() == 0){              // 右子进程
      close(0);                    // 关闭 stdin
      dup(p[0]);                   // dup 到 fd=0
      close(p[0]); close(p[1]);
      runcmd(pcmd->right);
    }
    close(p[0]); close(p[1]);
    wait(); wait();                // 等待两个子进程
    break;
  }
  exit();
}
```

### 管道实现细节

`ls | grep foo` 的 fd 变化：

```
父进程 (shell)
  pipe(p) → p[0]=3, p[1]=4

  fork() → 左子进程 (ls)
    close(1)        fd: [ -,  -, -, 4 ]
    dup(4)          fd: [ -, 1, -, 4 ]    ← stdout=1 指向管道写端
    close(4)        fd: [ -, 1, -, - ]
    exec("ls")      ls 的 stdout 写入管道

  fork() → 右子进程 (grep)
    close(0)        fd: [ -, -, 3, - ]
    dup(3)          fd: [ 0, -, 3, - ]    ← stdin=0 指向管道读端
    close(3)        fd: [ 0, -, -, - ]
    exec("grep")    grep 的 stdin 从管道读取

  父进程:
    close(3); close(4)  ← 关闭自己的管道副本
    wait(); wait()
```

### 重定向实现

`cmd > file` 的 fd 变化：

```
runcmd(redircmd):
  close(1)           fd: [ -, -, ... ]    ← 关闭 stdout
  open("file", O_CREATE|O_WRONLY)
                     fd: [ -, 1, ... ]    ← 文件获得 fd=1（最低可用）
  runcmd(execcmd)    exec 的 stdout 写入文件
```

利用了 fd 分配总是取最小可用号的特性（`open` 返回最低未用的 fd）。

### 命令行解析

```c
// sh.c — parsecmd 和 parseline 构建命令树
struct cmd* parsecmd(char *s) {
  struct cmd *cmd;
  cmd = parseline(&s);   // 解析整行
  peek(&s, s_end);
  if(s != s_end)
    panic("syntax");
  nulterminate(cmd);     // 终止所有字符串
  return cmd;
}

// 解析优先级: ; (最低) → | → > < → 命令 (最高)
struct cmd* parseline(char **ps)  // 解析 cmd1 ; cmd2
struct cmd* parsepipe(char **ps)  // 解析 cmd1 | cmd2
struct cmd* parseexec(char **ps)  // 解析基本命令或重定向
```

### 后台执行

```c
// sh.c:159 — 主循环
if(fork1() == 0)
  runcmd(parsecmd(buf));   // 子进程执行命令

// 非后台命令：父进程 wait
// 后台命令（& 结尾）：父进程不 wait，直接打印下一个提示符
if(!backcmd)
  wait();
```

### 内建命令

xv6 shell 有少数内建命令，在 fork 之前处理：

```c
if(buf[0] == 'c' && buf[1] == 'd' && buf[2] == ' '){
  buf[strlen(buf)-1] = 0;  // 去掉换行
  if(chdir(buf+3) < 0)
    printf(2, "cannot cd %s\n", buf+3);
  continue;  // 不 fork，直接读下一个命令
}
```

`cd` 必须在 shell 进程中执行（子进程的 chdir 不影响父进程）。

## 关键要点
> xv6 shell 将命令行解析为递归命令树（execcmd/redircmd/pipecmd），然后递归执行。管道通过 fork+pipe+dup+close 实现 fd 重定向，重定向利用 open 返回最小可用 fd 的特性。cd 是唯一内建命令。

## 关联
- [[xv6 管道]] — pipe() 系统调用的内核实现
- [[xv6 exec 详解]] — exec 加载并执行命令
- [[xv6 文件系统]] — open/close/dup 的 fd 管理
- [[xv6 系统调用]] — fork/pipe/open/exec/wait 等
- [[xv6 进程管理]] — fork/wait 的进程关系
