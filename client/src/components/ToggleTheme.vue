<script>
export default {
  methods: {
    toggleTheme() {
      console.log("[custom] INFO: Toggling theme")

      localStorage.theme = localStorage.theme === 'light' ? 'dark' : 'light';

      if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    },
  },
};
</script>

<template>
  <a @click="toggleTheme()" class="AsideButton"><slot></slot></a>
</template>