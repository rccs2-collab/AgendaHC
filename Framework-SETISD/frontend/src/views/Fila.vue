<template>
  <div class="flex h-full min-h-0">
    <nav v-if="!compacto" class="hidden lg:block w-60 shrink-0 border-r border-line bg-paper-bg overflow-y-auto py-4" aria-label="Unidades">
      <p class="px-4 pb-2 text-xs font-bold text-ink-muted">Unidades</p>
      <ul class="space-y-px px-2">
        <li v-for="u in opcoesUnidade" :key="u.valor ?? 'todas'">
          <button
            type="button"
            @click="trocarUnidade(u.valor)"
            :aria-current="unidade === u.valor ? 'true' : undefined"
            :class="unidade === u.valor ? 'bg-surface text-ink shadow-[0_1px_2px_rgba(43,41,37,0.08)] ring-1 ring-line' : 'text-ink-muted hover:bg-surface/70 hover:text-ink'"
            class="w-full flex items-baseline justify-between gap-2 rounded-md px-2.5 py-2 text-left text-sm transition-colors"
          >
            <span class="font-semibold truncate">{{ u.rotulo }}</span>
            <span class="tabular text-xs text-ink-muted shrink-0">{{ u.exames }}</span>
          </button>
        </li>
      </ul>
      <p class="px-4 pt-4 text-[11px] leading-relaxed text-ink-muted">
        Exames pendentes por unidade. A fila agrupa os exames de cada paciente.
      </p>
    </nav>

    <section class="flex-1 min-w-0 flex flex-col">
      <div class="px-6 pt-4 pb-3 border-b border-line bg-paper-bg space-y-3">
        <div class="flex flex-wrap items-center gap-3">
          <label class="relative flex-1 min-w-[16rem] max-w-md">
            <span class="sr-only">Buscar paciente</span>
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-ink-muted" aria-hidden="true" />
            <input
              v-model="busca"
              type="search"
              placeholder="Buscar por nome ou prontuário"
              class="w-full rounded-md border border-line-strong bg-surface pl-9 pr-3 py-2 text-sm text-ink placeholder:text-ink-muted/80 focus:border-acao focus:outline-none focus:ring-2 focus:ring-acao/20"
            />
          </label>
          <select
            v-model="unidadeSelect"
            :class="compacto ? '' : 'lg:hidden'"
            class="rounded-md border border-line-strong bg-surface px-3 py-2 text-sm text-ink"
            aria-label="Unidade"
          >
            <option v-for="u in opcoesUnidade" :key="u.valor ?? 'todas'" :value="u.valor ?? ''">{{ u.rotulo }} ({{ u.exames }})</option>
          </select>
          <div class="ml-auto flex items-center gap-2 text-xs text-ink-muted">
            <span v-if="dados">{{ dados.fonte }} · lido {{ horaLeitura }}</span>
            <button
              type="button"
              @click="carregar()"
              :disabled="carregando"
              class="inline-flex items-center gap-1 rounded-md px-2 py-1 font-semibold text-acao hover:bg-acao-suave disabled:opacity-50"
            >
              <ArrowPathIcon :class="{ 'animate-spin': carregando }" class="h-4 w-4" aria-hidden="true" />
              Atualizar
            </button>
          </div>
        </div>

        <dl v-if="dados" :class="compacto ? 'gap-x-5' : 'gap-x-8'" class="flex flex-wrap items-baseline gap-y-1 text-sm">
          <div class="flex items-baseline gap-1.5">
            <dt class="sr-only">Pacientes na fila</dt>
            <dd class="tabular text-xl font-extrabold text-ink">{{ dados.resumo.pacientes }}</dd>
            <span class="text-ink-muted">pacientes · {{ dados.resumo.exames }} exames</span>
          </div>
          <div class="flex items-baseline gap-1.5">
            <dt class="sr-only">Na lista de prioridade</dt>
            <dd class="tabular text-xl font-extrabold text-lista-ink">{{ dados.resumo.prioritarios }}</dd>
            <span class="text-ink-muted">na lista de prioridade</span>
          </div>
          <div class="flex items-baseline gap-1.5">
            <dt class="sr-only">Com alerta de combinação</dt>
            <dd class="tabular text-xl font-extrabold text-separar-ink">{{ dados.resumo.com_alerta }}</dd>
            <span class="text-ink-muted">com alerta de combinação</span>
          </div>
          <div class="flex items-baseline gap-1.5">
            <dt class="sr-only">Espera mediana</dt>
            <dd class="tabular text-xl font-extrabold" :class="dados.resumo.espera_mediana > dados.regra.espera_limite_dias ? 'text-espera-ink' : 'text-ink'">{{ dados.resumo.espera_mediana }}</dd>
            <span class="text-ink-muted">dias de espera mediana<template v-if="!compacto"> · máx. {{ dados.resumo.espera_maxima }}</template></span>
          </div>
        </dl>

        <div v-if="dados" class="flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-ink-muted">
          <span class="font-bold text-ink">Ordenação</span>
          <template v-for="(c, i) in dados.regra.criterios" :key="c">
            <ChevronRightIcon v-if="i > 0" class="h-3.5 w-3.5" aria-hidden="true" />
            <span class="rounded bg-chegada-bg px-1.5 py-px font-semibold text-ink">
              {{ c === 'ESPERA_LIMITE' ? `Espera > ${dados.regra.espera_limite_dias} dias` : ROTULO_CRITERIO[c] }}
            </span>
          </template>
          <span>· regra {{ nomeUnidade(dados.regra.unidade) }} v{{ dados.regra.versao }}<template v-if="dados.regra.exemplo"> (exemplo)</template></span>
          <router-link to="/regras" class="font-semibold text-acao underline underline-offset-2 hover:text-acao-hover">Editar regra</router-link>
        </div>
      </div>

      <div class="flex-1 min-h-0 overflow-y-auto" ref="areaTabela">
        <div v-if="erro && dados" class="flex items-center gap-3 border-b border-line bg-separar-bg px-6 py-2 text-sm text-separar-ink" role="alert">
          <span class="font-bold">Não foi possível atualizar.</span>
          <span>Mostrando a última leitura. {{ erro }}</span>
          <button type="button" @click="carregar()" class="ml-auto font-bold underline underline-offset-2">Tentar de novo</button>
        </div>

        <div v-if="erro && !dados" class="m-6 rounded-md border border-separar-bg bg-surface p-4 text-sm" role="alert">
          <p class="font-bold text-separar-ink">Não foi possível carregar a fila.</p>
          <p class="text-ink-muted mt-1">{{ erro }}</p>
          <button type="button" @click="carregar()" class="mt-3 rounded-md bg-acao px-3 py-1.5 text-sm font-bold text-white hover:bg-acao-hover">Tentar de novo</button>
        </div>

        <table v-else class="w-full table-fixed text-sm">
          <thead class="sticky top-0 z-10 bg-paper-bg/95 backdrop-blur-sm text-left text-xs font-bold text-ink-muted">
            <tr class="border-b border-line">
              <th scope="col" class="w-[4.75rem] pl-6 pr-1 py-2">Posição</th>
              <th scope="col" class="w-[16rem] px-2 py-2">Paciente</th>
              <th scope="col" class="px-2 py-2">Exames pendentes</th>
              <th scope="col" class="w-20 px-2 py-2 text-right">Espera</th>
              <th scope="col" class="w-[11.5rem] px-2 py-2">Motivo da posição</th>
              <th v-if="!compacto" scope="col" class="w-[9.5rem] pl-2 pr-6 py-2">Combinação</th>
            </tr>
          </thead>
          <tbody v-if="carregando && !dados">
            <tr v-for="n in 10" :key="n" class="border-b border-line">
              <td :colspan="compacto ? 5 : 6" class="px-6 py-3">
                <div class="h-4 rounded bg-line/70 animate-pulse" :style="{ width: `${50 + (n * 37) % 45}%` }"></div>
              </td>
            </tr>
          </tbody>
          <TransitionGroup v-else tag="tbody" name="fila">
            <tr
              v-for="(g, idx) in gruposVisiveis"
              :key="g.chave"
              :data-chave="g.chave"
              :ref="(el) => registrarLinha(el, idx)"
              :tabindex="idx === indiceFoco ? 0 : -1"
              @focus="indiceFoco = idx"
              @click="selecionar(g, idx)"
              @keydown.enter.prevent="selecionar(g, idx, true)"
              @keydown.down.prevent="focarLinha(idx + 1)"
              @keydown.up.prevent="focarLinha(idx - 1)"
              @keydown.esc="fecharDetalhe"
              :class="selecionado?.chave === g.chave ? 'bg-acao-suave/70' : movidos[g.chave] ? 'bg-lista-bg/45 hover:bg-lista-bg/60' : 'bg-surface hover:bg-surface-sunken'"
              class="border-b border-line align-top cursor-pointer focus-visible:outline-2 focus-visible:outline-acao focus-visible:-outline-offset-2"
            >
              <td class="pl-6 pr-1 py-2.5">
                <div class="flex items-center gap-1.5">
                  <span class="tabular text-base font-extrabold text-ink">{{ g.posicao }}</span>
                  <span
                    v-if="movidos[g.chave]"
                    class="inline-flex items-center gap-0.5 rounded bg-lista-bg px-1 text-[11px] font-bold text-lista-ink"
                    :title="`Subiu ${movidos[g.chave]} posições`"
                  >
                    <ArrowUpIcon class="h-3 w-3" aria-hidden="true" />{{ movidos[g.chave] }}
                  </span>
                </div>
              </td>
              <td class="px-2 py-2.5">
                <p class="font-bold text-ink leading-snug break-words">{{ g.nome }}</p>
                <p class="tabular text-xs text-ink-muted">
                  <template v-if="g.sem_prontuario">Sem prontuário no extrato</template>
                  <template v-else>Pront. {{ g.prontuario }}</template>
                </p>
              </td>
              <td class="px-2 py-2.5">
                <ul class="space-y-1">
                  <li v-for="i in g.itens" :key="i.codigo_solicitacao + i.codigo_exame" class="flex items-baseline gap-2 min-w-0" :class="i.na_unidade ? 'text-ink' : 'text-ink-muted'">
                    <span class="leading-snug" :class="i.na_unidade ? 'font-semibold' : ''">{{ exameCurto(i.nome_exame) }}</span>
                    <span class="tabular text-xs text-ink-muted shrink-0">{{ dataCurta(i.data_solicitacao) }}</span>
                    <span v-if="!i.na_unidade" class="text-xs shrink-0">· {{ nomeUnidade(i.unidade) }}</span>
                    <StatusTag :status="i.status" class="shrink-0" />
                  </li>
                </ul>
              </td>
              <td class="px-2 py-2.5 text-right">
                <span class="tabular font-bold" :class="g.espera_dias > (dados?.regra.espera_limite_dias ?? 60) ? 'text-espera-ink' : 'text-ink'">{{ g.espera_dias }}</span>
                <span class="text-xs text-ink-muted"> dias</span>
              </td>
              <td class="px-2 py-2.5" :class="compacto ? 'pr-6' : ''">
                <div class="flex flex-col items-start gap-1">
                  <MotivoChip :motivo="g.motivo" />
                  <template v-if="compacto">
                    <AlertaCombinacao v-for="a in g.alertas" :key="a.exames.join()" :alerta="a" />
                  </template>
                </div>
              </td>
              <td v-if="!compacto" class="pl-2 pr-6 py-2.5">
                <div class="flex flex-col items-start gap-1">
                  <AlertaCombinacao v-for="a in g.alertas" :key="a.exames.join()" :alerta="a" />
                </div>
              </td>
            </tr>
          </TransitionGroup>
        </table>

        <div v-if="dados && !gruposFiltrados.length && busca.trim()" class="px-6 py-12 text-center">
          <p class="font-bold text-ink">Nenhum paciente encontrado para “{{ busca }}”.</p>
          <p class="mt-1 text-sm text-ink-muted">Busque pelo nome como aparece no AGHU ou pelo número do prontuário.</p>
          <button type="button" @click="busca = ''" class="mt-3 text-sm font-semibold text-acao underline underline-offset-2">Limpar busca</button>
        </div>
        <div v-else-if="dados && !gruposFiltrados.length" class="px-6 py-12 text-center">
          <p class="font-bold text-ink">Fila vazia {{ unidade ? `em ${nomeUnidade(unidade)}` : 'em todas as unidades' }}.</p>
          <p class="mt-1 text-sm text-ink-muted">Todas as solicitações lidas do AGHU já têm resultado registrado. Novas solicitações entram na próxima leitura.</p>
        </div>

        <div v-if="gruposFiltrados.length > limite" class="px-6 py-4 flex items-center gap-3 text-sm text-ink-muted">
          <span>Mostrando {{ limite }} de {{ gruposFiltrados.length }} pacientes</span>
          <button type="button" @click="limite += 60" class="rounded-md border border-line-strong bg-surface px-3 py-1.5 font-semibold text-ink hover:bg-surface-sunken">Mostrar mais 60</button>
        </div>
      </div>
    </section>

    <Transition name="painel">
      <aside
        v-if="selecionado"
        class="w-[25rem] shrink-0 border-l border-line bg-surface overflow-y-auto"
        aria-label="Detalhe do paciente"
        @keydown.esc="fecharDetalhe"
      >
        <DetalhePaciente
          :chave="selecionado.chave"
          :posicao="selecionado.posicao"
          :motivo="selecionado.motivo"
          :unidade="unidade"
          @fechar="fecharDetalhe"
          @alterado="aoAlterar"
        />
      </aside>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue';
