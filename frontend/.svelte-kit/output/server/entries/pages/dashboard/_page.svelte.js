import { c as create_ssr_component, a as subscribe } from "../../../chunks/ssr.js";
import { a as authStore } from "../../../chunks/authStore.js";
import "@sveltejs/kit/internal";
import "../../../chunks/exports.js";
import "../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../chunks/state.svelte.js";
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let $$unsubscribe_authStore;
  $$unsubscribe_authStore = subscribe(authStore, (value) => value);
  $$unsubscribe_authStore();
  return `${$$result.head += `<!-- HEAD_svelte-12tbmtc_START -->${$$result.title = `<title>Dashboard - SkillNest</title>`, ""}<!-- HEAD_svelte-12tbmtc_END -->`, ""} ${`<div class="flex justify-center items-center py-12" data-svelte-h="svelte-120vuiy"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>`}`;
});
export {
  Page as default
};
