/**
 * Cognisutra Utilities
 * Common JavaScript functions for the platform
 */

// API Helper - Make AJAX requests safely
class API {
    static async request(url, options = {}) {
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        };

        const config = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    static get(url) {
        return this.request(url, { method: 'GET' });
    }

    static post(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static put(url, data) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static delete(url) {
        return this.request(url, { method: 'DELETE' });
    }
}

// Notification Helper
class Notify {
    static show(message, type = 'info', duration = 3000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `p-4 rounded-lg animate-fade-in ${
            type === 'success' ? 'bg-green-100 text-green-700' :
            type === 'error' ? 'bg-red-100 text-red-700' :
            type === 'warning' ? 'bg-yellow-100 text-yellow-700' :
            'bg-blue-100 text-blue-700'
        }`;
        alertDiv.textContent = message;

        const container = document.body.appendChild(alertDiv);
        
        if (duration > 0) {
            setTimeout(() => container.remove(), duration);
        }

        return container;
    }

    static success(message, duration = 3000) {
        return this.show(message, 'success', duration);
    }

    static error(message, duration = 5000) {
        return this.show(message, 'error', duration);
    }

    static warning(message, duration = 4000) {
        return this.show(message, 'warning', duration);
    }

    static info(message, duration = 3000) {
        return this.show(message, 'info', duration);
    }
}

// Form Helper
class Form {
    static validate(formElement) {
        const formData = new FormData(formElement);
        const errors = [];

        // Check for required fields
        for (let [key, value] of formData.entries()) {
            if (!value.trim()) {
                errors.push(`${key} is required`);
            }
        }

        return {
            valid: errors.length === 0,
            errors: errors
        };
    }

    static serialize(formElement) {
        const formData = new FormData(formElement);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        return data;
    }

    static reset(formElement) {
        formElement.reset();
    }

    static disable(formElement) {
        const inputs = formElement.querySelectorAll('input, textarea, select, button');
        inputs.forEach(input => input.disabled = true);
    }

    static enable(formElement) {
        const inputs = formElement.querySelectorAll('input, textarea, select, button');
        inputs.forEach(input => input.disabled = false);
    }
}

// Debounce Helper
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle Helper
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Storage Helper
class Storage {
    static set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Storage Error:', e);
        }
    }

    static get(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Storage Error:', e);
            return null;
        }
    }

    static remove(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Storage Error:', e);
        }
    }

    static clear() {
        try {
            localStorage.clear();
        } catch (e) {
            console.error('Storage Error:', e);
        }
    }
}

// DOM Helper
class DOM {
    static ready(callback) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', callback);
        } else {
            callback();
        }
    }

    static query(selector) {
        return document.querySelector(selector);
    }

    static queryAll(selector) {
        return document.querySelectorAll(selector);
    }

    static addClass(element, className) {
        element.classList.add(className);
    }

    static removeClass(element, className) {
        element.classList.remove(className);
    }

    static toggleClass(element, className) {
        element.classList.toggle(className);
    }

    static hasClass(element, className) {
        return element.classList.contains(className);
    }

    static on(element, event, handler) {
        element.addEventListener(event, handler);
    }

    static off(element, event, handler) {
        element.removeEventListener(event, handler);
    }

    static html(element, content) {
        element.innerHTML = content;
    }

    static text(element, content) {
        element.textContent = content;
    }

    static show(element) {
        element.style.display = '';
    }

    static hide(element) {
        element.style.display = 'none';
    }

    static toggle(element) {
        element.style.display = element.style.display === 'none' ? '' : 'none';
    }
}

// String Helper
class StringUtil {
    static capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    static slug(str) {
        return str
            .toLowerCase()
            .trim()
            .replace(/[^\w\s-]/g, '')
            .replace(/[\s_]+/g, '-')
            .replace(/^-+|-+$/g, '');
    }

    static truncate(str, length = 50) {
        return str.length > length ? str.substring(0, length) + '...' : str;
    }

    static capitalizeWords(str) {
        return str.replace(/\b\w/g, char => char.toUpperCase());
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { API, Notify, Form, debounce, throttle, Storage, DOM, StringUtil };
}