import { useToast } from 'vue-toastification';
import { MagnifyingGlassIcon, ArrowPathIcon, ArrowUpIcon, ChevronRightIcon } from '@heroicons/vue/20/solid';
import api from '../services/api';
import MotivoChip from '../components/MotivoChip.vue';
import StatusTag from '../components/StatusTag.vue';
import AlertaCombinacao from '../components/AlertaCombinacao.vue';
import DetalhePaciente from '../components/DetalhePaciente.vue';
import { ROTULO_CRITERIO, dataCurta, exameCurto, nomeUnidade, type GrupoFila, type Regra, type Motivo } from '../lib/agenda';

interface RespostaFila {
  fonte: string;
  gerado_em: string;
  unidade: string | null;
  regra: Regra;
  resumo: { pacientes: number; exames: number; prioritarios: number; com_alerta: number; espera_mediana: number; espera_maxima: number };
  unidades: { unidade: string; exames: number; pacientes: number }[];
  total_exames: number;
  grupos: GrupoFila[];
}

const toast = useToast();
const dados = ref<RespostaFila | null>(null);
const carregando = ref(false);
const erro = ref('');
const unidade = ref<string | null>(null);
const busca = ref('');
const limite = ref(60);
const selecionado = ref<{ chave: string; posicao: number; motivo: Motivo } | null>(null);
const movidos = ref<Record<string, number>>({});
const linhas: (HTMLElement | null)[] = [];
const indiceFoco = ref(0);
const areaTabela = ref<HTMLElement | null>(null);

