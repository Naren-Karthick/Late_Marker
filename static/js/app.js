// State
let state = {
    selectedYear: null,
    selectedSession: null,
    students: [],
    selectedStudents: new Map(),
    logs: []
};

// DOM Elements
const views = {
    auth: document.getElementById('auth-view'),
    main: document.getElementById('main-layout'),
    tracker: document.getElementById('tracker-view'),
    dashboard: document.getElementById('dashboard-view')
};

const UI = {
    toast: document.getElementById('toast'),
    loginForm: document.getElementById('login-form'),
    btnLogout: document.getElementById('btn-logout'),
    navTracker: document.getElementById('nav-tracker'),
    navDashboard: document.getElementById('nav-dashboard'),
    yearSelector: document.getElementById('year-selector'),
    sessionSelector: document.getElementById('session-selector'),
    studentList: document.getElementById('student-list'),
    searchInput: document.getElementById('student-search'),
    selectedCount: document.getElementById('selected-count'),
    btnSubmit: document.getElementById('btn-submit-late'),
    trackerRoleInfo: document.getElementById('tracker-role-info'),
    logsTableBody: document.querySelector('#logs-table tbody'),
    btnExport: document.getElementById('btn-export'),
    filterDate: document.getElementById('filter-date'),
    filterYear: document.getElementById('filter-year'),
    statsContainer: document.getElementById('stats-container')
};

// Utils
function showToast(message, type = 'success') {
    UI.toast.textContent = message;
    UI.toast.className = `toast show ${type}`;
    setTimeout(() => {
        UI.toast.className = 'toast';
    }, 3000);
}

function switchView(viewName) {
    Object.values(views).forEach(v => v?.classList.remove('active'));
    if (viewName === 'auth') {
        views.auth.classList.add('active');
    } else {
        views.main.classList.add('active');
        views.tracker.classList.remove('active');
        views.dashboard.classList.remove('active');
        views[viewName].classList.add('active');
        
        UI.navTracker.classList.toggle('active', viewName === 'tracker');
        UI.navDashboard.classList.toggle('active', viewName === 'dashboard');
    }
}

// Initialization
function init() {
    if (api.isAuthenticated()) {
        setupApp();
    } else {
        switchView('auth');
    }
    attachEventListeners();
}

async function setupApp() {
    switchView('tracker');
    UI.trackerRoleInfo.textContent = `Logged in as: ${api.user.role} (${api.user.username})`;
    
    // Reps are restricted to their year
    if (api.user.role === 'Rep') {
        UI.navDashboard.style.display = 'none'; // Reps don't need full dashboard
        UI.yearSelector.innerHTML = `<button class="pill selected" data-value="${api.user.assigned_year}">${api.user.assigned_year.replace('_', ' ')}</button>`;
        state.selectedYear = api.user.assigned_year;
        await fetchStudents();
    }
}

// Event Listeners
function attachEventListeners() {
    // Auth
    UI.loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = e.target.querySelector('button');
        btn.disabled = true;
        btn.textContent = 'Logging in...';
        try {
            await api.login(
                document.getElementById('username').value,
                document.getElementById('password').value
            );
            showToast('Logged in successfully');
            setupApp();
        } catch (err) {
            showToast('Invalid credentials', 'error');
        } finally {
            btn.disabled = false;
            btn.textContent = 'Login';
        }
    });

    UI.btnLogout.addEventListener('click', () => {
        api.logout();
        switchView('auth');
    });

    // Navigation
    UI.navTracker.addEventListener('click', () => switchView('tracker'));
    UI.navDashboard.addEventListener('click', () => {
        switchView('dashboard');
        loadDashboard();
    });

    // Selectors
    UI.yearSelector.addEventListener('click', async (e) => {
        if(api.user.role === 'Rep') return; // Cannot change year
        if (e.target.classList.contains('pill')) {
            document.querySelectorAll('#year-selector .pill').forEach(p => p.classList.remove('selected'));
            e.target.classList.add('selected');
            state.selectedYear = e.target.dataset.value;
            await fetchStudents();
        }
    });

    UI.sessionSelector.addEventListener('click', (e) => {
        if (e.target.classList.contains('pill')) {
            document.querySelectorAll('#session-selector .pill').forEach(p => p.classList.remove('selected'));
            e.target.classList.add('selected');
            state.selectedSession = e.target.dataset.value;
            checkSubmitState();
        }
    });

    // Search
    UI.searchInput.addEventListener('input', (e) => {
        renderStudents(e.target.value.toLowerCase());
    });

    // Submit
    UI.btnSubmit.addEventListener('click', async () => {
        if (!state.selectedYear || !state.selectedSession || state.selectedStudents.size === 0) return;
        
        const studentLogs = Array.from(state.selectedStudents.entries()).map(([id, data]) => ({
            student_id: id,
            date: data.date,
            time: data.time
        }));
        
        try {
            UI.btnSubmit.disabled = true;
            UI.btnSubmit.textContent = 'Submitting...';
            
            await api.markLate(
                studentLogs,
                state.selectedSession
            );
            
            showToast(`Successfully logged ${state.selectedStudents.size} students`);
            
            // Reset state
            state.selectedStudents.clear();
            renderStudents();
            checkSubmitState();
        } catch (err) {
            showToast('Failed to submit logs', 'error');
        } finally {
            UI.btnSubmit.disabled = false;
            UI.btnSubmit.textContent = 'Submit Late Entry';
        }
    });

    // Dashboard Filters & Export
    if(UI.filterDate) UI.filterDate.addEventListener('change', loadDashboard);
    if(UI.filterYear) UI.filterYear.addEventListener('change', loadDashboard);
    if(UI.btnExport) {
        UI.btnExport.addEventListener('click', async () => {
            try {
                await api.exportCsv({
                    date: UI.filterDate.value,
                    year: UI.filterYear.value
                });
                showToast('Export successful');
            } catch (err) {
                showToast('Failed to export', 'error');
            }
        });
    }
}

