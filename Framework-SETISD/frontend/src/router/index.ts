import { createRouter, createWebHistory, NavigationGuardNext } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Configuracoes from '../views/Configuracoes.vue';

import Exemplos from '../views/Exemplos.vue';
import Pacientes from '../views/Pacientes.vue';
import Fila from '../views/Fila.vue';
import Painel from '../views/Painel.vue';
import Regras from '../views/Regras.vue';

const routes = [
  {
    path: '/',
    redirect: '/fila',
  },
  {
    path: '/inicio',
    name: 'Início',
    component: Home,
  },
  {
    path: '/fila',
    name: 'Fila',
    component: Fila,
    meta: { requiresAuth: true, titulo: 'Fila de marcação' },
  },
  {
    path: '/painel',
    name: 'Painel',
    component: Painel,
    meta: { requiresAuth: true, titulo: 'Painel da gestão' },
  },
  {
    path: '/regras',
    name: 'Regras',
    component: Regras,
    meta: { requiresAuth: true, titulo: 'Regras de prioridade' },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { layout: 'LoginLayout' },
  },
  {
    path: '/componentes',
    name: 'Componentes',
    component: Exemplos,
  },
  {
    path: '/exemplo',
    name: 'Exemplo',
    component: Pacientes,
    meta: { requiresAuth: true },
  },
  {
    path: '/configuracoes',
    name: 'Configuracoes',
    component: Configuracoes,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  linkActiveClass: '!bg-paper-active-link !text-white',
  linkExactActiveClass: '!bg-paper-active-link !text-white',
});

router.beforeEach((to, _from, next: NavigationGuardNext) => {
  // Pinia store must be used inside a function to ensure it's initialized
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;