const opcoesUnidade = computed(() => {
  const lista = dados.value?.unidades ?? [];
  const total = lista.reduce((s, u) => s + u.exames, 0);
  return [
    { valor: null as string | null, rotulo: 'Todas as unidades', exames: total },
    ...lista.map((u) => ({ valor: u.unidade as string | null, rotulo: nomeUnidade(u.unidade), exames: u.exames })),
  ];
});

const unidadeSelect = computed({
  get: () => unidade.value ?? '',
  set: (v: string) => trocarUnidade(v || null),
});

const gruposFiltrados = computed(() => {
  const termo = busca.value.trim().toLowerCase();
  const grupos = dados.value?.grupos ?? [];
  if (!termo) return grupos;
  return grupos.filter((g) => g.nome.toLowerCase().includes(termo) || g.prontuario.includes(termo));
});

const gruposVisiveis = computed(() => gruposFiltrados.value.slice(0, limite.value));

const compacto = computed(() => !!selecionado.value);

const horaLeitura = computed(() => {
  if (!dados.value) return '';
  return `às ${new Date(dados.value.gerado_em).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}`;
});

function registrarLinha(el: unknown, idx: number) {
  linhas[idx] = (el as HTMLElement) ?? null;
}

function focarLinha(idx: number) {
  if (idx < 0 || idx >= gruposVisiveis.value.length) return;
  linhas[idx]?.focus();
}

