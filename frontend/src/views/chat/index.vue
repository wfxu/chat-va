<script setup lang="ts">
import Sider from './sider/index.vue'
import Content from './content/index.vue'

</script>

<template>
    <div class="flex h-screen bg-slate-500 p-4">
        <a-layout
        breakpoint="lg"
        class="flex h-full w-full bg-yellow-100"
        >
            <Sider />
            <Content />
        </a-layout>
    </div>
</template>