<template>
  <div id="app">
    <component :is="layout">
    	<router-view/>
    </component>
  </div>
</template>

<script src="./App.js"></script>