function chavePosicoes() {
  return `agendahc:posicoes:${unidade.value ?? 'todas'}`;
}

function lerPosicoes(): Map<string, number> | null {
  try {
    const bruto = sessionStorage.getItem(chavePosicoes());
    return bruto ? new Map(Object.entries(JSON.parse(bruto) as Record<string, number>)) : null;
  } catch {
    return null;
  }
}

function salvarPosicoes(grupos: GrupoFila[]) {
  try {
    sessionStorage.setItem(chavePosicoes(), JSON.stringify(Object.fromEntries(grupos.map((g) => [g.chave, g.posicao]))));
  } catch {
    return;
  }
}

function quadro() {
  return new Promise<void>((resolve) => requestAnimationFrame(() => requestAnimationFrame(() => resolve())));
}

async function carregar(marcarMovimento = false) {
  carregando.value = true;
  erro.value = '';
  const emMemoria = dados.value ? new Map(dados.value.grupos.map((g) => [g.chave, g.posicao] as [string, number])) : null;
  const anteriores = emMemoria ?? lerPosicoes();
  try {
    const { data } = await api.get<RespostaFila>('/api/fila', { params: { unidade: unidade.value || undefined } });
    const novos: Record<string, number> = {};
    if (anteriores && (marcarMovimento || !emMemoria)) {
      for (const g of data.grupos) {
        const antes = anteriores.get(g.chave);
        if (antes && antes - g.posicao > 0) novos[g.chave] = antes - g.posicao;
      }
    }
    if (!emMemoria && anteriores && Object.keys(novos).length) {
      const ordemAntiga = [...data.grupos].sort(
        (a, b) => (anteriores.get(a.chave) ?? Number.MAX_SAFE_INTEGER) - (anteriores.get(b.chave) ?? Number.MAX_SAFE_INTEGER),
      );
      dados.value = { ...data, grupos: ordemAntiga };
      await nextTick();
      await quadro();
    }
    movidos.value = novos;
    salvarPosicoes(data.grupos);
    dados.value = data;
    if (selecionado.value) {
      const atual = data.grupos.find((g) => g.chave === selecionado.value?.chave);
      selecionado.value = atual ? { chave: atual.chave, posicao: atual.posicao, motivo: atual.motivo } : selecionado.value;
    }
  } catch (e: any) {
    erro.value = e?.response?.data?.detail ?? 'Verifique a conexão com o servidor e tente de novo.';
  } finally {
    carregando.value = false;
  }
}

