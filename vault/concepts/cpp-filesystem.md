---
title: std::filesystem（C++17）
tags: [cpp17, filesystem, path, directory, file-io]
aliases: [filesystem, 文件系统, path, directory_iterator, 递归目录]
created: 2026-04-04
updated: 2026-04-04
---

# std::filesystem（C++17）

`std::filesystem` 是 C++ 对文件系统操作的标准接口——跨平台的路径处理、目录遍历、文件状态查询。

## 意图与场景

- 跨平台路径拼接和解析
- 遍历目录树
- 文件/目录的创建、删除、复制
- 查询文件大小、修改时间

## path 操作

```cpp
#include <filesystem>
namespace fs = std::filesystem;

// 路径构造
fs::path p1 = "/home/user/documents/file.txt";
fs::path p2 = "C:\\Users\\file.txt";        // Windows
fs::path p3 = fs::current_path();           // 当前工作目录

// 路径拼接（operator/ 而非 operator+）
fs::path full = p1.parent_path() / "other.txt";  // /home/user/documents/other.txt

// 路径分解
p1.root_path();       // "/"
p1.filename();        // "file.txt"
p1.stem();            // "file"
p1.extension();       // ".txt"
p1.parent_path();     // "/home/user/documents"

// 路径规范化
fs::path messy = "/home/user/../user/./docs";
messy.lexically_normal();  // "/home/user/docs"
```

## 文件操作

```cpp
// 存在性与类型
fs::exists("config.txt");                     // 文件是否存在
fs::is_regular_file("config.txt");            // 是否普通文件
fs::is_directory("docs/");                    // 是否目录

// 文件大小和时间
auto size = fs::file_size("data.bin");        // 返回 uintmax_t
auto time = fs::last_write_time("file.txt");  // 最后修改时间

// 创建与删除
fs::create_directory("new_dir");              // 创建单层目录
fs::create_directories("a/b/c");              // 递归创建
fs::remove("file.txt");                       // 删除文件
fs::remove_all("dir/");                       // 递归删除目录

// 复制与移动
fs::copy("src.txt", "dst.txt");               // 复制文件
fs::copy("src_dir", "dst_dir", fs::copy_options::recursive);  // 递归复制目录
fs::rename("old.txt", "new.txt");             // 重命名/移动
```

## 目录遍历

```cpp
// 非递归遍历
for (const auto& entry : fs::directory_iterator(".")) {
    std::cout << entry.path() << "\n";
}

// 递归遍历
for (const auto& entry : fs::recursive_directory_iterator(".")) {
    if (entry.is_regular_file() && entry.path().extension() == ".cpp") {
        std::cout << entry.path() << "\n";
    }
}

// C++20：范围接口
for (const auto& entry : fs::directory_iterator(".") |
     std::views::filter([](const auto& e) { return e.is_regular_file(); })) {
    // ...
}
```

## 关键要点

> 路径拼接用 `operator/`（不是 `+`），它自动处理路径分隔符的跨平台差异。`path` 对象到 `string` 的转换需要显式调用 `.string()` 或 `.generic_string()`。

> 文件系统操作可能失败——用异常版本或检查 `std::error_code` 重载。

## 相关模式 / 关联

- [[cpp-异常处理]] — filesystem 的异常处理
- [[cpp-string深入]] — path 与 string 的转换
