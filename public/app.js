// FantasyXI Pro - Main Client State & Interactive Controllers

const state = {
  activeTab: 'home',
  balance: 2500,
  userTeam: [],
  maxPlayers: 11,
  creditsLeft: 100.0,
  currentRole: 'WK'
};

const playersDatabase = [
  // Wicket Keepers (WK)
  { id: 1, name: 'Sanju Samson', team: 'IND', role: 'WK', credits: 9.0, points: 74.5, selected: false },
  { id: 2, name: 'Heinrich Klaasen', team: 'SA', role: 'WK', credits: 9.5, points: 88.0, selected: false },
  { id: 3, name: 'Jos Buttler', team: 'ENG', role: 'WK', credits: 10.0, points: 92.0, selected: false },

  // Batsmen (BAT)
  { id: 4, name: 'Suryakumar Yadav', team: 'IND', role: 'BAT', credits: 10.5, points: 110.0, selected: false },
  { id: 5, name: 'Travis Head', team: 'AUS', role: 'BAT', credits: 10.0, points: 95.5, selected: false },
  { id: 6, name: 'Yashasvi Jaiswal', team: 'IND', role: 'BAT', credits: 9.0, points: 82.0, selected: false },
  { id: 7, name: 'Mitchell Marsh', team: 'AUS', role: 'BAT', credits: 8.5, points: 68.0, selected: false },

  // All Rounders (AR)
  { id: 8, name: 'Hardik Pandya', team: 'IND', role: 'AR', credits: 9.5, points: 105.0, selected: false },
  { id: 9, name: 'Marcus Stoinis', team: 'AUS', role: 'AR', credits: 9.0, points: 79.0, selected: false },
  { id: 10, name: 'Axar Patel', team: 'IND', role: 'AR', credits: 8.5, points: 71.0, selected: false },

  // Bowlers (BOWL)
  { id: 11, name: 'Jasprit Bumrah', team: 'IND', role: 'BOWL', credits: 11.0, points: 125.0, selected: false },
  { id: 12, name: 'Adam Zampa', team: 'AUS', role: 'BOWL', credits: 9.0, points: 84.0, selected: false },
  { id: 13, name: 'Arshdeep Singh', team: 'IND', role: 'BOWL', credits: 8.5, points: 76.5, selected: false },
  { id: 14, name: 'Mitchell Starc', team: 'AUS', role: 'BOWL', credits: 9.5, points: 89.0, selected: false }
];

// Tab Switcher Controller
function switchTab(tabId) {
  state.activeTab = tabId;
  
  // Hide all tab contents
  document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));

  // Show active tab content
  const activeEl = document.getElementById(`tab-${tabId}`);
  if (activeEl) activeEl.classList.remove('hidden');

  // Update navbar styles
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.classList.remove('bg-brand-600', 'text-white');
    btn.classList.add('text-slate-400');
  });

  const activeNav = document.getElementById(`nav-${tabId}`);
  if (activeNav) {
    activeNav.classList.add('bg-brand-600', 'text-white');
    activeNav.classList.remove('text-slate-400');
  }

  if (tabId === 'team') {
    renderPlayers();
  }

  // Update address bar path for SPA feel
  history.pushState(null, '', `/${tabId === 'home' ? '' : tabId}`);
}

// Render Player List for Selected Role
function renderPlayers() {
  const container = document.getElementById('player-list');
  if (!container) return;

  const filtered = playersDatabase.filter(p => p.role === state.currentRole);

  container.innerHTML = filtered.map(player => `
    <div class="p-3.5 flex justify-between items-center hover:bg-white/5 transition">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-slate-800 border border-white/10 flex items-center justify-center font-bold text-xs text-brand-500">
          ${player.team}
        </div>
        <div>
          <strong class="text-white block font-semibold">${player.name}</strong>
          <span class="text-[11px] text-slate-400">${player.points} Points</span>
        </div>
      </div>

      <div class="flex items-center gap-4">
        <span class="text-xs font-bold text-accent-green">${player.credits} Cr</span>
        <button onclick="togglePlayer(${player.id})" class="px-3 py-1.5 rounded-lg text-xs font-bold transition ${
          player.selected 
            ? 'bg-rose-600 text-white' 
            : 'bg-brand-600 hover:bg-brand-500 text-white'
        }">
          ${player.selected ? 'Remove' : 'Select'}
        </button>
      </div>
    </div>
  `).join('');
}

// Filter Players by Role
function filterRole(role) {
  state.currentRole = role;
  document.querySelectorAll('.role-tab').forEach(btn => {
    btn.classList.remove('bg-brand-600', 'text-white');
    btn.classList.add('text-slate-400');
  });

  event.currentTarget.classList.add('bg-brand-600', 'text-white');
  event.currentTarget.classList.remove('text-slate-400');
  renderPlayers();
}

// Toggle Player Selection
function togglePlayer(id) {
  const player = playersDatabase.find(p => p.id === id);
  if (!player) return;

  if (player.selected) {
    player.selected = false;
    state.userTeam = state.userTeam.filter(p => p.id !== id);
    state.creditsLeft += player.credits;
  } else {
    if (state.userTeam.length >= state.maxPlayers) {
      alert('Maximum 11 players can be selected.');
      return;
    }
    if (state.creditsLeft < player.credits) {
      alert('Not enough credits left!');
      return;
    }
    player.selected = true;
    state.userTeam.push(player);
    state.creditsLeft -= player.credits;
  }

  document.getElementById('selected-count').innerText = `${state.userTeam.length} / 11`;
  document.getElementById('credits-left').innerText = state.creditsLeft.toFixed(1);
  renderPlayers();
}

// Join Contest Logic
function joinContest(name, fee) {
  if (state.balance < fee) {
    alert(`Insufficient balance! Need ₹${fee} to join ${name}. Please add cash in Wallet.`);
    switchTab('wallet');
    return;
  }

  state.balance -= fee;
  updateBalanceUI();
  alert(`🎉 Success! You have joined "${name}" for ₹${fee}. Best of luck!`);
}

// Wallet Balance UI Sync
function updateBalanceUI() {
  const el = document.getElementById('user-balance');
  const walletEl = document.getElementById('wallet-total');
  if (el) el.innerText = `₹${state.balance.toLocaleString('en-IN')}`;
  if (walletEl) walletEl.innerText = `₹${state.balance.toLocaleString('en-IN')}.00`;
}

// Add Cash Modal Trigger
function addCashModal() {
  const amount = prompt('Enter amount to add into Wallet (₹):', '500');
  if (amount && !isNaN(amount) && Number(amount) > 0) {
    state.balance += Number(amount);
    updateBalanceUI();
    alert(`₹${amount} successfully added to your wallet!`);
  }
}

// Claim Daily Rewards
function claimReward(amount) {
  state.balance += amount;
  updateBalanceUI();
  alert(`🎉 Claimed ₹${amount} bonus cash!`);
}

// Notifications Toggle Drawer
function toggleNotifications() {
  const drawer = document.getElementById('notification-drawer');
  if (drawer) drawer.classList.toggle('hidden');
}

// Copy Referral Link
function copyReferral() {
  navigator.clipboard.writeText('https://fantasyxi.pro/ref/QA95PRO');
  alert('Referral link copied to clipboard!');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  renderPlayers();
});
