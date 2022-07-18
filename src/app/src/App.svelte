<script>
  import Ed from "./lib/Editor.svelte";
  import { writable } from "svelte/store";
  import { onDestroy } from "svelte";
  const content = writable("");
  const hash = writable("");
  const dates = writable(null);
  const active = writable(null);
  const api = "http://localhost:8000";
  let lock = false
  async function digest(message) {
    const msgUint8 = new TextEncoder().encode(message); // encode as (utf-8) Uint8Array
    const hashBuffer = await crypto.subtle.digest("SHA-1", msgUint8); // hash the message
    const hashArray = Array.from(new Uint8Array(hashBuffer)); // convert buffer to byte array
    const hashHex = hashArray
      .map((b) => b.toString(16).padStart(2, "0"))
      .join(""); // convert bytes to hex string
    return hashHex;
  }
  const ud = dates.subscribe((v) => {
    if (!v) return;
    console.log("new val pal", v.year);
    console.log(v.day[1]);
    active.set(v.day[1]);
    fetch(`${api}/pages/${v.day[1]}`).then(async (r) => {
      let c = await r.json();
      content.set(c.text);
      hash.set(await digest(c));
    });
  });
  fetch(api + "/dates").then(async (r) => dates.set(await r.json()));

  const uv = content.subscribe(async (v) => {
    if (lock) return;
    console.log("sending data")
    if (!v) return;
    let h = await digest(v);
    if (h == $hash) return;
    lock = true
    fetch(api + "/pages", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        key: $active,
        text: $content,
      }),
    }).then(async (r) => {
      lock = false
    });
  });
  onDestroy(ud);
  onDestroy(uv);
</script>

<main>
  <div class="wrapper">
    <div class="nav">
      <div class="navitem">
        <button>+</button>
        <button>D1</button>
        <button>-</button>
      </div>
      <div class="navitem">
        <button>+</button>
        <button>W1</button>
        <button>-</button>
      </div>
      <div class="navitem">
        <button>+</button>
        <button>M1</button>
        <button>-</button>
      </div>
      <div class="navitem">
        <button>+</button>
        <button>Y1</button>
        <button>-</button>
      </div>
    </div>
    <textarea bind:value={$content} />
  </div>
</main>

<style>
  .wrapper {
    display: flex;
    flex-direction: column;
  }
  .nav {
    display: flex;
  }
  .navitem {
    margin-left: 20px;
  }
</style>
