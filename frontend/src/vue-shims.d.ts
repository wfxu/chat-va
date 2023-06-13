declare module '*.vue' {
    import { DefineComponent } from 'vue';
  
    // 使用 `defineComponent` 定义组件类型
    const component: DefineComponent<{}, {}, any>;
    export default component;
  }
  