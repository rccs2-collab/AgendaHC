<template>
  <span
    :class="classes"
    class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-bold whitespace-nowrap"
    :title="motivo.detalhe"
  >
    <component :is="icone" class="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
    {{ motivo.rotulo }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { ListBulletIcon, ClockIcon, ArrowDownTrayIcon } from '@heroicons/vue/20/solid';
import type { Motivo } from '../lib/agenda';

const props = defineProps<{ motivo: Motivo }>();

const classes = computed(() => ({
  LISTA: 'bg-lista-bg text-lista-ink',
  ESPERA: 'bg-espera-bg text-espera-ink',
  CHEGADA: 'bg-chegada-bg text-chegada-ink',
}[props.motivo.tipo]));

const icone = computed(() => ({
  LISTA: ListBulletIcon,
  ESPERA: ClockIcon,
  CHEGADA: ArrowDownTrayIcon,
}[props.motivo.tipo]));
</script>
