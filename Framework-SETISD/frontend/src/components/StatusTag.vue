<template>
  <span
    v-if="status !== 'PENDENTE'"
    :class="classes"
    class="inline-flex items-center gap-1 rounded px-1.5 py-px text-[11px] font-bold whitespace-nowrap"
  >
    <component :is="icone" class="h-3 w-3" aria-hidden="true" />
    {{ ROTULO_STATUS[status] }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { PhoneIcon, PhoneXMarkIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/vue/16/solid';
import { ROTULO_STATUS, type StatusItem } from '../lib/agenda';

const props = defineProps<{ status: StatusItem }>();

const classes = computed(() => ({
  PENDENTE: '',
  EM_CONTATO: 'bg-agrupar-bg text-agrupar-ink',
  SEM_CONTATO: 'bg-separar-bg text-separar-ink',
  AGENDADO: 'bg-ok-bg text-ok-ink',
  CANCELADO: 'bg-chegada-bg text-chegada-ink',
}[props.status]));

const icone = computed(() => ({
  PENDENTE: PhoneIcon,
  EM_CONTATO: PhoneIcon,
  SEM_CONTATO: PhoneXMarkIcon,
  AGENDADO: CheckCircleIcon,
  CANCELADO: XCircleIcon,
}[props.status]));
</script>
