// Todo App with Local Storage
class TodoApp {
    constructor() {
        this.todos = [];
        this.currentFilter = 'all';
        this.init();
    }

    init() {
        this.loadTodosFromStorage();
        this.setupEventListeners();
        this.render();
    }

    // Local Storage Methods
    saveTodosToStorage() {
        localStorage.setItem('todos', JSON.stringify(this.todos));
        console.log('✓ Todos saved to local storage');
    }

    loadTodosFromStorage() {
        const stored = localStorage.getItem('todos');
        this.todos = stored ? JSON.parse(stored) : [];
        console.log('✓ Todos loaded from local storage', this.todos.length, 'items');
    }

    // Todo Management
    addTodo(text, priority = 'medium') {
        if (!text.trim()) {
            alert('Please enter a task!');
            return;
        }

        const todo = {
            id: Date.now(),
            text: text.trim(),
            completed: false,
            priority: priority,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };

        this.todos.unshift(todo);
        this.saveTodosToStorage();
        this.render();
    }

    deleteTodo(id) {
        this.todos = this.todos.filter(todo => todo.id !== id);
        this.saveTodosToStorage();
        this.render();
    }

    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            todo.updatedAt = new Date().toISOString();
            this.saveTodosToStorage();
            this.render();
        }
    }

    editTodo(id, newText, newPriority) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.text = newText.trim();
            todo.priority = newPriority;
            todo.updatedAt = new Date().toISOString();
            this.saveTodosToStorage();
            this.render();
        }
    }

    clearCompleted() {
        this.todos = this.todos.filter(todo => !todo.completed);
        this.saveTodosToStorage();
        this.render();
    }

    deleteAll() {
        if (this.todos.length === 0) {
            alert('No tasks to delete!');
            return;
        }
        if (confirm('Are you sure you want to delete ALL tasks?')) {
            this.todos = [];
            this.saveTodosToStorage();
            this.render();
        }
    }

    // Filtering
    getFilteredTodos() {
        switch (this.currentFilter) {
            case 'active':
                return this.todos.filter(t => !t.completed);
            case 'completed':
                return this.todos.filter(t => t.completed);
            default:
                return this.todos;
        }
    }

    // Statistics
    updateStats() {
        const total = this.todos.length;
        const active = this.todos.filter(t => !t.completed).length;
        const completed = this.todos.filter(t => t.completed).length;

        document.getElementById('totalCount').textContent = total;
        document.getElementById('activeCount').textContent = active;
        document.getElementById('completedCount').textContent = completed;

        // Disable clear completed if no completed tasks
        const clearBtn = document.getElementById('clearCompleted');
        clearBtn.disabled = completed === 0;

        // Disable delete all if no tasks
        const deleteBtn = document.getElementById('deleteAll');
        deleteBtn.disabled = total === 0;
    }

    // Rendering
    renderTodoItem(todo) {
        const li = document.createElement('li');
        li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
        li.dataset.id = todo.id;

        li.innerHTML = `
            <input type="checkbox" class="checkbox" ${todo.completed ? 'checked' : ''}>
            <div class="todo-content">
                <span class="todo-text">${this.escapeHtml(todo.text)}</span>
                <span class="priority-badge ${todo.priority}">${todo.priority}</span>
            </div>
            <div class="todo-actions">
                <button class="edit-btn" title="Edit">✏️ Edit</button>
                <button class="delete-btn" title="Delete">🗑️ Delete</button>
            </div>
        `;

        // Event listeners for this item
        const checkbox = li.querySelector('.checkbox');
        checkbox.addEventListener('change', () => this.toggleTodo(todo.id));

        const editBtn = li.querySelector('.edit-btn');
        editBtn.addEventListener('click', () => this.openEditModal(todo));

        const deleteBtn = li.querySelector('.delete-btn');
        deleteBtn.addEventListener('click', () => this.deleteTodo(todo.id));

        return li;
    }

    render() {
        const todoList = document.getElementById('todoList');
        const emptyState = document.getElementById('emptyState');
        const filteredTodos = this.getFilteredTodos();

        // Clear list
        todoList.innerHTML = '';

        if (filteredTodos.length === 0) {
            emptyState.style.display = 'block';
            todoList.style.display = 'none';
        } else {
            emptyState.style.display = 'none';
            todoList.style.display = 'block';
            filteredTodos.forEach(todo => {
                todoList.appendChild(this.renderTodoItem(todo));
            });
        }

        this.updateStats();
    }

    // Modal/Edit functionality
    openEditModal(todo) {
        const modal = document.getElementById('editModal');
        const editInput = document.getElementById('editInput');
        const editPriority = document.getElementById('editPriority');
        const saveBtn = document.getElementById('saveEditBtn');

        editInput.value = todo.text;
        editPriority.value = todo.priority;

        modal.classList.add('active');

        const handleSave = () => {
            const newText = editInput.value;
            const newPriority = editPriority.value;
            if (newText.trim()) {
                this.editTodo(todo.id, newText, newPriority);
                modal.classList.remove('active');
                saveBtn.removeEventListener('click', handleSave);
            }
        };

        saveBtn.addEventListener('click', handleSave);

        const cancelBtn = document.getElementById('cancelEditBtn');
        const handleCancel = () => {
            modal.classList.remove('active');
            cancelBtn.removeEventListener('click', handleCancel);
            saveBtn.removeEventListener('click', handleSave);
        };
        cancelBtn.addEventListener('click', handleCancel);
    }

    // Utility
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Event Listeners Setup
    setupEventListeners() {
        // Add todo
        const addBtn = document.getElementById('addBtn');
        const todoInput = document.getElementById('todoInput');

        const handleAdd = () => {
            const priority = document.getElementById('prioritySelect')?.value || 'medium';
            this.addTodo(todoInput.value, priority);
            todoInput.value = '';
            todoInput.focus();
        };

        addBtn.addEventListener('click', handleAdd);
        todoInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleAdd();
        });

        // Filter buttons
        const filterBtns = document.querySelectorAll('.filter-btn');
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.currentFilter = btn.dataset.filter;
                this.render();
            });
        });

        // Action buttons
        document.getElementById('clearCompleted').addEventListener('click', () => this.clearCompleted());
        document.getElementById('deleteAll').addEventListener('click', () => this.deleteAll());

        // Close modal when clicking outside
        const modal = document.getElementById('editModal');
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('active');
                }
            });
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TodoApp();
    console.log('✓ Todo App initialized');
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+K or Cmd+K to focus input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('todoInput').focus();
    }
});
