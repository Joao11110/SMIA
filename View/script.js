document.getElementById('carregarEspecialistas').addEventListener('click', carregarEspecialistas);

async function carregarEspecialistas() {
    try {
        const response = await fetch('http://localhost:5000/especialistas');
        if (!response.ok) {
            throw new Error('Erro ao carregar especialistas');
        }
        const especialistas = await response.json();
        exibirEspecialistas(especialistas);
    } catch (error) {
        console.error('Erro:', error);
        document.getElementById('listaEspecialistas').innerHTML = 
            `<p class="error">${error.message}</p>`;
    }
}

function exibirEspecialistas(especialistas) {
    const listaDiv = document.getElementById('listaEspecialistas');
    
    if (especialistas.length === 0) {
        listaDiv.innerHTML = '<p>Nenhum especialista encontrado</p>';
        return;
    }

    const listaHTML = especialistas.map(esp => `
        <div class="especialista">
            <h3>${esp.nome}</h3>
            <p>CRM: ${esp.crm}</p>
            <p>Email: ${esp.email}</p>
        </div>
    `).join('');

    listaDiv.innerHTML = listaHTML;
}