import { c as create_ssr_component, a as subscribe, e as escape } from "../../chunks/ssr.js";
import { a as authStore } from "../../chunks/authStore.js";
import "@sveltejs/kit/internal";
import "../../chunks/exports.js";
import "../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../chunks/state.svelte.js";
const Layout = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let $authStore, $$unsubscribe_authStore;
  $$unsubscribe_authStore = subscribe(authStore, (value) => $authStore = value);
  $$unsubscribe_authStore();
  return `<div class="min-h-screen bg-gray-50"> <nav class="bg-white shadow-sm border-b border-gray-200"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="flex justify-between h-16"><div class="flex items-center space-x-8"><a href="/" class="flex items-center" data-svelte-h="svelte-ceyucn"><span class="text-2xl font-bold text-blue-600">SkillNest</span></a> <div class="hidden md:flex space-x-4"><a href="/problems" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition" data-svelte-h="svelte-1vadzuw">Problems</a> <a href="/leaderboard" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition" data-svelte-h="svelte-ga2imy">Leaderboard</a> ${$authStore.isAuthenticated ? `<a href="/dashboard" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition" data-svelte-h="svelte-y45gz9">Dashboard</a> ${$authStore.user?.role === "admin" ? `<a href="/teacher/dashboard" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition" data-svelte-h="svelte-13qztle">Admin</a>` : ``}` : ``}</div></div> <div class="flex items-center space-x-4">${$authStore.isAuthenticated ? `<span class="text-sm text-gray-700">${escape($authStore.user?.email)}</span> <button class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium transition" data-svelte-h="svelte-1b2poju">Logout</button>` : `<a href="/login" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition" data-svelte-h="svelte-43j1da">Login</a> <a href="/register" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition" data-svelte-h="svelte-qn635r">Register</a>`}</div></div></div></nav>  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">${slots.default ? slots.default({}) : ``}</main>  <footer class="bg-white border-t border-gray-200 mt-12" data-svelte-h="svelte-1gmbbr7"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6"><p class="text-center text-gray-500 text-sm">© 2026 SkillNest. Multi-language Coding Platform with Docker Sandbox Execution.</p></div></footer></div>`;
});
export {
  Layout as default
};
