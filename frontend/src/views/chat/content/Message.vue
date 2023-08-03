<script setup lang="ts">
import { nextTick, computed } from 'vue'
import { MehTwoTone, SketchCircleFilled, FrownFilled } from '@ant-design/icons-vue'
import MarkdownIt from 'markdown-it'
import mdKatex from '@traptitech/markdown-it-katex'
import mila from 'markdown-it-link-attributes'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

// const inversion = ref(false)
// const textRef = ref()
// const asRawText = inversion.value
// const loading = ref(false)
// const text = ref('文本')
// const error = ref(false)

interface Props {
  dateTime?: string
  text?: string
  inversion?: boolean
  error?: boolean
  loading?: boolean
  asRawText?: boolean
}

const props = defineProps<Props>()

const mdi = new MarkdownIt({
  html: true,
  linkify: true,
  highlight(code: string, language: string) {
    const validLang = !!(language && hljs.getLanguage(language))
    if (validLang) {
      const lang = language ?? ''
      return highlightBlock(hljs.highlight(code, { language: lang }).value, lang)
    }
    return highlightBlock(hljs.highlightAuto(code).value, '')
  },
})

mdi.use(mila, { attrs: { target: '_blank', rel: 'noopener' } })
mdi.use(mdKatex, { blockClass: 'katexmath-block rounded-md p-[10px]', errorColor: ' #cc0000' })

const wrapClass = computed(() => {
  return [
    'text-wrap',
    'min-w-[20px]',
    'rounded-md',
    'px-3 py-2',
    props.inversion ? 'bg-[#d2f9d1]' : 'bg-[#f4f6f8]',
    props.inversion ? 'dark:bg-[#a1dc95]' : 'dark:bg-[#1e1e20]',
    props.inversion ? 'message-request' : 'message-reply',
    { 'text-red-500': props.error },
  ]
})

const text = computed(() => {
  const value = props.text ?? '啥也没有哦'
  let renderedText = value;
  if (!props.asRawText)
    // return mdi.render(value)
    renderedText = mdi.render(value)
    // 在 nextTick 中添加事件监听器
    nextTick(() => {
      document.querySelectorAll('.code-block-header__copy').forEach((copyButton) => {
        copyButton.addEventListener('click', copyCodeToClipboard)
      })
    })
    return renderedText
  return value
})

function copyCodeToClipboard(event: Event) {
  const code = event.target.closest('.code-block-wrapper').querySelector('.code-block-body').textContent
  navigator.clipboard.writeText(code)
  // .then(() => {
  //   // 复制成功，显示提示信息
  //   alert('复制成功！')
  // })
  // .catch(() => {
  //   // 复制失败，显示提示信息
  //   alert('复制失败，请重试。')
  // })
}

const handleRegenerate = () => {
  console.log('regenerate')
}

const handleSelect = () => {
  console.log('select')
}

function highlightBlock(str: string, lang?: string) {
  return `<pre class="code-block-wrapper">
  <div class="code-block-header">
    <span class="code-block-header__lang">${lang}</span>
    <span class="code-block-header__copy"">copy</span>
  </div><code class="hljs code-block-body ${lang}">${str}</code>
</pre>`
}

</script>

<template>
    <div
        class="flex w-full mb-6 overflow-hidden"
        :class="[{ 'flex-row-reverse': inversion }]"
    >
        <div
            class="flex items-center justify-center flex-shrink-0 h-8 overflow-hidden rounded-full basis-8"
            :class="[inversion ? 'ml-2' : 'mr-2']"
        >
            <meh-two-tone v-if="inversion" :style="{fontSize: '40px', color: 'aliceblue'}"/>
            <sketch-circle-filled v-else :style="{fontSize: '45px', color: 'aliceblue'}"/>
        </div>
        <div class="overflow-hidden text-sm " :class="[inversion ? 'items-end' : 'items-start']">
            <p class="text-xs text-[#b4bbc4]" :class="[inversion ? 'text-right' : 'text-left']">
                {{ dateTime }}
            </p>
            <div
                class="flex items-end gap-1 mt-2"
                :class="[inversion ? 'flex-row-reverse' : 'flex-row']"
            >
                <div class="text-black" :class="wrapClass">
                    <div ref="textRef" class="leading-relaxed break-words">
                        <div v-if="!inversion">
                            <div v-if="!asRawText" class="markdown-body" v-html="text" />
                            <div v-else class="whitespace-pre-wrap" v-text="text" />
                        </div>
                        <div v-else class="whitespace-pre-wrap" v-text="text" />
                        <template v-if="loading">
                            <span class="dark:text-white w-[4px] h-[20px] block animate-blink" />
                        </template>
                    </div>
                </div>                        
                <div class="flex flex-col">
                    <a-button
                        v-if="!inversion"
                        class="mb-2 transition text-neutral-300 hover:text-neutral-800 dark:hover:text-neutral-300"
                        @click="handleRegenerate"
                    >
                        <frown-filled />
                    </a-button>
                    <a-dropdown-button
                        type="primary" 
                        :placement="inversion ? 'bottomLeft' : 'bottomRight'"
                        @click="handleSelect"
                        :getPopupContainer="(triggerNode: HTMLElement) => triggerNode.parentNode"
                    >
                        <template #overlay>
                            <a-menu>
                                <a-menu-item key="1">
                                    <a href="javascript:;">复制</a>
                                </a-menu-item>
                                <a-menu-item key="2" >
                                    <a href="javascript:;">删除</a>
                                </a-menu-item>
                            </a-menu>
                        </template>
                    </a-dropdown-button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="less">
@import url(./style.less);
</style>
