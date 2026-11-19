<template>
  <div
    class="flex w-full overflow-hidden rounded-sm bg-line"
    :class="alto ? 'h-4' : 'h-2.5'"
    role="img"
    :aria-label="descricao"
  >
    <span
      v-for="(f, i) in FAIXAS"
      :key="f.rotulo"
      :style="{ width: `${largura(i)}%`, background: f.cor }"
      :title="`${f.rotulo}: ${faixas[i]}`"
      class="h-full first:rounded-l-sm last:rounded-r-sm"
    ></span>
  </div>
</template>

<script lang="ts">
export const FAIXAS = [
  { rotulo: 'até 30 dias', cor: '#c9d9d9' },
  { rotulo: '31 a 60 dias', cor: '#e9c46f' },
  { rotulo: '61 a 90 dias', cor: '#d98a2b' },
  { rotulo: 'mais de 90 dias', cor: '#a33811' },
];
</script>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{ faixas: number[]; alto?: boolean }>();

const total = computed(() => props.faixas.reduce((s, n) => s + n, 0));

function largura(i: number) {
  return total.value ? (props.faixas[i] / total.value) * 100 : 0;
}

const descricao = computed(() => FAIXAS.map((f, i) => `${f.rotulo}: ${props.faixas[i]}`).join(', '));
</script>