// Tracker Logic
async function fetchStudents() {
    if (!state.selectedYear) return;
    try {
        state.students = await api.getStudents(state.selectedYear);
        state.selectedStudents.clear(); // Reset selection on year change
        renderStudents();
    } catch (err) {
        showToast('Failed to load students', 'error');
    }
}

function renderStudents(filter = '') {
    UI.studentList.innerHTML = '';
    
    const filtered = state.students.filter(s => 
        s.name.toLowerCase().includes(filter) || 
        s.register_no.toLowerCase().includes(filter)
    );

    if (filtered.length === 0) {
        UI.studentList.innerHTML = '<p class="text-muted">No students found.</p>';
        return;
    }

    filtered.forEach(student => {
        const isSelected = state.selectedStudents.has(student.id);
        const card = document.createElement('div');
        card.className = `student-card ${isSelected ? 'selected' : ''}`;
        card.innerHTML = `
            <div class="checkbox"></div>
            <div class="student-info">
                <h4>${student.name}</h4>
                <p>${student.register_no} • ${student.batch}</p>
            </div>
        `;
        
        card.addEventListener('click', () => {
            if (state.selectedStudents.has(student.id)) {
                state.selectedStudents.delete(student.id);
                card.classList.remove('selected');
            } else {
                const now = new Date();
                const dateStr = now.toISOString().split('T')[0];
                const timeStr = now.toTimeString().split(' ')[0]; // HH:MM:SS
                state.selectedStudents.set(student.id, { date: dateStr, time: timeStr });
                card.classList.add('selected');
            }
            updateSelectionCount();
            checkSubmitState();
        });
        
        UI.studentList.appendChild(card);
    });
    
    updateSelectionCount();
}

function updateSelectionCount() {
    UI.selectedCount.textContent = `${state.selectedStudents.size} selected`;
}

function checkSubmitState() {
    UI.btnSubmit.disabled = !(state.selectedYear && state.selectedSession && state.selectedStudents.size > 0);
}

// Dashboard Logic
async function loadDashboard() {
    if(api.user.role === 'Rep') return;

    const actionCol = document.getElementById('col-action');
    if(api.user.role !== 'HOD' && actionCol) {
        actionCol.style.display = 'none';
    } else if(actionCol) {
        actionCol.style.display = 'table-cell';
    }

    try {
        const filters = {
            date: UI.filterDate.value,
            year: UI.filterYear.value
        };
        const [logs, stats] = await Promise.all([
            api.getLogs(filters),
            api.getStats()
        ]);
        
        // Render Logs
        UI.logsTableBody.innerHTML = '';
        if(logs.length === 0) {
            UI.logsTableBody.innerHTML = `<tr><td colspan="${api.user.role === 'HOD' ? 6 : 5}" style="text-align:center">No records found</td></tr>`;
        } else {
            logs.forEach(log => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${log.date} ${log.time}</td>
                    <td><span class="pill" style="padding:0.2rem 0.5rem;font-size:0.8rem">${log.session}</span></td>
                    <td>${log.student.register_no}</td>
                    <td>${log.student.name}</td>
                    <td>${log.student.year.replace('_', ' ')}</td>
                `;
                
                if (api.user.role === 'HOD') {
                    const tdAction = document.createElement('td');
                    const delBtn = document.createElement('button');
                    delBtn.className = 'btn-outline text-danger';
                    delBtn.style.padding = '0.4rem 0.8rem';
                    delBtn.textContent = 'Delete';
                    delBtn.onclick = async () => {
                        if(confirm('Are you sure you want to delete this log?')) {
                            try {
                                await api.deleteLog(log.id);
                                showToast('Log deleted');
                                loadDashboard(); // refresh
                            } catch(e) {
                                showToast('Failed to delete', 'error');
                            }
                        }
                    };
                    tdAction.appendChild(delBtn);
                    tr.appendChild(tdAction);
                }
                
                UI.logsTableBody.appendChild(tr);
            });
        }
        
        // Render Stats (Simple version)
        if (!filters.date && !filters.year) { // Only show general stats when not heavily filtered
            UI.statsContainer.innerHTML = `
                <div class="stat-card glass">
                    <h3>${logs.length}</h3>
                    <p>Total Lates (Filtered)</p>
                </div>
                <div class="stat-card glass">
                    <h3>${stats.length}</h3>
                    <p>Unique Students Late (30 days)</p>
                </div>
            `;
        }
        
    } catch (err) {
        showToast('Failed to load dashboard', 'error');
    }
}

// Start app
init();
