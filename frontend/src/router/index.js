import Vue from 'vue'
import Router from 'vue-router'
import AppIndex from '../components/home/AppIndex'
import Articles from '../components/jotter/Articles'
import LibraryIndex from '../components/library/LibraryIndex'
import Login from '../components/Login'
import Home from '../components/Home'
import AdminIndex from '../components/admin/AdminIndex'
import Register from '../components/Register'
import DashBoard from '../components/admin/dashboard/admin/index'
import ArticleDetails from '../components/jotter/ArticleDetails'
import Error404 from '../components/pages/Error404'

import single_gene_search from '../components/gene_phenotype/single_gene_search'
import single_phenotype_search from '../components/gene_phenotype/single_phenotype_search'
import multi_gene_search from '../components/gene_phenotype/multi_gene_search'
import multi_phenotype_search from '../components/gene_phenotype/multi_phenotype_search'
import gp_upload_file from '../components/gene_phenotype/gp_upload_file'
import gp_search_result from '../components/gene_phenotype/gp_search_result'
import gp_visualize from '../components/gene_phenotype/gp_visualize'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Default',
      redirect: '/home',
      component: Home
    },
    {
      // home页面并不需要被访问，只是作为其它组件的父组件
      path: '/home',
      name: 'Home',
      component: Home,
      redirect: '/index',
      children: [
        {
          path: '/index',
          name: 'AppIndex',
          component: AppIndex
        },
        {
          path: '/single_gene_search',
          name: 'single_gene_search',
          component: single_gene_search
        },
        {
          path: '/single_phenotype_search',
          name: 'single_phenotype_search',
          component: single_phenotype_search
        },
        {
          path: '/multi_gene_search',
          name: 'multi_gene_search',
          component: multi_gene_search
        },
        {
          path: '/multi_phenotype_search',
          name: 'multi_phenotype_search',
          component: multi_phenotype_search
        },
        {
          path: '/gp_upload_file',
          name: 'gp_upload_file',
          component: gp_upload_file
        },
        {
          path: '/gp_search_result',
          name: 'gp_search_result',
          component: gp_search_result
        },
        {
          path: '/gp_visualize',
          name: 'gp_visualize',
          component: gp_visualize
        },

        {
          path: '/jotter',
          name: 'Jotter',
          component: Articles
        },
        {
          path: '/jotter/article',
          name: 'Article',
          component: ArticleDetails
        },
        {
          path: '/library',
          name: 'Library',
          component: LibraryIndex
        }
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/admin',
      name: 'Admin',
      component: AdminIndex,
      // meta: {
      //   requireAuth: true
      // },
      children: [
        {
          path: '/admin/dashboard',
          name: 'Dashboard',
          component: DashBoard
          // meta: {
          //   requireAuth: true
          // }
        }
      ]
    },
    {
      path: '*',
      component: Error404
    }
  ]
})

// 用于创建默认路由
export const createRouter = routes => new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Default',
      redirect: '/home',
      component: Home
    },
    {
      // home页面并不需要被访问，只是作为其它组件的父组件
      path: '/home',
      name: 'Home',
      component: Home,
      redirect: '/index',
      children: [
        {
          path: '/index',
          name: 'AppIndex',
          component: AppIndex
        },
        {
          path: '/jotter',
          name: 'Jotter',
          component: Articles
        },
        {
          path: '/jotter/article',
          name: 'Article',
          component: ArticleDetails
        },
        {
          path: '/library',
          name: 'Library',
          component: LibraryIndex
        }
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/admin',
      name: 'Admin',
      component: AdminIndex,
      // meta: {
      //   requireAuth: true
      // },
      children: [
        {
          path: '/admin/dashboard',
          name: 'Dashboard',
          component: DashBoard
          // meta: {
          //   requireAuth: true
          // }
        }
      ]
    },
    {
      path: '*',
      component: Error404
    }
  ]
})
