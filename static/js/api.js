const API_BASE = ""; // Relative since served from same domain

class ApiService {
    constructor() {
        this.token = localStorage.getItem('access_token');
        this.user = JSON.parse(localStorage.getItem('user_data') || 'null');
    }

    setAuth(token, user) {
        this.token = token;
        this.user = user;
        localStorage.setItem('access_token', token);
        localStorage.setItem('user_data', JSON.stringify(user));
    }

    logout() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_data');
    }

    isAuthenticated() {
        return !!this.token;
    }

    async request(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...(this.token ? { 'Authorization': `Bearer ${this.token}` } : {}),
            ...options.headers
        };

        const config = {
            ...options,
            headers
        };

        if (options.body && typeof options.body === 'object' && !(options.body instanceof URLSearchParams)) {
            config.body = JSON.stringify(options.body);
        }

        const response = await fetch(`${API_BASE}${endpoint}`, config);
        
        if (response.status === 401) {
            this.logout();
            window.location.reload();
            throw new Error("Unauthorized");
        }

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || `HTTP error ${response.status}`);
        }

        // Return blob for exports, json otherwise
        if (options.isBlob) {
            return response.blob();
        }
        
        return response.json();
    }

    async login(username, password) {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const data = await this.request('/token', {
            method: 'POST',
            body: formData,
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });

        this.setAuth(data.access_token, {
            username: data.username,
            role: data.role,
            assigned_year: data.assigned_year
        });
        return data;
    }

    async getStudents(year = null) {
        let url = '/students';
        if (year) url += `?year=${year}`;
        return this.request(url);
    }

    async markLate(studentLogs, session) {
        return this.request('/logs', {
            method: 'POST',
            body: { student_logs: studentLogs, session }
        });
    }

    async getLogs(filters = {}) {
        const params = new URLSearchParams();
        if (filters.date) params.append('date', filters.date);
        if (filters.year) params.append('year', filters.year);
        if (filters.session) params.append('session', filters.session);
        
        return this.request(`/logs?${params.toString()}`);
    }

    async getStats() {
        return this.request('/stats');
    }

    async exportCsv(filters = {}) {
        const params = new URLSearchParams();
        if (filters.date) params.append('date', filters.date);
        if (filters.year) params.append('year', filters.year);
        
        const blob = await this.request(`/export/csv?${params.toString()}`, { isBlob: true });
        
        // Trigger download
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `late_logs_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    }

    async deleteLog(logId) {
        return this.request(`/logs/${logId}`, {
            method: 'DELETE'
        });
    }
}

const api = new ApiService();
