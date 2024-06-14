<script>
export default {
  props: {
    view: String
  },
  methods: {
    toggleLocale() {
      console.log("[custom] INFO: Toggling locale")

      const newLocale = this.$i18n.locale == 'en' ? 'hu' : 'en';
      this.$i18n.locale = newLocale;
      localStorage.setItem('locale', newLocale)

      document.title = this.$t('title.' + this.view)
    }
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

  <a @click="toggleLocale()" class="AsideButton"><slot></slot></a>
</template>