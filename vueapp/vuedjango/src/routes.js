import Vue from 'vue'
import VueRouter from 'vue-router'
import Review from './views/Review.vue'
// import infiniteScroll from 'vue-infinite-scroll'

Vue.use(VueRouter)
// Vue.use(infiniteScroll)


export default new VueRouter({
    mode:'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'review',
            component:Review, 
        },
    ]
})