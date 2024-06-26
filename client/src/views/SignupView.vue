<script>
// Menus
import LandingMenu from '@/components/menus/LandingMenu.vue'

// UI elements
import ChipButton from '@/components/elements/ChipButton.vue';
import FormInputs from '@/components/elements/FormInputs.vue';

export default {
  components: {
    // Menus
    LandingMenu,

    // UI elements
    ChipButton,
    FormInputs
  },
  created() {
    document.title = this.$t('title.Signup')
  }
};
</script>

<template>
  <LandingMenu view="Signup"/>
  <main>
    <article>
      <h4>{{ $t('text.heading.signup-1') }}</h4>
      <p class="dark:text-opacity-55 text-opacity-55 dark:text-white text-black">{{ $t('text.paragraph.signup-1') }}</p>
    </article>
  </main>
</template>