function trocarUnidade(valor: string | null) {
  if (unidade.value === valor) return;
  unidade.value = valor;
  selecionado.value = null;
  dados.value = null;
  indiceFoco.value = 0;
  limite.value = 60;
  carregar();
}

async function selecionar(g: GrupoFila, idx: number, peloTeclado = false) {
  indiceFoco.value = idx;
  selecionado.value = { chave: g.chave, posicao: g.posicao, motivo: g.motivo };
  if (peloTeclado) {
    await nextTick();
    document.getElementById('detalhe-titulo')?.focus();
  }
}

async function fecharDetalhe() {
  const chave = selecionado.value?.chave;
  selecionado.value = null;
  await nextTick();
  if (chave) areaTabela.value?.querySelector<HTMLElement>(`[data-chave="${CSS.escape(chave)}"]`)?.focus();
}

async function aoAlterar(evento: { tipo: 'prioridade' | 'tratamento'; mensagem: string }) {
  const chave = selecionado.value?.chave;
  const antes = selecionado.value?.posicao;
  await carregar(evento.tipo === 'prioridade');
  const agora = dados.value?.grupos.find((g) => g.chave === chave);
  if (!agora) {
    toast.success(`${evento.mensagem} Paciente saiu da fila.`);
    selecionado.value = null;
    return;
  }
  if (antes && agora.posicao < antes) {
    toast.success(`${evento.mensagem} Subiu de ${antes}º para ${agora.posicao}º.`);
    await nextTick();
    const linha = areaTabela.value?.querySelector<HTMLElement>(`[data-chave="${CSS.escape(chave ?? '')}"]`);
    linha?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  } else {
    toast.success(evento.mensagem);
  }
}

watch(busca, () => {
  limite.value = 60;
});

onMounted(() => carregar());
</script>

<style scoped>
.fila-move {
  transition: transform 480ms cubic-bezier(0.16, 1, 0.3, 1);
}
.fila-enter-from,
.fila-leave-to {
  opacity: 0;
}
.fila-enter-active {
  transition: opacity 200ms ease-out;
}
.fila-leave-active {
  transition: opacity 160ms ease-out;
  position: absolute;
  width: 100%;
}
.painel-enter-from,
.painel-leave-to {
  opacity: 0;
  transform: translateX(12px);
}
.painel-enter-active,
.painel-leave-active {
  transition: opacity 180ms ease-out, transform 180ms ease-out;
}
@media (prefers-reduced-motion: reduce) {
  .fila-move,
  .fila-enter-active,
  .fila-leave-active,
  .painel-enter-active,
  .painel-leave-active {
    transition: none;
  }
}
</style>
