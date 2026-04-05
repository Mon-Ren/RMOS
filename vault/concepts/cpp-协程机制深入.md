---
title: C++20 协程机制深入
tags: [cpp20, coroutine, coroutine-frame, promise-type, compiler-magic]
aliases: [协程机制, coroutine 深入, 协程帧, 编译器生成状态机]
created: 2026-04-05
updated: 2026-04-05
---

# C++20 协程机制深入

**一句话概述：** C++20 协程的本质是编译器把一个函数拆成多个片段（suspension points），在堆上分配一个"协程帧"保存局部状态，每次挂起/恢复就是在切换这个帧里的执行位置——你写的 `co_await`/`co_yield` 背后是一整套类型推导和代码变换。

## 意图与场景

- 理解协程不是"语法糖"，而是编译器层面的代码变换
- 搞清楚 `co_await` 时编译器到底调了哪些方法、按什么顺序
- 写自己的 `task`/`generator` 时知道每一步在做什么

## 核心机制

### 协程帧（Coroutine Frame）

当你写一个包含 `co_await`/`co_yield`/`co_return` 的函数时，编译器会在堆上分配一个协程帧：

```
协程帧布局（概念性）:
┌──────────────────────────────┐
│ promise_type 对象             │  ← 编译器构造
│ 参数的拷贝（by-value）        │  ← 如果参数是 by-value
│ 局部变量                     │  ← 跨 suspension point 存活的局部变量
│ 暂停点标记（coroutine state） │  ← 当前执行到第几个 co_await
│ 分配器信息（可选）            │  ← 自定义分配
└──────────────────────────────┘
```

关键：**不是所有局部变量都进协程帧**。只有跨 suspension point 存活的变量才需要保存。编译器做活跃性分析（liveness analysis）来最小化帧大小。

```cpp
Task<int> compute(int n) {
    int x = n * 2;         // ← x 跨 co_await 存活 → 进帧
    auto result = co_await fetch_data(x);  // 挂起点 1
    {
        int temp = result + 1;  // ← temp 在下一个 co_await 前已销毁 → 不进帧
    }
    int y = result * 3;    // ← y 跨 co_await 存活 → 进帧
    co_return y;           // 挂起点 2
}
```

### 三个核心类型

协程机制围绕三个类型协作，缺一不可：

#### 1. promise_type — 协程的"灵魂"

编译器根据协程函数的返回类型 `R` 找到 `R::promise_type`（或通过 `std::coroutine_traits<R, Args...>::promise_type`）。

```cpp
struct Task {
    struct promise_type {
        // ① 协程创建时调用
        Task get_return_object() {
            return Task{
                std::coroutine_handle<promise_type>::from_promise(*this)
            };
        }

        // ② 初始挂起点：立即挂起 vs 立即执行
        // suspend_always → 协程创建后先挂起（惰性启动）
        // suspend_never  → 协程创建后立即开始执行第一段
        std::suspend_always initial_suspend() { return {}; }

        // ③ co_return 时调用
        void return_value(int v) { result_ = v; }
        // 如果协程是 void 返回值，用 return_void()

        // ④ 协程结束时调用（正常结束或未捕获异常）
        std::suspend_always final_suspend() noexcept { return {}; }

        // ⑤ 异常处理：未捕获异常时调用
        void unhandled_exception() {
            exception_ = std::current_exception();
        }

        int result_;
        std::exception_ptr exception_;
    };
};
```

#### 2. Awaitable — 可等待对象

`co_await expr` 中的 `expr` 必须是 Awaitable。一个类型是 Awaitable 当且仅当它有这三个成员函数（或能通过 `operator co_await` 转换成有这三个函数的类型）：

```cpp
struct HttpAwaitable {
    // ① 是否需要挂起？返回 false = 不挂起，继续执行
    bool await_ready() {
        return request_.is_complete();  // 如果已经完成就不挂起
    }

    // ② 挂起时调用：保存 continuation，注册回调
    //    返回值可以是 void（总是挂起）、bool、或另一个 Awaitable
    void await_suspend(std::coroutine_handle<> h) {
        continuation_ = h;
        request_.on_complete([this]() {
            continuation_.resume();  // 数据到达后恢复协程
        });
    }

    // ③ 恢复后调用：返回 co_await 表达式的值
    int await_resume() {
        return request_.get_result();
    }

    HttpRequest request_;
    std::coroutine_handle<> continuation_;
};
```

调用顺序：`await_ready()` → (如果返回 false) → `await_suspend(handle)` → (将来某个时刻 `handle.resume()`) → `await_resume()`

#### 3. coroutine_handle — 控制杆

`std::coroutine_handle<promise_type>` 是指向协程帧的轻量指针（通常就是一个指针大小）：

