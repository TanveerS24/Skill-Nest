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
  let confirmPassword = "";
  $$unsubscribe_authStore();
  return `${$$result.head += `<!-- HEAD_svelte-1vr87rd_START -->${$$result.title = `<title>Register - SkillNest</title>`, ""}<!-- HEAD_svelte-1vr87rd_END -->`, ""} <div class="flex flex-col items-center justify-center min-h-[calc(100vh-12rem)]"><div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md"><h1 class="text-3xl font-bold mb-6 text-center text-gray-900" data-svelte-h="svelte-zqnkg8">Create Account</h1> ${$authStore.error ? `<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">${escape($authStore.error)}</div>` : ``} ${``} <form><div class="mb-4"><label for="email" class="block text-sm font-medium text-gray-700 mb-2" data-svelte-h="svelte-hrq7r8">Email</label> <input id="email" type="email" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="your@email.com" required${add_attribute("value", email)}></div> <div class="mb-4"><label for="password" class="block text-sm font-medium text-gray-700 mb-2" data-svelte-h="svelte-1k7rb9q">Password</label> <input id="password" type="password" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="••••••••" minlength="8" required${add_attribute("value", password)}> <p class="mt-1 text-xs text-gray-500" data-svelte-h="svelte-yhvj1a">Minimum 8 characters</p></div> <div class="mb-6"><label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2" data-svelte-h="svelte-q0fdo5">Confirm Password</label> <input id="confirmPassword" type="password" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="••••••••" required${add_attribute("value", confirmPassword)}></div> <button type="submit" ${""} class="w-full bg-blue-600 text-white py-2 px-4 rounded-md font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition">${escape("Register")}</button></form> <p class="mt-6 text-center text-sm text-gray-600" data-svelte-h="svelte-uxdfwj">Already have an account?
			<a href="/login" class="text-blue-600 hover:text-blue-700 font-medium">Login here</a></p></div></div>`;
});
export {
  Page as default
};
