let currentRow;

document.addEventListener('DOMContentLoaded', () => {
    fetch('http://127.0.0.1:8000/dados') // Substitua pela URL da sua API
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('teste')
            populateTable(data);
            document.getElementById('loading').style.display = 'none'; // Esconde a mensagem de carregamento
            document.getElementById('dataframe').style.display = 'table'; // Mostra a tabela
        })
        .catch(error => {
            console.error('Houve um problema com a requisição:', error);
            document.getElementById('loading').innerText = 'Erro ao carregar dados.';
        });
});

function populateTable(data) {
    const tbody = document.querySelector('#dataframe tbody');
    const thead = document.querySelector('#dataframe thead tr');
    
    tbody.innerHTML = ''; // Limpa a tabela antes de preencher
    thead.innerHTML = ''; // Limpa o cabeçalho antes de preencher

    // Extrai as colunas automaticamente
    if (data.length > 0) {
        const columns = Object.keys(data[0]);
        
        // Preenche o cabeçalho da tabela
        columns.forEach(col => {
            const th = document.createElement('th');
            th.innerText = col.charAt(0).toUpperCase() + col.slice(1); // Capitaliza a primeira letra
            thead.appendChild(th);
        });

        // Preenche as linhas da tabela
        data.forEach(item => {
            const row = document.createElement('tr');
            row.onclick = () => editRow(row);
            columns.forEach(col => {
                const td = document.createElement('td');
                td.innerText = item[col];
                row.appendChild(td);
            });
            tbody.appendChild(row);
        });
    }
}

function editRow(row) {
    currentRow = row;
    const valueCell = row.cells[2].innerText; // Supondo que a coluna a ser editada seja a terceira
    document.getElementById('newValue').value = valueCell;
    document.getElementById('editModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}

function saveChanges() {
    const newValue = document.getElementById('newValue').value;
    currentRow.cells[2].innerText = newValue; // Atualiza a célula correspondente
    closeModal();
}

// Fechar o modal ao clicar fora dele
window.onclick = function(event) {
    const modal = document.getElementById('editModal');
    if (event.target == modal) {
        closeModal();
    }
}