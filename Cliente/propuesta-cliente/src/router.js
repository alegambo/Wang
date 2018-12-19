import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/PropuestaForm.vue'
import Propuesta from './views/Propuesta.vue'
import PropuestaForm from './views/PropuestaForm.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    },
    {
      path: '/propuestas',
      name: 'propuestas',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/Propuesta.vue')
    },
    {
      path: '/propuesta/crear',
      name: 'propuesta-crear',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/PropuestaForm.vue')
    },
    {
      path: '/propuesta/:id/editar',
      name: 'propuesta-editar',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/PropuestaForm.vue')
    }
  ]
})
