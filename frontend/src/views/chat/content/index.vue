<script setup lang="ts">
import { AliwangwangFilled, UpCircleFilled } from '@ant-design/icons-vue'
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import Message from './Message.vue'

const route = useRoute()
const { uuid } = route.params as { uuid: string }
// const dataSources = [
//   { dateTime: '2022-01-01 10:00:00', text: 'Hello', inversion: false, error: false, loading: false },
//   { dateTime: '2022-01-01 11:00:00', text: 'Hi!', inversion: true, error: false, loading: false },
//   { dateTime: '2022-01-01 12:00:00', text: 'How are you?', inversion: false, error: true, loading: false },
//   { dateTime: '2022-01-01 10:00:00', text: uuid, inversion: true, error: false, loading: false },
//   // ...
// ];
const dataSources = ref(<typeof Message[]>[])
const fetchData = async (uuid: string | string[]) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/chat/${uuid}`)
    dataSources.value = response.data.messages
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
const onSearch = () => {
    console.log(search_string.value)
}

</script>

<template>
    <a-layout-content class="flex-grow h-full bg-slate-600">
        <div class="flex flex-col w-full h-full">
            <main class="flex-1 overflow-hidden">
                <div class="h-full overflow-hidden overflow-y-auto">
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
                                    :dateTime="item.dateTime"
                                    :text="item.text"
                                    :inversion="item.inversion"
                                    :error="item.error"
                                    :loading="item.loading"
                                />
                            </div>
                        </template>
                    </div>
                </div>
            </main>
            <footer class="flex flex-row w-full max-h-36 dark:bg-[#101014] justify-center">
                <div class="flex w-4/5 h-full items-center justify-between space-x-2 p-4">
                    <a-textarea
                        v-model:value="search_string"
                        placeholder="来说点什么吧...(Shift + Enter = 换行）"
                        :autoSize="{ minRows: 2, maxRows: 5 }"
                        :bordered="false"
                        size="large"
                        class="custom-textarea flex w-full overflow-y-hidden bg-slate-500 px-2 my-2 rounded-md text-white justify-center
                        focus:bg-slate-600 focus:text-white focus:border-blue-500 focus:outline-none focus:ring-0"
                    />
                    <a-button type="primary" class="h-auto w-auto" @click="onSearch">
                        <UpCircleFilled style="font-size: 25px; color:cadetblue;" class="pl-2 h-full"/>
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