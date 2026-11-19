<template>
  <div class="relative h-screen overflow-hidden md:flex">
    <div class="bg-paper-sidebar text-gray-100 flex justify-between md:hidden shrink-0">
      <router-link to="/fila" class="block p-4 text-white font-extrabold">{{ SYSTEM_TITLE }}</router-link>
      <button @click="sidebarOpen = !sidebarOpen" class="p-4 focus:outline-none focus:bg-paper-active-link" aria-label="Abrir menu">
        <Bars3Icon class="h-6 w-6" />
      </button>
    </div>

    <aside
      :class="[
        sidebarOpen ? 'translate-x-0' : '-translate-x-full',
        isCollapsed ? 'md:w-[72px]' : 'md:w-56'
      ]"
      class="bg-paper-sidebar text-gray-200 pt-5 pb-2 px-2 absolute inset-y-0 left-0 transform md:relative md:translate-x-0 transition-all duration-200 ease-out z-20 h-full shrink-0 flex flex-col justify-between"
    >
      <div>
        <button
          type="button"
          @click="toggleSidebar"
          title="Recolher / expandir o menu"
          class="w-full text-left text-white flex items-center gap-3 px-3 mb-5 rounded hover:bg-paper-active-link/60 py-1.5 transition-colors"
        >
          <QueueListIcon class="h-7 w-7 shrink-0 text-[#a9c6c7]" />
          <span v-if="!isCollapsed" class="text-lg font-extrabold leading-tight select-none">
            {{ SYSTEM_TITLE }}
            <span class="block text-[11px] font-semibold text-gray-400 tracking-normal">Central de Marcação</span>
          </span>
        </button>

        <nav class="space-y-0.5" aria-label="Navegação principal">
          <router-link
            v-for="item in navegacao"
            :key="item.to"
            v-show="!item.auth || authStore.isAuthenticated"
            :to="item.to"
            :title="isCollapsed ? item.rotulo : ''"
            :class="[isCollapsed ? 'justify-center px-2' : 'px-3']"
            class="flex items-center gap-3 py-2 rounded text-sm font-semibold text-gray-300 transition-colors duration-150 hover:bg-paper-active-link/70 hover:text-white"
          >
            <component :is="item.icone" class="h-5 w-5 shrink-0" />
            <span v-if="!isCollapsed" class="truncate">{{ item.rotulo }}</span>
          </router-link>
        </nav>
      </div>

      <div v-if="!isCollapsed" class="px-3 pt-3 pb-1 border-t border-white/10 text-xs text-gray-400 mt-auto">
        <p class="font-semibold text-gray-200 truncate">{{ APP_NAME }}</p>
        <p class="text-[11px] text-gray-400 truncate">Versão {{ APP_VERSION }} | HC-UFPE</p>
      </div>
      <div v-else class="px-2 pt-3 pb-1 border-t border-white/10 text-[10px] text-center text-gray-400 mt-auto">
        v{{ APP_VERSION }}
      </div>
    </aside>

    <div class="flex-1 flex flex-col bg-paper-bg overflow-hidden h-full min-w-0">
      <header class="flex justify-between items-center px-6 h-14 bg-surface border-b border-line shrink-0">
        <h1 class="text-lg font-bold text-ink">{{ $route.meta.titulo || $route.name }}</h1>
        <div>
          <router-link v-if="!authStore.isAuthenticated" to="/login">
            <Button variant="primary">
              <template #icon>
                <ArrowRightOnRectangleIcon class="h-5 w-5" />
              </template>
              Entrar
            </Button>
          </router-link>
          <ProfileDropdown v-else />
        </div>
      </header>
      <main class="flex-1 min-h-0 overflow-y-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import {
  QueueListIcon,
  ChartBarIcon,
  AdjustmentsHorizontalIcon,
  Cog6ToothIcon,
  Bars3Icon,
  ArrowRightOnRectangleIcon,
} from '@heroicons/vue/24/outline';
import ProfileDropdown from '../components/ProfileDropdown.vue';
import Button from '../components/Button.vue';
import { useAuthStore } from '../stores/auth';
import { APP_VERSION, APP_NAME, SYSTEM_TITLE, fetchSystemConfig } from '../config/version';

const sidebarOpen = ref(false);
const isCollapsed = ref(false);

const route = useRoute();
const authStore = useAuthStore();

const navegacao = [
  { to: '/fila', rotulo: 'Fila de marcação', icone: QueueListIcon, auth: true },
  { to: '/painel', rotulo: 'Painel da gestão', icone: ChartBarIcon, auth: true },
  { to: '/regras', rotulo: 'Regras de prioridade', icone: AdjustmentsHorizontalIcon, auth: true },
  { to: '/configuracoes', rotulo: 'Configurações', icone: Cog6ToothIcon, auth: true },
];

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
};

watch(() => route.path, () => {
  sidebarOpen.value = false;
});

onMounted(fetchSystemConfig);
</script>
