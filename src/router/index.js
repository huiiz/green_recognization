import { createRouter, createWebHashHistory } from 'vue-router'
import Select from '../views/Select.vue'
import Select2 from '../views/Select2.vue'
import Predict from '../views/Predict.vue'

const projectName = '绿化先锋' //——基于深度学习的绿化信息提取与绿化率提升系统

const routes = [{
        path: '/',
        redirect: '/select'
    },
    {
        path: '/select',
        name: 'Select',
        component: Select,
        meta: {
            title: '绿化提取' + ' | ' + projectName
        }
    },
    {
        path: '/predict',
        name: 'Predict',
        component: Predict,
        meta: {
            title: '动态预测' + ' | ' + projectName
        }
    },
    {
        path: '/select2',
        name: 'Select2',
        component: Select2,
        meta: {
            title: '绿化规划' + ' | ' + projectName
        }
    },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router