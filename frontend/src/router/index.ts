import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import Chat from '@/views/chat'

const routes: RouteRecordRaw[] = [
  // {
  //   path: '/login',
  //   name: 'Login',
  //   component: Login,
  // },
  {
    path: '/',
    name: 'chat',
    component: Chat,
  },
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
});
