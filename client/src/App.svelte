<script>
  import Body from "./Body.svelte";
  const bodyDataRequest = getBodyInformation();

  function addLeadingZero(n) {
    if (n < 10) {
      return "0" + n;
    }
    return n;
  }

  async function getBodyInformation() {
    const response = await fetch("./get-body-info");
    const data = await response.text();
    const divs = document.querySelectorAll("div.body");
    return (
      data
        // Remove starting and closing square brackets
        .slice(1, data.length - 1)
        // Replace single quotes with double quotes
        .replaceAll(`'`, `"`)
        // Create array with individual objects
        .split("},")
        // Add closing curly brace to all except last element
        .map((e, i, a) => (i !== a.length - 1 ? e + "}" : e))
        // Convert each item to object
        .map(JSON.parse)
    );
  }
</script>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  #solar-system-objects {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }

  h1 {
    font-size: 4em;
  }

  h2 {
    font-size: 2em;
  }

  h1, h2 {
    color: hsl(20, 100%, 50%);
    text-transform: uppercase;
    /* font-size: 4em; */
    font-weight: 100;
    display: block;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }

  header {
    margin-bottom: 40px;
  }
</style>

<main>
  <h1>Distances and light in space</h1>
  <header>Solar system data from <a href="https://www.astropy.org/">https://www.astropy.org/</a></header>
  <div id="solar-system-objects">
    {#await bodyDataRequest then bodies}
      {#each bodies as body}
        <Body object={body} />
      {/each}
    {/await}
  </div>

  <p>
    ... and these distances pale in comparison to the other galaxies, which are
    at least 2.5 million light years away.
  </p>
</main>
