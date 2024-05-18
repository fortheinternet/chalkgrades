<script>
export default {
  methods: {
    toggleTheme() {
      localStorage.theme = localStorage.theme === 'light' ? 'dark' : 'light';

      if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark')
      }
      
      else {
        document.documentElement.classList.remove('dark')
      }
    },
  },
};
</script>

<template>
  <!--
    <div class="locale-changer">
      <select v-model="$i18n.locale">
        <option v-for="locale in $i18n.availableLocales" :key="`locale-${locale}`" :value="locale">{{ locale }}</option>
      </select>
    </div>
  -->

  <a @click="toggleTheme()" class="AsideButton-btn"><slot></slot></a>
  
</template>