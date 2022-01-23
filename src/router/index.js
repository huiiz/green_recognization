import { createRouter, createWebHashHistory } from 'vue-router'
import Select from '../views/Select.vue'
import Predict from '../views/Predict.vue'

const routes = [
  {
    path: '/',
    redirect: '/select'
  },
  {
    path: '/select',
    name: 'Select',
    component: Select,
    meta: {
      title: '绿化提取'
    }
  },
  {
    path: '/predict',
    name: 'Predict',
    component: Predict,
    meta: {
      title: '预测'
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
