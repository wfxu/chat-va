<script setup lang="ts">
import { UserOutlined, SettingFilled } from '@ant-design/icons-vue'

</script>

<template>
    <footer class="flex items-center justify-between min-w-0 p-4 overflow-hidden border-t dark:border-neutral-800">
        <div class="flex-1 flex-shrink-0 overflow-hidden">
            <a-avatar :size="46" class="flex items-center justify-center">
                <template #icon><UserOutlined /></template>
            </a-avatar>
        </div>
        <div class="flex-1">
            wfxu
        </div>
        <setting-filled class="text-xl"/>
    </footer>
</template>