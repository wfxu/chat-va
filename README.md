

## 基本介绍

### 项目介绍

> chat-va: chat virtual assistant，意指个人聊天助手。
>
> 初衷是将自己实现的功能放到web上供目标用户体验并收集反馈。

## 项目架构

### 技术选型

- 前端：[vue3]() + [ant design vue]() + [vite](https://vitejs.dev/)
- 后端：[python]() 的 [fastapi]()

### 目录结构

```
|-- server

|-- web
    |-- node_modules        // 存放所有安装的依赖包
    |-- src                 // 存放源代码
        |-- api             // api 组
        |-- assets          // 静态资源
        |-- componets       // 全局组件
        |-- router          // 路由声明文件
        |-- style           // 全局样式
        |-- utils           // 方法包库
        |-- view            // 主要view代码
        |-- App.vue         // 根组件
        |-- main.js         // 入口文件
    |-- index.html          // 用于挂载 Vue 应用程序的 HTML 入口文件
    |-- package.json        // 项目元数据和依赖项列表
    |-- package-lock.json   // 锁定依赖项版本的文件
    |-- vite.config.js      // vite 工具的配置文件
```