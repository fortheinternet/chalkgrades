<script>
// Menus
import LandingMenu from '@/components/menus/LandingMenu.vue'

// UI elements
import ChipButton from '@/components/elements/ChipButton.vue';

export default {
  components: {
    // Menus
    LandingMenu,

    // UI elements
    ChipButton
  },
  created() {
    document.title = this.$t('title.Home')
  }
};
</script>

<template>
  <LandingMenu view="Home"/>
  <main>
    <article>
      <h4>{{ $t('text.heading.landing-1') }}</h4>
      <p class="subtext">{{ $t('text.paragraph.landing-1') }}</p>
    </article>

    <div class="flex sm:flex-row flex-col">
      <ChipButton routePath="/login" :internal="true" :highlighted="true">{{ $t('button.login') }}</ChipButton>
      <ChipButton routePath="https://github.com/fortheinternet/chalkgrades" :internal="false" :highlighted="false">{{ $t('button.github') }}</ChipButton>
    </div>

  </main>
</template>