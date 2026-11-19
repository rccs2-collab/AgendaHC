<template>
  <div class="px-6 py-5 max-w-[1280px] space-y-6">
    <p v-if="dados" class="text-xs text-ink-muted">{{ dados.fonte }} · indicadores calculados na leitura</p>

    <div v-if="carregando && !dados" class="space-y-3">
      <div v-for="n in 5" :key="n" class="h-12 rounded bg-line/70 animate-pulse"></div>
    </div>

    <template v-else-if="dados">
      <section class="rounded-lg bg-surface ring-1 ring-line p-5">
        <dl class="flex flex-wrap gap-x-10 gap-y-3">
          <div>
            <dt class="text-xs font-bold text-ink-muted">Exames pendentes</dt>
            <dd class="tabular text-3xl font-extrabold text-ink">{{ dados.totais.pendentes }}</dd>
          </div>
          <div>
            <dt class="text-xs font-bold text-ink-muted">Esperando há mais de 60 dias</dt>
            <dd class="tabular text-3xl font-extrabold text-espera-ink">
              {{ dados.totais.acima_60 }}
              <span class="text-base font-bold text-ink-muted">({{ pct(dados.totais.acima_60, dados.totais.pendentes) }})</span>
            </dd>
          </div>
          <div>
            <dt class="text-xs font-bold text-ink-muted">Resultados registrados no AgendaHC</dt>
            <dd class="flex flex-wrap items-baseline gap-x-3 text-sm text-ink pt-2">
              <span v-for="(n, s) in dados.status" :key="s"><strong class="tabular text-lg font-extrabold">{{ n }}</strong> {{ ROTULO_STATUS[s as StatusItem] }}</span>
              <span v-if="!Object.keys(dados.status).length" class="text-ink-muted">nenhum ainda</span>
            </dd>
          </div>
        </dl>

        <div class="mt-5">
          <p class="text-xs font-bold text-ink-muted mb-1.5">Tempo de espera dos pendentes</p>
          <BarraFaixas :faixas="dados.totais.faixas" alto />
          <ul class="mt-2 flex flex-wrap gap-x-5 gap-y-1 text-xs text-ink-muted">
            <li v-for="(f, i) in FAIXAS" :key="f.rotulo" class="flex items-center gap-1.5">
              <span class="h-2.5 w-2.5 rounded-sm" :style="{ background: f.cor }"></span>
              {{ f.rotulo }} <strong class="tabular text-ink">{{ dados.totais.faixas[i] }}</strong>
            </li>
          </ul>
        </div>
      </section>

      <section class="rounded-lg bg-surface ring-1 ring-line overflow-hidden">
        <h2 class="px-5 pt-4 pb-3 text-sm font-extrabold text-ink">Demanda por unidade</h2>
        <table class="w-full text-sm">
          <thead class="text-left text-xs font-bold text-ink-muted border-y border-line bg-surface-sunken whitespace-nowrap">
            <tr>
              <th scope="col" class="pl-5 pr-2 py-2">Unidade</th>
              <th scope="col" class="px-2 py-2 text-right">Pendentes</th>
              <th scope="col" class="px-2 py-2 text-right">Espera mediana</th>
              <th scope="col" class="px-2 py-2 text-right">Máxima</th>
              <th scope="col" class="px-2 py-2 text-right">&gt; 60 dias</th>
              <th scope="col" class="px-3 py-2 w-[22%]">Distribuição da espera</th>
              <th scope="col" class="pl-2 pr-5 py-2">Exames com mais pedidos</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in dados.unidades" :key="u.unidade" class="border-b border-line last:border-0 align-top">
              <th scope="row" class="pl-5 pr-2 py-3 text-left font-bold text-ink">{{ nomeUnidade(u.unidade) }}</th>
              <td class="tabular px-2 py-3 text-right font-bold text-ink">{{ u.pendentes }}</td>
              <td class="tabular px-2 py-3 text-right text-ink">{{ u.espera_mediana }} d</td>
              <td class="tabular px-2 py-3 text-right text-ink">{{ u.espera_maxima }} d</td>
              <td class="tabular px-2 py-3 text-right" :class="u.acima_60 ? 'font-bold text-espera-ink' : 'text-ink-muted'">{{ u.acima_60 }}</td>
              <td class="px-3 py-3.5"><BarraFaixas :faixas="u.faixas" /></td>
              <td class="pl-2 pr-5 py-3 text-xs text-ink-muted">
                <span v-for="(e, n) in u.principais_exames" :key="e.exame">
                  {{ exameCurto(e.exame) }} <strong class="tabular text-ink">{{ e.pendentes }}</strong><template v-if="n < u.principais_exames.length - 1"> · </template>
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <p class="text-xs text-ink-muted max-w-3xl">
        Indicadores que dependem de dados ainda ausentes no extrato do AGHU (agendados após a data de retorno,
        antecedência por município) aparecem aqui quando a TI incluir os campos.
      </p>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import api from '../services/api';
import BarraFaixas, { FAIXAS } from '../components/BarraFaixas.vue';
import { ROTULO_STATUS, exameCurto, nomeUnidade, type StatusItem } from '../lib/agenda';

interface Painel {
  fonte: string;
  totais: { pendentes: number; tratados: number; acima_60: number; faixas: number[] };
  status: Record<string, number>;
  unidades: {
    unidade: string; pendentes: number; tratados: number; espera_mediana: number; espera_maxima: number;
    acima_60: number; faixas: number[]; principais_exames: { exame: string; pendentes: number }[];
  }[];
}

const dados = ref<Painel | null>(null);
const carregando = ref(false);

function pct(parte: number, total: number) {
  return total ? `${Math.round((parte / total) * 100)}%` : '0%';
}

onMounted(async () => {
  carregando.value = true;
  try {
    dados.value = (await api.get<Painel>('/api/painel')).data;
  } finally {
    carregando.value = false;
  }
});
</script>
