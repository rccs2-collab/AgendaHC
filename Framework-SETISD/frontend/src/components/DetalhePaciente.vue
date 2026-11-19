<template>
  <div class="flex flex-col min-h-full">
    <div class="sticky top-0 z-10 bg-surface border-b border-line px-5 pt-4 pb-3">
      <div class="flex items-start justify-between gap-3">
        <div class="min-w-0">
          <h2 id="detalhe-titulo" tabindex="-1" class="text-base font-extrabold text-ink leading-snug rounded focus-visible:outline-2 focus-visible:outline-acao">{{ paciente?.nome ?? '…' }}</h2>
          <p class="tabular text-xs text-ink-muted">
            <template v-if="paciente?.prontuario">Prontuário {{ paciente.prontuario }}</template>
            <template v-else-if="paciente">Sem prontuário no extrato</template>
          </p>
        </div>
        <button type="button" @click="emit('fechar')" class="rounded-md p-1 text-ink-muted hover:bg-surface-sunken hover:text-ink" aria-label="Fechar detalhe">
          <XMarkIcon class="h-5 w-5" />
        </button>
      </div>
      <div class="mt-2 flex flex-wrap items-center gap-2 text-sm">
        <span class="tabular font-extrabold text-ink">{{ posicao }}º na fila</span>
        <MotivoChip :motivo="motivo" />
      </div>
      <p class="mt-1 text-xs text-ink-muted">{{ motivo.detalhe }}</p>
    </div>

    <div v-if="erroCarga && !paciente" class="p-5 text-sm" role="alert">
      <p class="font-bold text-separar-ink">Não foi possível abrir o paciente.</p>
      <p class="mt-1 text-ink-muted">{{ erroCarga }}</p>
      <button type="button" @click="carregar" class="mt-3 rounded-md bg-acao px-3 py-1.5 text-sm font-bold text-white hover:bg-acao-hover">Tentar de novo</button>
    </div>

    <div v-else-if="carregando && !paciente" class="p-5 space-y-3">
      <div v-for="n in 4" :key="n" class="h-10 rounded bg-line/70 animate-pulse"></div>
    </div>

    <div v-else-if="paciente" class="divide-y divide-line">
      <section v-if="paciente.alertas.length" class="px-5 py-4 space-y-2">
        <h3 class="text-xs font-bold text-ink-muted">Combinação de exames</h3>
        <div v-for="a in paciente.alertas" :key="a.exames.join()" class="text-sm">
          <AlertaCombinacao :alerta="a" />
          <p class="mt-1.5 text-ink">{{ a.orientacao }}</p>
          <p class="mt-1 text-xs text-ink-muted">{{ a.exames.map(exameCurto).join(' + ') }}<template v-if="a.exemplo"> · regra de exemplo</template></p>
        </div>
      </section>

      <section class="px-5 py-4">
        <h3 class="text-xs font-bold text-ink-muted mb-2">Exames do paciente</h3>
        <ul class="divide-y divide-line">
          <li v-for="i in paciente.itens" :key="i.codigo_solicitacao + i.codigo_exame" class="py-3 first:pt-1 last:pb-0">
            <div>
              <div class="flex items-start justify-between gap-2">
                <p class="font-bold text-ink text-sm leading-snug">{{ exameCurto(i.nome_exame) }}</p>
                <StatusTag :status="i.status" />
              </div>
              <p class="tabular mt-0.5 text-xs text-ink-muted">
                {{ nomeUnidade(i.unidade) }} · Solic. {{ i.codigo_solicitacao }} · {{ dataCompleta(i.data_solicitacao) }} · {{ i.espera_dias }} dias
              </p>
              <p v-if="i.status_info?.data_agendada" class="mt-1 text-xs font-semibold text-ok-ink">
                Agendado para {{ dataCompleta(i.status_info.data_agendada) }}
              </p>
              <p v-if="i.status_info?.observacao" class="mt-1 text-xs text-ink">“{{ i.status_info.observacao }}”</p>
              <button
                v-if="!finalizado(i.status) && aberto !== chaveItem(i)"
                type="button"
                @click="abrirRegistro(i)"
                class="mt-2 text-xs font-bold text-acao hover:text-acao-hover underline underline-offset-2"
              >
                Registrar resultado
              </button>
            </div>

            <form v-if="aberto === chaveItem(i)" @submit.prevent="registrar(i)" class="mt-3 space-y-3">
              <fieldset>
                <legend class="text-xs font-bold text-ink mb-1.5">Resultado</legend>
                <div class="grid grid-cols-2 gap-1.5">
                  <label
                    v-for="op in opcoesStatus"
                    :key="op.valor"
                    :class="form.status === op.valor ? 'bg-surface ring-2 ring-acao text-ink' : 'bg-surface ring-1 ring-line text-ink-muted hover:text-ink'"
                    class="flex items-center gap-2 rounded-md px-2.5 py-2 text-xs font-semibold cursor-pointer has-[:focus-visible]:ring-2 has-[:focus-visible]:ring-acao"
                  >
                    <input type="radio" class="sr-only" :value="op.valor" v-model="form.status" />
                    <component :is="op.icone" class="h-4 w-4 shrink-0" aria-hidden="true" />
                    {{ op.rotulo }}
                  </label>
                </div>
              </fieldset>
              <label v-if="form.status === 'AGENDADO'" class="block">
                <span class="text-xs font-bold text-ink">Data marcada no AGHU</span>
                <input v-model="form.data" type="date" required class="mt-1 block w-full rounded-md border border-line-strong bg-surface px-2.5 py-1.5 text-sm text-ink" />
              </label>
              <label class="block">
                <span class="text-xs font-bold text-ink">Observação <span class="font-normal text-ink-muted">(opcional)</span></span>
                <textarea v-model="form.observacao" rows="2" class="mt-1 block w-full rounded-md border border-line-strong bg-surface px-2.5 py-1.5 text-sm text-ink" placeholder="Ex.: paciente pediu horário pela manhã"></textarea>
              </label>
              <p v-if="erroForm" class="text-xs font-semibold text-separar-ink" role="alert">{{ erroForm }}</p>
              <div class="flex items-center gap-2">
                <button type="submit" :disabled="salvando || !form.status" class="rounded-md bg-acao px-3 py-1.5 text-sm font-bold text-white hover:bg-acao-hover disabled:bg-paper-disabled disabled:text-ink-muted">
                  {{ salvando ? 'Registrando…' : 'Registrar' }}
                </button>
                <button type="button" @click="aberto = null" class="rounded-md px-3 py-1.5 text-sm font-semibold text-ink-muted hover:text-ink">Cancelar</button>
              </div>
              <p class="text-[11px] text-ink-muted">A marcação é feita no AGHU. Aqui fica só o registro do resultado.</p>
            </form>
          </li>
        </ul>
      </section>

      <section class="px-5 py-4">
        <h3 class="text-xs font-bold text-ink-muted mb-2">Lista de prioridade</h3>
        <ul v-if="paciente.prioridades.length" class="space-y-1.5 text-sm">
          <li v-for="p in paciente.prioridades" :key="p.id" class="flex items-baseline gap-2">
            <span class="font-bold text-lista-ink">{{ p.area }}</span>
            <span class="text-ink">{{ p.motivo }}</span>
            <span v-if="p.exemplo" class="text-xs text-ink-muted">· exemplo</span>
          </li>
        </ul>
        <template v-else-if="paciente.prontuario">
          <button
            v-if="!formPrioridade.aberto"
            type="button"
            @click="formPrioridade.aberto = true"
            class="inline-flex items-center gap-1.5 rounded-md ring-1 ring-line-strong bg-surface px-3 py-1.5 text-sm font-semibold text-ink hover:bg-surface-sunken"
          >
            <UserPlusIcon class="h-4 w-4 text-acao" aria-hidden="true" />
            Incluir na lista de prioridade
          </button>
          <form v-else @submit.prevent="incluirPrioridade" class="space-y-2.5">
            <label class="block">
              <span class="text-xs font-bold text-ink">Área responsável</span>
              <select v-model="formPrioridade.area" class="mt-1 block w-full rounded-md border border-line-strong bg-surface px-2.5 py-1.5 text-sm text-ink">
                <option>Nefrologia</option>
                <option>Oncologia</option>
                <option>Cardiologia</option>
                <option>Outra</option>
              </select>
            </label>
            <label class="block">
              <span class="text-xs font-bold text-ink">Motivo</span>
              <input v-model="formPrioridade.motivo" required type="text" placeholder="Ex.: paciente em hemodiálise" class="mt-1 block w-full rounded-md border border-line-strong bg-surface px-2.5 py-1.5 text-sm text-ink" />
            </label>
            <p v-if="erroPrioridade" class="text-xs font-semibold text-separar-ink" role="alert">{{ erroPrioridade }}</p>
            <div class="flex items-center gap-2">
              <button type="submit" :disabled="salvando" class="rounded-md bg-acao px-3 py-1.5 text-sm font-bold text-white hover:bg-acao-hover disabled:bg-paper-disabled">Incluir</button>
              <button type="button" @click="formPrioridade.aberto = false" class="rounded-md px-3 py-1.5 text-sm font-semibold text-ink-muted hover:text-ink">Cancelar</button>
            </div>
          </form>
        </template>
        <p v-else class="text-sm text-ink-muted">Sem prontuário no extrato: não é possível incluir na lista.</p>
      </section>

      <section class="px-5 py-4">
        <div class="flex gap-2 text-xs text-ink-muted">
          <InformationCircleIcon class="h-4 w-4 shrink-0 text-ink-muted" aria-hidden="true" />
          <p>Sem dado no extrato do AGHU: {{ paciente.dados_ausentes.join(', ') }}. Esses critérios entram na ordenação quando a TI incluir os campos.</p>
        </div>
      </section>

      <section class="px-5 py-4">
        <h3 class="text-xs font-bold text-ink-muted mb-2">Histórico</h3>
        <ol v-if="paciente.historico.length" class="space-y-2 text-sm">
          <li v-for="(h, n) in paciente.historico" :key="n" class="flex gap-2">
            <span class="tabular text-xs text-ink-muted w-24 shrink-0 pt-0.5">{{ dataHora(h.criado_em) }}</span>
            <span class="text-ink"><strong class="font-bold">{{ ROTULO_STATUS[h.status as StatusItem] }}</strong> · {{ exameDoCodigo(h.codigo_exame) }} · {{ h.usuario }}</span>
          </li>
        </ol>
        <p v-else class="text-sm text-ink-muted">Nenhum registro ainda. Cada resultado registrado aparece aqui, com quem registrou e quando.</p>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue';
