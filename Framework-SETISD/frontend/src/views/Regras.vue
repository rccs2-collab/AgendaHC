<template>
  <div class="px-6 py-5 max-w-[1280px] space-y-6">
    <div v-if="carregando && !dados" class="space-y-3">
      <div v-for="n in 5" :key="n" class="h-12 rounded bg-line/70 animate-pulse"></div>
    </div>

    <template v-else-if="dados">
      <section class="rounded-lg bg-surface ring-1 ring-line overflow-hidden">
        <div class="px-5 pt-4 pb-3 border-b border-line">
          <h2 class="text-sm font-extrabold text-ink">Ordem dos critérios por unidade</h2>
          <p class="text-xs text-ink-muted mt-0.5">A fila aplica os critérios de cima para baixo. Cada alteração gera uma nova versão e fica registrada na auditoria.</p>
        </div>
        <div class="grid md:grid-cols-[16rem_1fr]">
          <ul class="border-r border-line bg-surface-sunken py-2 max-h-[26rem] overflow-y-auto">
            <li v-for="r in dados.regras" :key="r.unidade">
              <button
                type="button"
                @click="escolher(r)"
                :class="edicao?.unidade === r.unidade ? 'bg-surface text-ink font-bold ring-1 ring-line' : 'text-ink-muted hover:text-ink'"
                class="w-full flex items-baseline justify-between gap-2 px-4 py-2 text-left text-sm"
              >
                <span class="truncate">{{ r.unidade === '*' ? 'Padrão (todas)' : nomeUnidade(r.unidade) }}</span>
                <span class="tabular text-xs shrink-0">v{{ r.versao }}</span>
              </button>
            </li>
          </ul>

          <form v-if="edicao" @submit.prevent="salvar" class="p-5 space-y-4">
            <div class="flex flex-wrap items-baseline gap-x-3">
              <h3 class="text-base font-extrabold text-ink">{{ edicao.unidade === '*' ? 'Regra padrão' : nomeUnidade(edicao.unidade) }}</h3>
              <span class="text-xs text-ink-muted">
                versão {{ edicao.versao }}
                <template v-if="edicao.exemplo"> · regra de exemplo, a validar com a Central</template>
                <template v-else> · alterada por {{ edicao.atualizado_por }}</template>
              </span>
            </div>

            <ol class="space-y-1.5 max-w-lg">
              <li v-for="(c, i) in edicao.criterios" :key="c" class="flex items-center gap-3 rounded-md bg-surface ring-1 ring-line px-3 py-2">
                <span class="tabular w-5 text-sm font-extrabold text-ink">{{ i + 1 }}</span>
                <span class="flex-1 text-sm font-semibold text-ink">
                  {{ c === 'ESPERA_LIMITE' ? `Espera acima de ${edicao.espera_limite_dias} dias` : ROTULO_CRITERIO[c] }}
                </span>
                <button type="button" @click="mover(i, -1)" :disabled="i === 0" class="rounded p-1 text-ink-muted hover:bg-surface-sunken hover:text-ink disabled:opacity-30" :aria-label="`Subir ${ROTULO_CRITERIO[c]}`">
                  <ChevronUpIcon class="h-4 w-4" />
                </button>
                <button type="button" @click="mover(i, 1)" :disabled="i === edicao.criterios.length - 1" class="rounded p-1 text-ink-muted hover:bg-surface-sunken hover:text-ink disabled:opacity-30" :aria-label="`Descer ${ROTULO_CRITERIO[c]}`">
                  <ChevronDownIcon class="h-4 w-4" />
                </button>
              </li>
            </ol>

            <label class="flex items-center gap-3 text-sm text-ink">
              <span class="font-semibold">Limite de espera</span>
              <input v-model.number="edicao.espera_limite_dias" type="number" min="1" max="365" class="tabular w-20 rounded-md border border-line-strong bg-surface px-2 py-1.5 text-sm" />
              <span class="text-ink-muted">dias</span>
            </label>

            <p class="text-xs text-ink-muted max-w-lg">
              Data de retorno e distância do município entram como critérios quando o extrato do AGHU trouxer esses campos.
            </p>

            <div class="flex items-center gap-3">
              <button type="submit" :disabled="salvando || !alterada" class="rounded-md bg-acao px-4 py-2 text-sm font-bold text-white hover:bg-acao-hover disabled:bg-paper-disabled disabled:text-ink-muted">
                {{ salvando ? 'Salvando…' : 'Salvar nova versão' }}
              </button>
              <button v-if="alterada" type="button" @click="desfazer" class="text-sm font-semibold text-ink-muted hover:text-ink">Desfazer</button>
            </div>
          </form>
        </div>
      </section>

      <section class="rounded-lg bg-surface ring-1 ring-line overflow-hidden">
        <div class="px-5 pt-4 pb-3 flex items-baseline justify-between gap-3">
          <div>
            <h2 class="text-sm font-extrabold text-ink">Lista de prioridade</h2>
            <p class="text-xs text-ink-muted mt-0.5">Mantida pelas áreas solicitantes. Substitui as listas avulsas enviadas à Central.</p>
          </div>
        </div>
        <table class="w-full text-sm">
          <thead class="text-left text-xs font-bold text-ink-muted border-y border-line bg-surface-sunken whitespace-nowrap">
            <tr>
              <th scope="col" class="pl-5 pr-2 py-2">Prontuário</th>
              <th scope="col" class="px-2 py-2">Área</th>
              <th scope="col" class="px-2 py-2">Motivo</th>
              <th scope="col" class="px-2 py-2">Vale para</th>
              <th scope="col" class="px-2 py-2">Origem</th>
              <th scope="col" class="pl-2 pr-5 py-2"><span class="sr-only">Ações</span></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in dados.prioritarios" :key="p.id" class="border-b border-line last:border-0">
              <td class="tabular pl-5 pr-2 py-2.5 text-ink">{{ p.prontuario }}</td>
              <td class="px-2 py-2.5 font-bold text-lista-ink">{{ p.area }}</td>
              <td class="px-2 py-2.5 text-ink">{{ p.motivo }}</td>
              <td class="px-2 py-2.5 text-ink-muted">{{ p.unidade ? nomeUnidade(p.unidade) : 'Todas as unidades' }}</td>
              <td class="px-2 py-2.5 text-ink-muted">{{ p.exemplo ? 'Exemplo' : 'Incluído na fila' }}</td>
              <td class="pl-2 pr-5 py-2.5 text-right">
                <button type="button" @click="remover(p)" class="inline-flex items-center gap-1 rounded px-2 py-1 text-xs font-semibold text-ink-muted hover:bg-separar-bg hover:text-separar-ink">
                  <TrashIcon class="h-3.5 w-3.5" aria-hidden="true" /> Remover
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <section class="rounded-lg bg-surface ring-1 ring-line overflow-hidden">
        <div class="px-5 pt-4 pb-3">
          <h2 class="text-sm font-extrabold text-ink">Combinações de exames</h2>
          <p class="text-xs text-ink-muted mt-0.5">Regras de exemplo montadas a partir dos pares mais frequentes no extrato. A UDI precisa validar cada uma.</p>
        </div>
        <table class="w-full text-sm">
          <thead class="text-left text-xs font-bold text-ink-muted border-y border-line bg-surface-sunken whitespace-nowrap">
            <tr>
              <th scope="col" class="pl-5 pr-2 py-2">Exames</th>
              <th scope="col" class="px-2 py-2">Tipo</th>
              <th scope="col" class="pl-2 pr-5 py-2">Orientação ao marcador</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in dados.combinacoes" :key="c.id" class="border-b border-line last:border-0 align-top">
              <td class="pl-5 pr-2 py-2.5 text-ink">{{ exameCurto(c.exame_a) }} <span class="text-ink-muted">+</span> {{ exameCurto(c.exame_b) }}</td>
              <td class="px-2 py-2.5"><AlertaCombinacao :alerta="{ tipo: c.tipo, orientacao: c.orientacao, exames: [c.exame_a, c.exame_b] }" /></td>
              <td class="pl-2 pr-5 py-2.5 text-ink">{{ c.orientacao }}</td>
            </tr>
          </tbody>
        </table>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useToast } from 'vue-toastification';
