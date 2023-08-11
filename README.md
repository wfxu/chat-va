

## 基本介绍

### 项目介绍

> chat-va: chat virtual assistant，意指个人聊天助手。
>
> 初衷是将自己实现的功能放到web上供目标用户体验并收集反馈。

## 项目架构

### 技术选型

- 前端：[vue3](https://cn.vuejs.org/guide/introduction.html) + [ant design vue](https://www.antdv.com/components/overview-cn) + [vite](https://vitejs.dev/)
- 后端：[python](https://www.python.org/doc/) 的 [fastapi](https://fastapi.tiangolo.com/)

### 目录结构

```
|-- backend
    |-- main.py             // 后端主程序
    |-- openai_handle.py    // 处理openai接口程序
    |-- chat.db             // sqlite 数据库

|-- frontend
    |-- src                 // 存放源代码
        |-- assets          // 静态资源
        |-- router          // 路由声明文件
        |-- style           // 全局样式
        |-- utils           // 方法包库
        |-- view            // 主要view代码
            |-- chat        // chat 界面视图代码
        |-- App.vue         // 根组件
        |-- main.ts         // 入口文件
        |-- style.css       // 样式文件
    |-- index.html          // 用于挂载 Vue 应用程序的 HTML 入口文件
    |-- node_modules        // 存放所有安装的依赖包
    |-- package.json        // 项目元数据和依赖项列表
    |-- package-lock.json   // 锁定依赖项版本的文件
    |-- vite.config.js      // vite 工具的配置文件
    |-- tsconfig.json       // tsconfig 工具的配置文件
    |-- tsconfig.node.json  // tsconfig 工具的配置文件
    |-- README.md           // vite 工具的配置文件
    |-- tailwind.config.js  // tailwind 工具的配置文件
```

## 待实现路线
[✔]  聊天记录清空

[✔]  删除单条聊天记录

[✔]  修改单条发出记录

[✔]  重新生成ai记录

[✔]  新增聊天

[✔]  删除聊天

[✘]  用户登录、控制

[✘]  模型选项
