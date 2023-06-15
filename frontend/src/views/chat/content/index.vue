<script setup lang="ts">
import { AliwangwangFilled, UpCircleFilled } from '@ant-design/icons-vue'
import { ref } from 'vue'

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
                        <div class="flex items-center justify-center mt-4 text-center text-neutral-300">
                            <AliwangwangFilled class="mr-2 text-3xl" />
                            <span>Aha~</span>
                        </div>
                    </div>
                </div>
            </main>
            <footer class="flex flex-row w-full max-h-36 dark:bg-[#101014] justify-center">
                <div class="flex w-4/5 h-full items-center justify-between space-x-2 p-4">
                    <a-textarea
                        v-model:value="search_string"
                        placeholder="来说点什么吧...(Shift + Enter = 换行）"
                        :autoSize="{ minRows: 1, maxRows: 5 }"
                        :bordered="false"
                        class="flex flex-1 h-auto overflow-y-hidden bg-slate-500 px-2 my-2 rounded-md text-white"
                    />
                    <a-button type="primary" class="h-auto" @click="onSearch">
                        <UpCircleFilled style="font-size: 25px; color:cadetblue;" class="pl-2 h-full"/>
                    </a-button>
                </div>
            </footer>
        </div>
    </a-layout-content>
</template>