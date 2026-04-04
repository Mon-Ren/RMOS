---
title: RAII 惯用法
tags: [cpp, idiom, RAII, resource-management]
aliases: [RAII, Resource Acquisition Is Initialization, 资源获取即初始化]
created: 2026-04-04
updated: 2026-04-04
---

# RAII 惯用法

**一句话概述：** 将资源的生命周期绑定到对象的生命周期——构造函数获取资源，析构函数自动释放，借助 C++ 作用域规则实现异常安全的资源管理。

## 意图与场景

RAII（Resource Acquisition Is Initialization）是 C++ 最核心的惯用法。其核心思想：

- **资源获取 = 对象初始化**：在构造函数中获取资源（内存、文件句柄、锁、网络连接等）
- **资源释放 = 对象销毁**：在析构函数中释放资源，编译器保证离开作用域时自动调用
- **异常安全**：即使发生栈展开（stack unwinding），析构函数仍会被调用

**适用场景：**
- 互斥锁的获取与释放
- 文件的打开与关闭
- 动态内存的分配与释放
- 数据库连接、事务管理
- 任何"获取-释放"配对的资源

## C++ 实现代码

### 经典 RAII 封装

```cpp
#include <memory>
#include <mutex>
#include <fstream>
#include <stdexcept>

// 自定义 RAII 包装：管理文件句柄
class FileHandle {
    FILE* fp_;
public:
    explicit FileHandle(const char* path, const char* mode)
        : fp_(std::fopen(path, mode)) {
        if (!fp_) throw std::runtime_error("Failed to open file");
    }
    
    ~FileHandle() {
        if (fp_) std::fclose(fp_);
    }
    
    // 禁止拷贝
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
    
    // 允许移动
    FileHandle(FileHandle&& other) noexcept : fp_(other.fp_) {
        other.fp_ = nullptr;
    }
    FileHandle& operator=(FileHandle&& other) noexcept {
        if (this != &other) {
            if (fp_) std::fclose(fp_);
            fp_ = other.fp_;
            other.fp_ = nullptr;
        }
        return *this;
    }
    
    FILE* get() const noexcept { return fp_; }
    explicit operator bool() const noexcept { return fp_ != nullptr; }
};
```

### 标准库 RAII 示例

```cpp
#include <memory>
#include <mutex>
#include <fstream>
#include <vector>

void demonstrate_raii() {
    // 1. unique_ptr —— 内存资源
    auto ptr = std::make_unique<std::vector<int>>(1000);
    // 离开作用域自动 delete
    
    // 2. lock_guard —— 互斥锁资源
    std::mutex mtx;
    {
        std::lock_guard<std::mutex> lock(mtx);
        // 临界区操作，离开作用域自动解锁
    }
    
    // 3. fstream —— 文件资源
    {
        std::ofstream file("output.txt");
        file << "Hello RAII\n";
        // 离开作用域自动关闭文件
    }
    
    // 4. scoped_lock —— 多锁管理（C++17）
    std::mutex mtx1, mtx2;
    {
        std::scoped_lock lock(mtx1, mtx2);  // 自动避免死锁
        // 同时持有两把锁
    }
}
```

### 异常安全保证

```cpp
// 异常安全的多资源管理
void transfer_data(const std::string& src, const std::string& dst) {
    std::ifstream in(src);    // RAII
    std::ofstream out(dst);   // RAII
    
    if (!in || !out) throw std::runtime_error("Cannot open files");
    
    std::string buffer;
    while (std::getline(in, buffer)) {
        out << buffer << '\n';
        // 即使这里抛异常，in 和 out 都会自动关闭
    }
}
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 自动资源释放，杜绝泄漏 | 需要为每种资源编写 RAII 包装类 |
| 异常安全有保证 | 对象销毁顺序依赖声明顺序（反序销毁） |
| 代码简洁，减少样板代码 | 不适用于跨作用域/跨线程共享资源 |
| 编译器保证，零运行时开销 | 移动语义使所有权转移变得复杂 |

> [!tip] 关键要点
> RAII 是 C++ 资源管理的基石。**永远不要手动管理资源**——永远用 `unique_ptr` 代替 `new/delete`，用 `lock_guard` 代替 `lock/unlock`，用 `fstream` 代替 `fopen/fclose`。RAII 不仅防泄漏，更是异常安全的前提条件。

> [!info] RAII 与异常安全级别
> - **基本保证**：异常后对象处于有效状态，无资源泄漏
> - **强保证**：操作要么成功，要么状态不变（commit-or-rollback）
> - **不抛保证**：操作绝不抛出异常（`noexcept`）
> RAII 保证了基本级别；结合 copy-and-swap 可实现强保证。

## 相关链接

- [[cpp-智能指针详解]] — RAII 最典型的应用
- [[cpp-scope-guard]] — RAII 的泛化，用于任意清理操作
- [[cpp-移动语义]] — RAII 对象的所有权转移
- [[cpp-pimpl-惯用法]] — 内部使用 unique_ptr 实现 RAII
- [[设计模式概述]] — 模板方法模式与 RAII 的结合
