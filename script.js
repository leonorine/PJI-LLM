// Versions et LLM disponibles
const versions = ['v1', 'v2', 'v3', 'v4', 'v5', 'v6'];
const llms = ['ChatGPT', 'Gemini', 'Perplexity'];

// État courant
let currentVersion = 'v1';
let currentLLM = 'ChatGPT';

// Met à jour le titre et le iframe
function updateAppViewer() {
    document.getElementById('selected-version-title').textContent =
        "Version " + currentVersion.substring(1);
    const iframe = document.getElementById('app-viewer');
    iframe.src = `./${currentLLM}/${currentVersion}/index.html`;
}

// Gestion des tabs de version
document.querySelectorAll('#version-tabs li').forEach(tab => {
    tab.addEventListener('click', function() {
        document.querySelectorAll('#version-tabs li').forEach(li => li.classList.remove('active'));
        this.classList.add('active');
        currentVersion = this.getAttribute('data-version');
        updateAppViewer();
    });
});

// Gestion des boutons LLM
document.querySelectorAll('.llm-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.llm-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        currentLLM = this.getAttribute('data-llm');
        updateAppViewer();
    });
});

// Initialisation
document.querySelector('.llm-btn[data-llm="ChatGPT"]').classList.add('active');
updateAppViewer();
