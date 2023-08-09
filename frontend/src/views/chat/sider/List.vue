<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { PlusOutlined, CloseOutlined } from '@ant-design/icons-vue'

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

const addItem = () => {
  axios.get('http://127.0.0.1:8000/chat/add')
    .then(response => {
      console.log(response.data)
      axios.get('http://127.0.0.1:8000/chat')
        .then(response => {
          items.value = response.data
        })
        .catch(error => {
          console.error(error)
        })
      router.push(`/chat/${response.data.u_id}`)
    })
    .catch(error => {
      console.error(error)
    })
}

const visible = ref<boolean>(false)
const currentItem = ref('')
const showModal = (item: string) => {
  currentItem.value = item
  visible.value = true
}
const deleteConversation = () => {
  axios.post(`http://127.0.0.1:8000/chat/delete/${currentItem.value}`)
  .then(response => {
    if (response.data.status == 'success') {
      visible.value = false
      axios.get('http://127.0.0.1:8000/chat')
          .then(response => {
            items.value = response.data
          })
          .catch(error => {
            console.error(error)
          })
    }
  })
  .catch(error => {
    console.error(error)
  })
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
      <div class="flex justify-between w-full group">
        <div class="text-left text-base">
          {{ item }}
        </div>
        <div  class="text-right opacity-0 group-hover:opacity-100">
          <a-button @click="showModal(item)">
            <template #icon>
              <close-outlined style="font-size: 30px;" />
            </template>
          </a-button>
          <a-modal v-model:visible="visible" @ok="deleteConversation" title="删除会话">
            <p> 是否删除这个对话框 </p>
          </a-modal>
        </div>
      </div>
      </a>
      <a v-if="items.length < 10" 
        class="relative flex justify-center gap-3 px-3 py-3 break-all border rounded-md cursor-pointer hover:bg-neutral-100 group dark:border-neutral-800 dark:hover:bg-[#24272e]">
        <plus-outlined style="font-size: 30px;" @click="addItem" />
      </a>
    </div>
</template>