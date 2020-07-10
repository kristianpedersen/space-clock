<script>
  export let object;
</script>

<style>
  .space-object {
    border: 1px solid black;
    border-radius: 4px;
    padding: 10px;
    margin: 10px;
    max-width: 25%;
    display: inline-block;
  }
</style>

<div class="space-object">
  <h1>{object.name}</h1>
  <p>Når du ser på {object.name} ser du {object.delta} tilbake i tid.</p>
</div>
