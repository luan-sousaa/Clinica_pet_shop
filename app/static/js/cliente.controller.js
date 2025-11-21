/**
 * Controller para a página Cliente (cliente.html)
 * Gerencia visualização de dados do pet, vacinas, prescrições e agendamentos
 */

class ClienteController {
    constructor() {
        this.petId = null;
        this.petData = null;
    }

    /**
     * Inicializar o controller
     */
    init() {
        // Verificar autenticação
        if (!Auth.requireAuth()) {
            return;
        }

        this.petId = Auth.getPetId() || 1; // Default para 1 se não houver
        
        this.setupEventListeners();
        this.loadPetData();
        this.loadVacinas();
        this.loadConsultas();
        this.loadPrescricoes();
        this.loadAgendamentos();
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Botão de logout
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                if (confirm('Deseja realmente sair?')) {
                    Auth.logout();
                }
            });
        }

        // Checkboxes de agenda
        const checkboxes = document.querySelectorAll('.agenda-item input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => this.handleCheckboxChange(e));
        });
    }

    /**
     * Carregar dados do pet
     */
    async loadPetData() {
        try {
            const response = await api.getDadosPet();
            
            if (response.success) {
                this.petData = response.data;
                this.renderPetInfo();
                this.renderAgenda(response.data.servicos_agendados || []);
            } else {
                Utils.showError('Erro ao carregar dados do pet');
            }
        } catch (error) {
            Utils.showError(CONFIG.MESSAGES.ERROR_NETWORK);
        }
    }

    /**
     * Renderizar informações do pet
     */
    renderPetInfo() {
        const data = this.petData;
        
        // Atualizar nome do pet
        const petHeader = document.querySelector('.pet-header h1');
        if (petHeader) {
            petHeader.textContent = data.nome_pet || 'Nome do Pet';
        }

        // Formatar data de nascimento
        let dataNascimento = 'N/A';
        if (data.datanascimento) {
            dataNascimento = Utils.formatDate(data.datanascimento);
        } else if (data.idade) {
            dataNascimento = `${Math.floor(data.idade)} anos`;
        }

        // Atualizar informações
        const infoParagraphs = document.querySelectorAll('.pet-info p');
        if (infoParagraphs.length >= 4) {
            infoParagraphs[0].innerHTML = `<strong>Data de nascimento:</strong> ${dataNascimento}`;
            infoParagraphs[1].innerHTML = `<strong>Raça:</strong> ${data.raca_pet || 'N/A'}`;
            infoParagraphs[2].innerHTML = `<strong>Tutor:</strong> ${Auth.getUser()?.nome || 'N/A'}`;
            infoParagraphs[3].innerHTML = `<strong>Observações:</strong> ${data.observacoes_pet || 'Nenhuma'}`;
        }
    }

    /**
     * Renderizar agenda
     */
    renderAgenda(servicos) {
        const agendaContainer = document.querySelector('.agenda-box');
        
        if (!servicos || servicos.length === 0) {
            return; // Manter os itens de exemplo do HTML
        }

        // Limpar itens existentes (exceto o título)
        const items = agendaContainer.querySelectorAll('.agenda-item');
        items.forEach(item => item.remove());

        // Adicionar novos itens
        servicos.forEach((servico, index) => {
            const item = document.createElement('div');
            item.className = 'agenda-item';
            item.innerHTML = `
                <input type="checkbox" id="servico${index}">
                <label for="servico${index}">${servico.servico} - ${Utils.formatDate(servico.data)}</label>
            `;
            agendaContainer.appendChild(item);
        });
    }

    /**
     * Carregar histórico de vacinas
     */
    async loadVacinas() {
        try {
            const response = await api.getHistoricoVacinas(this.petId);
            
            if (response.success) {
                this.renderVacinas(response.data.vacinas || []);
            } else {
                console.error('Erro ao carregar vacinas');
            }
        } catch (error) {
            console.error('Erro de rede ao carregar vacinas');
        }
    }

    /**
     * Renderizar tabela de vacinas
     */
    renderVacinas(vacinas) {
        const tbody = document.querySelector('.vacina-table tbody');
        
        if (!tbody) return;

        if (vacinas.length === 0) {
            return; // Manter linhas vazias do HTML
        }

        // Limpar tbody
        tbody.innerHTML = '';

        // Adicionar vacinas
        vacinas.forEach(vacina => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${Utils.formatDate(vacina.data_aplicacao)}</td>
                <td>${vacina.nome_vacina}</td>
                <td>${vacina.proxima_dose ? Utils.formatDate(vacina.proxima_dose) : 'Dose única'}</td>
            `;
            tbody.appendChild(row);
        });
    }

    /**
     * Carregar consultas
     */
    async loadConsultas() {
        try {
            const response = await api.getConsultasPet(this.petId);
            
            if (response.success) {
                this.renderConsultas(response.data.consultas || []);
            } else {
                console.error('Erro ao carregar consultas');
            }
        } catch (error) {
            console.error('Erro de rede ao carregar consultas');
        }
    }

    /**
     * Renderizar consultas
     */
    renderConsultas(consultas) {
        const container = document.getElementById('consultas-lista');
        
        if (!container) return;

        if (consultas.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #999;">Nenhuma consulta registrada ainda</p>';
            return;
        }

        container.innerHTML = consultas.map(consulta => `
            <div class="consulta-card" style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-left: 4px solid #6B456C;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                    <div>
                        <h3 style="color: #6B456C; margin: 0 0 5px 0;">${consulta.motivo || 'Consulta'}</h3>
                        <p style="color: #666; font-size: 0.9em; margin: 0;">${Utils.formatDate(consulta.data_consulta)} - ${consulta.hora_consulta}</p>
                    </div>
                    <span style="background-color: ${consulta.status === 'agendada' ? '#2196F3' : '#999'}; color: white; padding: 5px 10px; border-radius: 15px; font-size: 0.8em;">${consulta.status}</span>
                </div>
                <div style="margin-top: 15px;">
                    <p style="margin: 5px 0;"><strong>Veterinário:</strong> ${consulta.veterinario || 'N/A'}</p>
                    ${consulta.observacoes ? `<p style="margin: 5px 0;"><strong>Observações:</strong> ${consulta.observacoes}</p>` : ''}
                </div>
            </div>
        `).join('');
    }

    /**
     * Carregar prescrições médicas
     */
    async loadPrescricoes() {
        try {
            const response = await api.getPrescricoesPet(this.petId);
            
            if (response.success) {
                this.renderPrescricoes(response.data.prescricoes || []);
            } else {
                console.error('Erro ao carregar prescrições');
            }
        } catch (error) {
            console.error('Erro de rede ao carregar prescrições');
        }
    }

    /**
     * Renderizar prescrições médicas
     */
    renderPrescricoes(prescricoes) {
        const container = document.getElementById('prescricoes-lista');
        
        if (!container) return;

        if (prescricoes.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #999;">Nenhuma prescrição registrada ainda</p>';
            return;
        }

        container.innerHTML = prescricoes.map(prescricao => `
            <div class="prescricao-card" style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-left: 4px solid #6B456C;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                    <div>
                        <h3 style="color: #6B456C; margin: 0 0 5px 0;">${prescricao.diagnostico}</h3>
                        <p style="color: #666; font-size: 0.9em; margin: 0;">Dr(a). ${prescricao.veterinario} - ${Utils.formatDate(prescricao.data_consulta)}</p>
                    </div>
                    <span style="background-color: ${prescricao.status === 'ativa' ? '#4CAF50' : '#999'}; color: white; padding: 5px 10px; border-radius: 15px; font-size: 0.8em;">${prescricao.status}</span>
                </div>
                <div style="margin-top: 15px;">
                    <p style="margin: 5px 0;"><strong>Medicamentos:</strong> ${prescricao.medicamentos_count || 0}</p>
                    <button onclick="clienteController.verDetalhesPrescricao(${prescricao.id})" style="margin-top: 10px; padding: 8px 15px; background-color: #6B456C; color: white; border: none; border-radius: 5px; cursor: pointer; font-family: 'Lexend', sans-serif;">Ver Detalhes</button>
                </div>
            </div>
        `).join('');
    }

    /**
     * Ver detalhes de uma prescrição
     */
    async verDetalhesPrescricao(prescricaoId) {
        try {
            const response = await api.getDetalhesPrescricao(prescricaoId);
            
            if (response.success) {
                this.mostrarModalPrescricao(response.data);
            } else {
                Utils.showError('Erro ao carregar detalhes da prescrição');
            }
        } catch (error) {
            Utils.showError(CONFIG.MESSAGES.ERROR_NETWORK);
        }
    }

    /**
     * Mostrar modal com detalhes da prescrição
     */
    mostrarModalPrescricao(prescricao) {
        const medicamentosHtml = prescricao.medicamentos.map(med => `
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                <h4 style="color: #6B456C; margin: 0 0 10px 0;">${med.nome}</h4>
                <p style="margin: 5px 0;"><strong>Dosagem:</strong> ${med.dosagem}</p>
                <p style="margin: 5px 0;"><strong>Frequência:</strong> ${med.frequencia}</p>
                <p style="margin: 5px 0;"><strong>Duração:</strong> ${med.duracao}</p>
                ${med.observacoes ? `<p style="margin: 5px 0;"><strong>Observações:</strong> ${med.observacoes}</p>` : ''}
            </div>
        `).join('');

        const modalHtml = `
            <div id="modal-prescricao-detalhes" style="display: flex; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); z-index: 1000; justify-content: center; align-items: center;">
                <div style="background-color: white; padding: 30px; border-radius: 10px; max-width: 700px; width: 90%; max-height: 90vh; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2 style="color: #6B456C; margin: 0;">Prescrição Médica</h2>
                        <button onclick="document.getElementById('modal-prescricao-detalhes').remove()" style="background: none; border: none; font-size: 24px; cursor: pointer; color: #666;">&times;</button>
                    </div>
                    <div style="margin-bottom: 20px;">
                        <p style="margin: 5px 0;"><strong>Veterinário:</strong> ${prescricao.veterinario}</p>
                        <p style="margin: 5px 0;"><strong>Data da Consulta:</strong> ${Utils.formatDate(prescricao.data_consulta)}</p>
                        <p style="margin: 5px 0;"><strong>Diagnóstico:</strong> ${prescricao.diagnostico}</p>
                    </div>
                    <h3 style="color: #6B456C; margin-top: 20px; margin-bottom: 10px;">Medicamentos</h3>
                    ${medicamentosHtml}
                    ${prescricao.orientacoes_gerais ? `
                        <div style="margin-top: 20px; padding: 15px; background-color: #fff3cd; border-radius: 8px;">
                            <h4 style="color: #856404; margin: 0 0 10px 0;">Orientações Gerais</h4>
                            <p style="margin: 0; color: #856404;">${prescricao.orientacoes_gerais}</p>
                        </div>
                    ` : ''}
                    ${prescricao.retorno ? `<p style="margin-top: 15px;"><strong>Retorno:</strong> ${Utils.formatDate(prescricao.retorno)}</p>` : ''}
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);

        // Fechar ao clicar fora
        document.getElementById('modal-prescricao-detalhes').addEventListener('click', (e) => {
            if (e.target.id === 'modal-prescricao-detalhes') {
                e.target.remove();
            }
        });
    }

    /**
     * Handler de mudança em checkbox
     */
    handleCheckboxChange(event) {
        const checkbox = event.target;
        const label = checkbox.nextElementSibling;
        
        if (checkbox.checked) {
            label.style.textDecoration = 'line-through';
            label.style.opacity = '0.6';
        } else {
            label.style.textDecoration = 'none';
            label.style.opacity = '1';
        }
    }
}

// Instância global para acessar de onclick
let clienteController;

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    clienteController = new ClienteController();
    clienteController.init();
});

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    const controller = new ClienteController();
    controller.init();
});