```cpp
// 关键操作
auto h = std::coroutine_handle<promise_type>::from_promise(p);
h.resume();    // 恢复协程执行
h.destroy();   // 销毁协程帧（释放内存）
h.done();      // 协程是否已执行完毕（到达 final_suspend）
auto& p = h.promise();  // 获取 promise 引用
```

## 完整流程图解

```
调用协程函数
    │
    ▼
① operator new 分配协程帧
    │
    ▼
② 在帧中构造 promise_type 对象
    │
    ▼
③ 调用 promise.get_return_object() → 返回值给调用者
    │
    ▼
④ 调用 promise.initial_suspend()
    │   ├── 返回 suspend_always → 协程暂停，调用者拿到 handle
    │   └── 返回 suspend_never  → 继续执行协程体
    ▼
⑤ 执行协程体，直到遇到 co_await/co_yield
    │
    ▼
⑥ co_await expr:
    │   ├── expr.await_ready() 返回 true → 不挂起，直接 await_resume()
    │   └── 返回 false → 调用 expr.await_suspend(handle)
    │       此时协程暂停，控制权返回给 resume() 的调用者
    │
    ▼ （某个时刻 handle.resume() 被调用）
    │
⑦ 调用 expr.await_resume() → 获取值，继续执行
    │
    ▼ （循环 ⑤-⑦ 直到 co_return）
    │
⑧ co_return val → 调用 promise.return_value(val)
    │
    ▼
⑨ 调用 promise.final_suspend()
    │   ├── 返回 suspend_always → 协程暂停（等待调用者 destroy）
    │   └── 返回 suspend_never  → 自动销毁协程帧
```

## 手写一个 generator（无标准库）

```cpp
#include <coroutine>
#include <exception>
#include <utility>

template <typename T>
class Generator {
public:
    struct promise_type {
        T current_value_;

        Generator get_return_object() {
            return Generator{
                std::coroutine_handle<promise_type>::from_promise(*this)
            };
        }

        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }

        // co_yield expr 会被翻译成 co_await promise.yield_value(expr)
        std::suspend_always yield_value(T value) {
            current_value_ = std::move(value);
            return {};
        }

        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };

    // 迭代器
    class iterator {
        std::coroutine_handle<promise_type> h_ = nullptr;
    public:
        iterator() = default;
        explicit iterator(std::coroutine_handle<promise_type> h) : h_(h) {}

        iterator& operator++() {
            h_.resume();
            if (h_.done()) h_ = nullptr;
            return *this;
        }

        T operator*() const { return h_.promise().current_value_; }
        bool operator==(std::nullptr_t) const { return h_ == nullptr; }
        bool operator!=(std::nullptr_t) const { return h_ != nullptr; }
    };

    iterator begin() {
        if (!handle_) return nullptr;
        handle_.resume();           // 执行到第一个 co_yield
        if (handle_.done()) return nullptr;
        return iterator{handle_};
    }

    iterator end() { return nullptr; }

    ~Generator() { if (handle_) handle_.destroy(); }

private:
    explicit Generator(std::coroutine_handle<promise_type> h) : handle_(h) {}
    std::coroutine_handle<promise_type> handle_;
};

// 使用
Generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;
        auto next = a + b;
        a = b;
        b = next;
    }
}

// for (auto val : fibonacci()) {
//     if (val > 100) break;
//     std::cout << val << " ";  // 0 1 1 2 3 5 8 13 21 34 55 89
// }
```

## 关键要点

> 协程帧的分配可以用自定义 allocator 避免——`promise_type` 定义 `operator new`/`operator delete` 即可控制。对于高频调用的协程，这是性能关键。

> `co_await` 不是"等待"，而是"挂起并注册恢复回调"。协程挂起后控制权立即返回给调用者，不会阻塞线程。

> `coroutine_handle<void>` 和 `coroutine_handle<promise_type>` 的区别：前者类型擦除了 promise，可以 resume/destroy 但不能访问 promise；后者能访问 promise 的所有成员。

> `initial_suspend` 返回 `suspend_always` 意味着"惰性启动"（lazy）——协程创建后不立即执行，需要调用者显式 `resume()`。返回 `suspend_never` 是"急切启动"（eager）。选择哪种取决于语义：generator 适合 lazy，task 适合 eager。

## 相关模式 / 关联

- [[cpp-协程]] — C++20 协程基础语法
- [[cpp-异步编程模型对比]] — callback vs future vs 协程对比
- [[cpp-类型擦除]] — coroutine_handle 的类型擦除本质
- [[cpp-future与async]] — 协程是 future/promise 模型的演进
- [[cpp-move-only类型]] — coroutine_handle 的所有权语义
