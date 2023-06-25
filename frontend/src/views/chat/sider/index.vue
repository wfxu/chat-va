<script setup lang="ts">
import { ref } from 'vue'
import { LeftCircleTwoTone, RightCircleTwoTone } from '@ant-design/icons-vue'
import List from './List.vue'
import Footer from './Footer.vue'

const siderCollapsed = ref(false)
function toggleSider() {
      siderCollapsed.value = !siderCollapsed.value;
    }
</script>

<template>
    <a-layout-sider
        :collapsed="siderCollapsed"
        collapsedWidth="0"
        collapsible="true"
        @collapse="toggleSider"
        :width="260"
        class="relative flex h-full min-w-0 bg-red-200 "
    >
        <template #trigger>
            <div class="absolute top-1/2 left-full ml-auto transform -translate-x-1/2 -translate-y-1/2 cursor-pointer">
                <right-circle-two-tone v-if="siderCollapsed" />
                <left-circle-two-tone v-else />
            </div>
        </template>
        <div class="flex flex-col h-full w-full" style="width: 260px" v-show="!siderCollapsed">
            <main class="flex flex-1 flex-col h-full bg-green-500">
                <div class="flex flex-1 h-full bg-slate-100 p-4">
                    <List />
                </div>
            </main>
            <Footer class="w-full bg-white" />
        </div>
    </a-layout-sider>
</template>

<style scoped>
</style>