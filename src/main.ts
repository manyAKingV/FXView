import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import  "./components/index.css"
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
//@ts-ignore
createApp(App).use(store).use(router).mount('#app')
