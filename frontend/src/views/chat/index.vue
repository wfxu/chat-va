<script setup lang="ts">
import Sider from './sider/index.vue'

</script>

<template>
    <div class="flex h-screen bg-slate-500 p-4">
        <a-layout
        breakpoint="lg"
        class="flex h-full w-full bg-yellow-100"
        >
            <Sider />
            <router-view v-slot="{ Component, route }">
                <component :is="Component" :key="route.fullPath" />
            </router-view>
        </a-layout>
    </div>
</template>