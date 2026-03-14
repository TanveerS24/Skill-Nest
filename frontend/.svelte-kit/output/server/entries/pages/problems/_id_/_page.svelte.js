import { c as create_ssr_component, a as subscribe, e as escape } from "../../../../chunks/ssr.js";
import { p as page } from "../../../../chunks/stores.js";
import { a as authStore } from "../../../../chunks/authStore.js";
import "monaco-editor";
import "@sveltejs/kit/internal";
import "../../../../chunks/exports.js";
import "../../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../../chunks/state.svelte.js";
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let $$unsubscribe_authStore;
  let $$unsubscribe_page;
  $$unsubscribe_authStore = subscribe(authStore, (value) => value);
  $$unsubscribe_page = subscribe(page, (value) => value);
  let $$settled;
  let $$rendered;
  let previous_head = $$result.head;
  do {
    $$settled = true;
    $$result.head = previous_head;
    $$rendered = `${$$result.head += `<!-- HEAD_svelte-awtmnj_START -->${$$result.title = `<title>${escape("Problem")} - SkillNest</title>`, ""}<!-- HEAD_svelte-awtmnj_END -->`, ""} ${`${`${``}`}`}`;
  } while (!$$settled);
  $$unsubscribe_authStore();
  $$unsubscribe_page();
  return $$rendered;
});
export {
  Page as default
};
