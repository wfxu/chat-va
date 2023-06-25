<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const items = ref([])
axios.get('http://127.0.0.1:8000/chat')
  .then(response => {
    items.value = response.data
  })
  .catch(error => {
    console.error(error)
  })

const router = useRouter()
const handleClick = (item: string) => {
    router.push(`/chat/${item}`)
    // 不需要后端这个就可以注释掉，我擦，这个把我搞疯了
    // const url = `http://127.0.0.1:8000/chat/${item}`
    // axios.get(url).then(response => {
    //     chatId.value = response.data.message
    //     console.log(chatId)
    // }).catch(error => {
    //     console.error(error)
    // })

}
</script>

<template>
    <div class="flex flex-1 flex-col h-full">
        <a 
            v-for="item in items" 
            :key="item" 
            @click="handleClick(item)"
            class="relative flex items-center gap-3 px-3 py-3 break-all border rounded-md cursor-pointer hover:bg-neutral-100 group dark:border-neutral-800 dark:hover:bg-[#24272e]"
            >
            {{ item }}
        </a>
    </div>
</template>