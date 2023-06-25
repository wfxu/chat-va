import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import Chat from '@/views/chat/index.vue'
import Content from '@/views/chat/content/index.vue'

const routes: RouteRecordRaw[] = [

  {
    path: '/',
    name: 'Root',
    component: Chat,
    redirect: '/chat',
    children: [
      {
        path: 'chat/:uuid?',
        name: 'Chat',
        component: Content,
      },
    ],
  },
  

];

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
});