import { ChevronUpIcon, ChevronDownIcon, TrashIcon } from '@heroicons/vue/20/solid';
import api from '../services/api';
import AlertaCombinacao from '../components/AlertaCombinacao.vue';
import { ROTULO_CRITERIO, exameCurto, nomeUnidade, type Prioridade, type Regra, type TipoCombinacao } from '../lib/agenda';

interface RespostaRegras {
  criterios_disponiveis: string[];
  regras: Regra[];
  prioritarios: Prioridade[];
  combinacoes: { id: number; exame_a: string; exame_b: string; tipo: TipoCombinacao; orientacao: string; exemplo: boolean }[];
}

const toast = useToast();
const dados = ref<RespostaRegras | null>(null);
const carregando = ref(false);
const salvando = ref(false);
const edicao = ref<Regra | null>(null);
const original = ref<Regra | null>(null);

const alterada = computed(() =>
  !!edicao.value && !!original.value &&
  (edicao.value.criterios.join() !== original.value.criterios.join() ||
    edicao.value.espera_limite_dias !== original.value.espera_limite_dias),
);

function escolher(r: Regra) {
  original.value = r;
  edicao.value = { ...r, criterios: [...r.criterios] };
}

function desfazer() {
  if (original.value) escolher(original.value);
}

function mover(i: number, delta: number) {
  if (!edicao.value) return;
  const lista = edicao.value.criterios;
  const j = i + delta;
  [lista[i], lista[j]] = [lista[j], lista[i]];
}

async function carregar(manterUnidade?: string) {
  carregando.value = true;
  try {
    dados.value = (await api.get<RespostaRegras>('/api/regras')).data;
    const alvo = dados.value.regras.find((r) => r.unidade === manterUnidade) ?? dados.value.regras[0];
    if (alvo) escolher(alvo);
  } finally {
    carregando.value = false;
  }
}

async function salvar() {
  if (!edicao.value) return;
  salvando.value = true;
  try {
    const { data } = await api.put('/api/regras', {
      unidade: edicao.value.unidade,
      criterios: edicao.value.criterios,
      espera_limite_dias: edicao.value.espera_limite_dias,
    });
    toast.success(`Regra salva como versão ${data.versao}. A fila já usa a nova ordem.`);
    await carregar(edicao.value.unidade);
  } catch (e: any) {
    toast.error(e?.response?.data?.detail ?? 'Não foi possível salvar a regra.');
  } finally {
    salvando.value = false;
  }
}

async function remover(p: Prioridade) {
  await api.delete(`/api/regras/prioritarios/${p.id}`);
  toast.success(`Prontuário ${p.prontuario} removido da lista de prioridade.`);
  await carregar(edicao.value?.unidade);
}

onMounted(() => carregar());
</script>
