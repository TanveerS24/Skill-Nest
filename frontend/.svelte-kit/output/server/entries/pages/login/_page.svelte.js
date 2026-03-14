import { c as create_ssr_component, a as subscribe, e as escape, d as add_attribute } from "../../../chunks/ssr.js";
import { a as authStore } from "../../../chunks/authStore.js";
import "@sveltejs/kit/internal";
import "../../../chunks/exports.js";
import "../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../chunks/state.svelte.js";
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let $authStore, $$unsubscribe_authStore;
  $$unsubscribe_authStore = subscribe(authStore, (value) => $authStore = value);
  let email = "";
  let password = "";
  $$unsubscribe_authStore();
  return `${$$result.head += `<!-- HEAD_svelte-1g9cjhb_START -->${$$result.title = `<title>Login - SkillNest</title>`, ""}<!-- HEAD_svelte-1g9cjhb_END -->`, ""} <div class="flex flex-col items-center justify-center min-h-[calc(100vh-12rem)]"><div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md"><h1 class="text-3xl font-bold mb-6 text-center text-gray-900" data-svelte-h="svelte-13ie3gu">Login to SkillNest</h1> ${$authStore.error ? `<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">${escape($authStore.error)}</div>` : ``} <form><div class="mb-4"><label for="email" class="block text-sm font-medium text-gray-700 mb-2" data-svelte-h="svelte-hrq7r8">Email</label> <input id="email" type="email" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="your@email.com" required${add_attribute("value", email)}></div> <div class="mb-6"><label for="password" class="block text-sm font-medium text-gray-700 mb-2" data-svelte-h="svelte-1k7rb9q">Password</label> <input id="password" type="password" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="••••••••" required${add_attribute("value", password)}></div> <button type="submit" ${""} class="w-full bg-blue-600 text-white py-2 px-4 rounded-md font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition">${escape("Login")}</button></form> <p class="mt-6 text-center text-sm text-gray-600" data-svelte-h="svelte-p4dtu9">Don&#39;t have an account?
			<a href="/register" class="text-blue-600 hover:text-blue-700 font-medium">Register here</a></p> <div class="mt-6 pt-6 border-t border-gray-200" data-svelte-h="svelte-1ed5d8f"><p class="text-xs text-gray-500 text-center">Demo credentials:<br>
				Admin: admin@skillnest.com / admin123<br>
				User: user@test.com / user123</p></div></div></div>`;
});
export {
  Page as default
};
