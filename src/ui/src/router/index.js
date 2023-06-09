import { createRouter, createWebHistory } from 'vue-router'
import BookRoom from '../views/BookRoom.vue'
import Login from '../views/Login.vue'
import Main from '../views/Main.vue'
import Account from '../views/Account.vue'
import Admin from '../views/Admin.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: '/',
    //   name: 'home',
    //   component: HomeView
    // },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // },
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/main',
      name: 'Main',
      component: Main
    },
    {
      path: '/book',
      name: 'BookRoom',
      component: BookRoom
    },
    {
      path: '/account',
      name: 'Account',
      component: Account
    },
    {
      path: '/admin',
      name: 'Admin',
      component: Admin
    }
    
  ]
})

export default router
