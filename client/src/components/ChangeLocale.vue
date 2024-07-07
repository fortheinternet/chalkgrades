<script>
  // Phosphor Icons
  import { PhCaretRight, PhCaretDown, PhCheck } from '@phosphor-icons/vue'

  // UI elements
  import AsideButton from '@/components/AsideButton.vue'

  export default {
    components: {
      // Phosphor Icons
      PhCaretRight,
      PhCaretDown,
      PhCheck,

      // UI elements
      AsideButton
    },
    props: {
      view: ''
    },
    data() {
      return {
        selected: false
      }
    },
    methods: {
      toggleSelected() {
        this.selected = !this.selected
      },
      changeLocale(newLocale) {
        console.log('Updating locale')

        this.$i18n.locale = newLocale
        localStorage.setItem('locale', newLocale)

        document.title = this.$t('title.' + this.view)
      }
    }
  }
</script>

<template>
  <AsideButton @click="toggleSelected()">
    <PhCaretRight weight="bold" size="17px" v-if="!selected" />
    <PhCaretDown weight="bold" size="17px" v-else />

    {{ $t('button.changelang') }}
  </AsideButton>

  <AsideButton
    v-if="selected"
    v-for="locale in $i18n.availableLocales"
    :key="locale"
    @click="changeLocale(locale)"
  >
    <PhCheck weight="bold" size="17px" v-if="$i18n.locale == locale" />
    <div class="h-[17px] w-[17px]" v-else></div>

    <div :class="{ 'font-bold': $i18n.locale == locale }">
      {{ $t(`languages.${locale}`) }}
    </div>
  </AsideButton>
</template>
