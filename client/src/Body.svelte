<script>
  export let object;
</script>

<style>
  h1 {
    text-transform: uppercase;
  }
  .space-object {
    border: 1px solid black;
    border-radius: 4px;
    padding: 10px;
    margin: 10px;
    flex: 0 0 25%;
  }
</style>

<div class="space-object">
  <h1>{object.name}</h1>
  <p>You're seeing what it looked like {object.delta} ago</p>
</div>
