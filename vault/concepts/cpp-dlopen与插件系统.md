---
title: dlopen 与插件系统
tags: [system, dlopen, dlsym, plugin, shared-library, hot-reload]
aliases: [动态加载库, 插件架构, dlopen 实战]
created: 2026-04-05
updated: 2026-04-05
---

# dlopen 与插件系统

**一句话概述：** dlopen 在运行时加载 .so/.dll，dlsym 查找符号地址。用统一的插件接口（extern "C" 导出工厂函数），主程序可以在不重新编译的情况下加载新功能模块。

```cpp
#include <dlfcn.h>

// 插件接口（头文件）
struct Plugin {
    virtual ~Plugin() = default;
    virtual void execute() = 0;
};
using CreatePluginFunc = Plugin* (*)();

// 加载插件
void* handle = dlopen("./myplugin.so", RTLD_LAZY);
auto create = (CreatePluginFunc)dlsym(handle, "create_plugin");
Plugin* p = create();
p->execute();
delete p;
dlclose(handle);

// 插件实现（编译为 .so）
extern "C" Plugin* create_plugin() { return new MyPluginImpl(); }
```

## 关键要点

> dlopen 的陷阱：全局变量的初始化顺序不确定、异常不能跨 .so 边界传播（除非用相同的异常处理 ABI）、不同 .so 中的静态变量是独立的。

## 相关模式 / 关联

- [[cpp-动态链接库]] — 动态链接基础
- [[cpp-ABI与二进制兼容]] — ABI 兼容
- [[cpp-工厂方法模式]] — 工厂模式
