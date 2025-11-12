// Script JavaScript principal
console.log('Pet Shop website loaded');

// Adicione suas funções JavaScript aqui
document.addEventListener('DOMContentLoaded', function() {
    // Exemplo: adicionar interatividade aos cards
    const cards = document.querySelectorAll('.service-card');
    
    cards.forEach(card => {
        card.addEventListener('click', function() {
            console.log('Card clicado:', this.querySelector('h3').textContent);
        });
    });
});
