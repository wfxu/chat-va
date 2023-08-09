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
        :collapsible="true"
        @collapse="toggleSider"
        :width="260"
        class="flex h-full min-w-0 bg-slate-500"
        zeroWidthTriggerStyle="background-color: transparent; width: 18px; height: 18px; left:100%; top: 50%; transform: translate(-50%, -100%);"
    >
        <template #trigger >
            <div style="display: flex; justify-content: center; align-items: center; ">
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