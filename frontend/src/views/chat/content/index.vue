<script setup lang="ts">
import { AliwangwangFilled, UpCircleFilled, RestFilled, ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons-vue'
import { ref, watch, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import Message from './Message.vue'
import { message } from 'ant-design-vue'

const route = useRoute()
const { uuid } = route.params as { uuid: string }
const dataSources = ref(<typeof Message[]>[])
const fetchData = async (uuid: string | string[]) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/chat/${uuid}`)
    dataSources.value = response.data.messages
    nextTick(() => {
      const container = document.getElementById('chatContainer');
      if (container) {
        container.scrollTo(0, container.scrollHeight);
      }
      messageInput.value.focus();
    });
  } catch (error) {
    console.error(error)
  }
}

watch(() => route.params.uuid, (newUuid) => {
  if (newUuid) {
    fetchData(newUuid);
  }
})

onMounted(() => {
  fetchData(route.params.uuid);
});

const search_string = ref('')

const visible = ref<boolean>(false);
const showModal = () => {
      visible.value = true;
    };
const onClear = () => {
    axios.post(`http://localhost:8000/chat/clear/${uuid}`
    ).then(response => {
        if (response.data.status == 'success') {
            fetchData(uuid);
            message.success('会话已经清空!');
            visible.value = false
        }
        
    }).catch(error => {
        console.log(error);
    })
}

const submitLoading = ref<boolean>(false)
const submitDisable = ref<boolean>(false)
const messageInput = ref(null)
const onSubmit = (e) => {
    if (e.shiftKey) {
        return;
    }

    submitLoading.value = true;
    const messageData = {
        u_id: uuid,
        dateTime: new Date().toLocaleString(),
        text: search_string.value,
        is_user: 1,
        error: 0,
        loading: 0,
    }
    search_string.value = '';
    submitDisable.value = true;
    axios.post('http://localhost:8000/chat/message', messageData)
    .then(response => {
        // 更新你的前端界面
        search_string.value = '';
        fetchData(uuid);
        submitLoading.value = false;
        submitDisable.value = false;
    }).catch(error => {
        console.log(error);
        submitLoading.value = false;
    });
}
const scrollToTop = () => {
    const container = document.getElementById('chatContainer');
    if (container) {
        container.scrollTo(0, 0);
    }
}

// 滚动到底部的方法
const scrollToBottom = () => {
    const container = document.getElementById('chatContainer');
    if (container) {
        container.scrollTo(0, container.scrollHeight);
    }
}

defineExpose({
    fetchData
})
</script>

<template>
    <a-layout-content class="flex-grow h-full bg-slate-600">
        <div class="flex flex-col w-full h-full">
            <main class="flex-1 overflow-hidden">
                <div class="h-full overflow-hidden overflow-y-auto" id="chatContainer">
                    <div class="w-full max-w-screen-xl m-auto dark:bg-[#101014] p-4">
                        <template v-if="!uuid">
                            <div class="flex items-center justify-center mt-4 text-center text-neutral-300">
                                <AliwangwangFilled class="mr-2 text-3xl" />
                                <span>Aha~</span>
                            </div>
                        </template>
                        <template v-else>
                            <div class="flex items-center justify-center mt-4 text-center text-neutral-300">
                                <AliwangwangFilled class="mr-2 text-3xl" />
                                <span>{{ uuid }}</span>
                            </div>
                            <div>
                                <Message 
                                    v-for="(item, index) of dataSources"
                                    :key="index"
                                    :u-id = "uuid"
                                    :m-id = "item.m_id"
                                    :date-time="item.datetime"
                                    :text="item.text"
                                    :inversion="item.is_user"
                                    :error="item.error"
                                    :loading="item.loading"
                                    :as-raw-text="item.is_user"
                                    :fetch-data="fetchData"
                                />
                            </div>
                        </template>
                    </div>
                </div>
            </main>
            <footer class="flex flex-row w-full max-h-36 dark:bg-[#101014] justify-center">
                <div class="flex w-4/5 h-full items-center justify-between space-x-2 p-4">
                    <a @click="scrollToTop">
                        <a-tooltip>
                            <template #title>穿越到顶部</template>
                            <arrow-up-outlined style="font-size: 30px;"/>
                        </a-tooltip>
                    </a>
                    <a @click="scrollToBottom">
                        <a-tooltip>
                            <template #title>穿越到底部</template>
                            <arrow-down-outlined style="font-size: 30px;"/>
                        </a-tooltip>
                    </a>
                    <a class="icon" @click="showModal">
                        <rest-filled style="font-size: 35px; color:cadetblue;" class="h-full"/>
                    </a>
                    <a-modal v-model:visible="visible" title="清空会话" @ok="onClear">
                        <a-alert message="Warning" description="确认要清空数据吗?" type="warning"/>
                    </a-modal>
                    <a-textarea
                        ref="messageInput"
                        v-model:value="search_string"
                        @pressEnter="onSubmit($event)"
                        :disabled="submitDisable"
                        placeholder="来说点什么吧...(Shift + Enter = 换行）"
                        :autoSize="{ minRows: 1, maxRows: 5 }"
                        :bordered="false"
                        size="large"
                        class="custom-textarea flex w-full overflow-y-hidden bg-slate-500 px-2 my-2 rounded-md text-white justify-center
                        focus:bg-white focus:text-slate-900 focus:border-blue-500 focus:ring-0"
                    />
                    <a-button class="h-35 w-35 border-none" @click="onSubmit" :loading="submitLoading" :ghost="true" size="large" type="primary">
                        <template #icon class="h-35 w-35 border-none">
                            <up-circle-filled style="font-size: 35px; color:cadetblue;" class="flex justify-center items-center"/>
                        </template>
                    </a-button>
                </div>
            </footer>
        </div>
    </a-layout-content>
</template>


<style scoped>
/* 滚动条 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
/* 外层轨道 */
::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 0;
}
/* 滑块 */
::-webkit-scrollbar-thumb {
  cursor: pointer;
  border-radius: 5px;
  background: rgba(0, 0, 0, 0.15);
  transition: color 0.2s ease;
}

textarea::placeholder {
    color: gray;
    font-size: 1em;
    font-style: italic;
}

</style>