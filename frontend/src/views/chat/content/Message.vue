<script setup lang="ts">
import { nextTick, computed, ref } from 'vue'
import { MehTwoTone, SketchCircleFilled, EditFilled, UndoOutlined, DiffFilled, CheckOutlined } from '@ant-design/icons-vue'
import MarkdownIt from 'markdown-it'
import mdKatex from '@traptitech/markdown-it-katex'
import mila from 'markdown-it-link-attributes'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import axios from 'axios'
import { message } from 'ant-design-vue'

interface Props {
  uId?: string
  mId?: number
  dateTime?: string
  text?: Text
  inversion?: number
  error?: number
  loading?: number
  asRawText?: number
  fetchData?: Function
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

function highlightBlock(str: string, lang?: string) {
  return `<pre class="code-block-wrapper">
  <div class="code-block-header">
    <span class="code-block-header__lang">${lang}</span>
    <span class="code-block-header__copy"">copy</span>
  </div><code class="hljs code-block-body ${lang}">${str}</code>
</pre>`
}

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
        if (copyButton.getAttribute('data-has-listener')) return;
        copyButton.addEventListener('click', copyCodeToClipboard);
        copyButton.setAttribute('data-has-listener', 'true');
      })
    })
  return renderedText.replace(/<p>|<\/p>/g, '')
})

function copyCodeToClipboard(event: Event) {
  const code = event.target.closest('.code-block-wrapper').querySelector('.code-block-body').textContent
  navigator.clipboard.writeText(code)
  .then(() => {
    message.success('代码复制成功!')
  })
  .catch(() => {
    console.log('复制失败，请重试。')
  })
}

const generateLoading = ref<boolean>(false)
const handleGenerate = () => {
  generateLoading.value = true
  axios.post(`http://127.0.0.1:8000/chat/${props.uId}/generate/${props.mId}`)
  .then(response => {
    generateLoading.value = false
    if (response.data.status == 'success') {
      props.fetchData(props.uId)
      message.success('生成成功!')
    }
  })
  .catch(err =>{
    generateLoading.value = false
  })
}

const isEditing = ref<boolean>(false)
const editText = ref<string>('')
const handleEdit = () => {
  isEditing.value = true
}
const doneEdit = () => {
  axios.post(`http://127.0.0.1:8000/chat/${props.uId}/update/${props.mId}`, { text: editText.value })
  .then(response => {
    if (response.data.status == 'success') {
      isEditing.value = false
      props.fetchData(props.uId)
      message.success('修改成功!')
    }
  })
  .catch(err =>{
    console.log(err)
  })
}

const handleCopy = () => {
  navigator.clipboard.writeText(props.text)
  .then(() => {
    message.success('复制成功!')
  })
  .catch(err => {
    message.error(`复制失败，请重试。${err}`);
  });
}

const deleteVisible = ref<boolean>(false)
const deleteShowModal = () => {
  deleteVisible.value = true
}

const handleDelete = () => {
  axios.post(`http://127.0.0.1:8000/chat/${props.uId}/delete/${props.mId}`)
  .then(response => {
    if (response.data.status == 'success') {
      deleteVisible.value = false
      props.fetchData(props.uId)
      message.success('删除成功!')
    }
  })
  console.log('delete')
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
        <div class="overflow-hidden text-sm group" :class="[inversion ? 'items-end' : 'items-start']">
          <div class="flex justify-between items-center" :class="[inversion ? 'flex-row-reverse' : '']">
            <p class="text-xs text-[#b4bbc4]" :class="[inversion ? 'text-right' : 'text-left']">
                {{ dateTime }}
            </p>
            <div class="flex flex-col opacity-0 group-hover:opacity-100">
                <a-dropdown-button
                    type="primary" 
                    :placement="inversion ? 'bottomLeft' : 'bottomRight'"
                >
                    <template #overlay >
                        <a-menu>
                            <a-menu-item key="1">
                                <a @click="handleCopy">复制</a>
                            </a-menu-item>
                            <a-menu-item key="2" >
                                <a @click="deleteShowModal">删除</a>
                                <a-modal v-model:visible="deleteVisible" title="删除记录" @ok="handleDelete" ok-text="确认" cancel-text="取消">
                                  <p>是否删除这条对话记录？</p>
                                </a-modal>
                            </a-menu-item>
                        </a-menu>
                    </template>
                    <template #icon><diff-filled style="font-size: 20px;"/></template>
                    <edit-filled v-if="inversion && !isEditing" @click="handleEdit" style="font-size: 18px;"/>
                    <check-outlined v-else-if="inversion && isEditing" @click="doneEdit" style="font-size: 18px;"/>
                    <a-spin v-else :spinning="generateLoading">
                    <undo-outlined @click="handleGenerate" :rotate="180" style="font-size: 18px;"/>
                    </a-spin>
                </a-dropdown-button>
              </div>
            </div>
            <div
                class="flex items-end gap-1 mt-2"
                :class="[inversion ? 'flex-row-reverse' : 'flex-row']"
            >
                <div class="text-black" :class="wrapClass">
                    <div v-if="!isEditing" ref="textRef" class="leading-relaxed break-words">
                        <div v-if="!inversion">
                            <div v-if="!asRawText" class="markdown-body" v-html="text" />
                            <div v-else class="whitespace-pre-wrap" v-text="text" />
                        </div>
                        <div v-else class="whitespace-pre-wrap" v-text="text" />
                        <template v-if="loading">
                            <span class="dark:text-white w-[4px] h-[20px] block animate-blink" />
                        </template>
                    </div>
                    <div v-else contenteditable="true" @input="editText = $event.target.innerText" class="whitespace-pre-wrap" style="box-sizing: border-box" v-text="text">
                    </div>
                </div>       
            </div>
        </div>
    </div>
</template>

<style lang="less">
@import url(./style.less);
</style>
