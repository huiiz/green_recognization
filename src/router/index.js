import { createRouter, createWebHashHistory } from 'vue-router'
import Select from '../views/Select.vue'
import Select2 from '../views/Select2.vue'
import Predict from '../views/Predict.vue'

const routes = [{
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
            title: '动态预测'
        }
    },
    {
        path: '/select2',
        name: 'Select2',
        component: Select2,
        meta: {
            title: '优化改进'
        }
    },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router