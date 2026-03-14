import { w as writable } from "./index.js";
import { a as authApi, c as clearToken } from "./client.js";
const initialState = {
  isAuthenticated: false,
  user: null,
  loading: false,
  error: null
};
function createAuthStore() {
  const { subscribe, set, update } = writable(initialState);
  return {
    subscribe,
    async login(email, password) {
      update((state) => ({ ...state, loading: true, error: null }));
      try {
        await authApi.login(email, password);
        const user = await authApi.getCurrentUser();
        update((state) => ({
          ...state,
          isAuthenticated: true,
          user,
          loading: false
        }));
        return true;
      } catch (error) {
        update((state) => ({
          ...state,
          loading: false,
          error: error.message
        }));
        return false;
      }
    },
    async register(email, password) {
      update((state) => ({ ...state, loading: true, error: null }));
      try {
        await authApi.register(email, password);
        return await this.login(email, password);
      } catch (error) {
        update((state) => ({
          ...state,
          loading: false,
          error: error.message
        }));
        return false;
      }
    },
    async logout() {
      try {
        await authApi.logout();
      } catch (error) {
        console.error("Logout error:", error);
      }
      clearToken();
      set(initialState);
    },
    async checkAuth() {
      update((state) => ({ ...state, loading: true }));
      try {
        const user = await authApi.getCurrentUser();
        update((state) => ({
          ...state,
          isAuthenticated: true,
          user,
          loading: false
        }));
      } catch (error) {
        update((state) => ({
          ...state,
          isAuthenticated: false,
          user: null,
          loading: false
        }));
      }
    },
    clearError() {
      update((state) => ({ ...state, error: null }));
    }
  };
}
const authStore = createAuthStore();
export {
  authStore as a
};