import { XMarkIcon, UserPlusIcon, InformationCircleIcon } from '@heroicons/vue/20/solid';
import { PhoneIcon, PhoneXMarkIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/vue/20/solid';
import api from '../services/api';
import MotivoChip from './MotivoChip.vue';
import StatusTag from './StatusTag.vue';
import AlertaCombinacao from './AlertaCombinacao.vue';
import {
  ROTULO_STATUS, dataCompleta, dataHora, exameCurto, nomeUnidade,
  type Alerta, type ItemFila, type Motivo, type Prioridade, type StatusItem,
} from '../lib/agenda';

interface DetalheResposta {
  chave: string;
  prontuario: string;
  nome: string;
  itens: ItemFila[];
  prioridades: Prioridade[];
  alertas: Alerta[];
  historico: { codigo_solicitacao: string; codigo_exame: string; status: string; usuario: string; criado_em: string }[];
  dados_ausentes: string[];
}

const props = defineProps<{ chave: string; posicao: number; motivo: Motivo; unidade: string | null }>();
const emit = defineEmits<{
  (e: 'fechar'): void;
  (e: 'alterado', evento: { tipo: 'prioridade' | 'tratamento'; mensagem: string }): void;
}>();

const paciente = ref<DetalheResposta | null>(null);
const carregando = ref(false);
const salvando = ref(false);
const aberto = ref<string | null>(null);
const erroForm = ref('');
const erroCarga = ref('');
const erroPrioridade = ref('');
const form = reactive<{ status: StatusItem | ''; data: string; observacao: string }>({ status: '', data: '', observacao: '' });
const formPrioridade = reactive({ aberto: false, area: 'Nefrologia', motivo: '' });

const opcoesStatus = [
  { valor: 'EM_CONTATO', rotulo: 'Em contato', icone: PhoneIcon },
  { valor: 'SEM_CONTATO', rotulo: 'Sem contato', icone: PhoneXMarkIcon },
  { valor: 'AGENDADO', rotulo: 'Agendado no AGHU', icone: CheckCircleIcon },
  { valor: 'CANCELADO', rotulo: 'Cancelado', icone: XCircleIcon },
] as const;

function chaveItem(i: ItemFila) {
  return `${i.codigo_solicitacao}:${i.codigo_exame}`;
}

function finalizado(status: StatusItem) {
  return status === 'AGENDADO' || status === 'CANCELADO';
}

function exameDoCodigo(codigo: string) {
  const item = paciente.value?.itens.find((i) => i.codigo_exame === codigo);
  return item ? exameCurto(item.nome_exame) : codigo;
}

function abrirRegistro(i: ItemFila) {
  aberto.value = chaveItem(i);
  form.status = '';
  form.data = '';
  form.observacao = '';
  erroForm.value = '';
}

async function carregar() {
  carregando.value = true;
  erroCarga.value = '';
  try {
    const { data } = await api.get<DetalheResposta>(`/api/fila/pacientes/${encodeURIComponent(props.chave)}`);
    paciente.value = data;
  } catch (e: any) {
    erroCarga.value = e?.response?.data?.detail ?? 'Verifique a conexão e tente de novo.';
  } finally {
    carregando.value = false;
  }
}

async function registrar(i: ItemFila) {
  if (!form.status) return;
  if (form.status === 'AGENDADO' && !form.data) {
    erroForm.value = 'Informe a data marcada no AGHU.';
    return;
  }
  salvando.value = true;
  erroForm.value = '';
  try {
    await api.post('/api/fila/tratamentos', {
      codigo_solicitacao: i.codigo_solicitacao,
      codigo_exame: i.codigo_exame,
      status: form.status,
      data_agendada: form.status === 'AGENDADO' ? form.data : null,
      observacao: form.observacao || null,
    });
    aberto.value = null;
    await carregar();
    emit('alterado', { tipo: 'tratamento', mensagem: `${exameCurto(i.nome_exame)}: ${ROTULO_STATUS[form.status as StatusItem]}.` });
  } catch (e: any) {
    erroForm.value = e?.response?.data?.detail ?? 'Não foi possível registrar. Tente de novo.';
  } finally {
    salvando.value = false;
  }
}

async function incluirPrioridade() {
  if (!paciente.value) return;
  salvando.value = true;
  erroPrioridade.value = '';
  try {
    const unidadeDoPaciente = props.unidade ?? null;
    await api.post('/api/regras/prioritarios', {
      prontuario: paciente.value.prontuario,
      area: formPrioridade.area,
      motivo: formPrioridade.motivo,
      unidade: unidadeDoPaciente,
    });
    formPrioridade.aberto = false;
    formPrioridade.motivo = '';
    await carregar();
    emit('alterado', { tipo: 'prioridade', mensagem: `Incluído na lista de prioridade (${formPrioridade.area}).` });
  } catch (e: any) {
    erroPrioridade.value = e?.response?.data?.detail ?? 'Não foi possível incluir. Tente de novo.';
  } finally {
    salvando.value = false;
  }
}

watch(() => props.chave, () => {
  paciente.value = null;
  aberto.value = null;
  formPrioridade.aberto = false;
  carregar();
}, { immediate: true });
</script>
