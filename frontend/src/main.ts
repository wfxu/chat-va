import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { router } from './router/index'
import Anit from 'ant-design-vue'

const app = createApp(App)

app.use(Anit)
app.use(router)

app.mount('#app')
