---
title: C++ 宏与调试输出
tags: [cpp, macro, debug, logging, trace, conditional-compilation]
aliases: [调试输出, debug macro, 日志宏, trace, 条件编译调试]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 宏与调试输出

调试宏是开发阶段的利器——编译时自动开关，Release 模式零开销。

## 调试输出宏

```cpp
#ifdef DEBUG
    #define DBG(x) std::cerr << "[DBG] " << __FILE__ << ":" << __LINE__ \
                             << " " << #x << " = " << (x) << "\n"
    #define TRACE() std::cerr << "[TRACE] " << __func__ << "\n"
#else
    #define DBG(x)    // 空——Release 模式零开销
    #define TRACE()
#endif

// 使用
DBG(variable_name);        // 输出 "[DBG] main.cpp:42 variable_name = 42"
TRACE();                   // 输出 "[TRACE] my_function"
```

## 条件日志

```cpp
#define LOG(level, msg) \
    do { \
        if (level <= current_log_level) { \
            std::cerr << "[" #level "] " << __FILE__ << ":" << __LINE__ \
                      << " " << msg << "\n"; \
        } \
    } while(0)

enum { LOG_ERROR = 0, LOG_WARN = 1, LOG_INFO = 2, LOG_DEBUG = 3 };
int current_log_level = LOG_DEBUG;

LOG(LOG_ERROR, "Connection failed: " << errno);
LOG(LOG_DEBUG, "Value = " << value);
```

## 性能计时宏

```cpp
#ifdef DEBUG
    #define TIME_IT(label, code) \
        do { \
            auto _start = std::chrono::high_resolution_clock::now(); \
            code; \
            auto _end = std::chrono::high_resolution_clock::now(); \
            auto _dur = std::chrono::duration_cast<std::chrono::microseconds>(_end - _start); \
            std::cerr << label << ": " << _dur.count() << " μs\n"; \
        } while(0)
#else
    #define TIME_IT(label, code) code
#endif

TIME_IT("sort", std::sort(v.begin(), v.end()));
```

## 关键要点

> 调试宏在 `#ifdef DEBUG` 下有输出，Release 模式编译为空——零性能开销。

> `do { ... } while(0)` 是宏定义的标准技巧——保证宏在 if/else 等语句中行为正确。

## 相关模式 / 关联

- [[cpp-预处理器]] — 宏的基础
- [[cpp-调试技术与断言]] — 断言与调试
