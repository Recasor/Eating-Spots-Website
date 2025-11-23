const tabs = document.querySelectorAll('.tab');
let tabActive = 'все',
    searchText = '';


tabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
        e.preventDefault();
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        tabActive = tab.dataset.tab;
        renderCards(tab.dataset.tab, searchText);
    });
});

const search = document.getElementById('searchCafe');

search.addEventListener('input', () => {
    searchText = search.value.toLowerCase();
    renderCards(tabActive, searchText);
});