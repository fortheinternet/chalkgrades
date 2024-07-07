<script>
  // Phosphor Icons
  import { PhSignOut } from '@phosphor-icons/vue'

  // UI elements
  import AsideButton from '@/components/AsideButton.vue'

  export default {
    components: {
      // Phosphor Icons
      PhSignOut,

      // UI elements
      AsideButton
    },
    methods: {
      logout() {
        localStorage.removeItem('token')
        this.$router.push('/')
      }
    }
  }
</script>

<template>
  <AsideButton @click="logout">
    <PhSignOut weight="bold" size="17px" />
    {{ $t('button.logout') }}
  </AsideButton>
</template>
