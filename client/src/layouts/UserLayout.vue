<script>
  // Phosphor Icons
  import { PhHouse, PhUser, PhPlus } from '@phosphor-icons/vue'

  // UI elements
  import AsideButton from '@/components/AsideButton.vue'
  import AsideInfo from '@/components/AsideInfo.vue'
  import ChangeLocale from '@/components/ChangeLocale.vue'
  import ToggleTheme from '@/components/ToggleTheme.vue'
  import Logout from '@/components/Logout.vue'

  export default {
    components: {
      // Phosphor Icons
      PhHouse,
      PhUser,
      PhPlus,

      // UI elements
      AsideButton,
      AsideInfo,
      ChangeLocale,
      ToggleTheme,
      Logout
    },
    props: {
      view: '',
      username: ''
    },
    data() {
      return {
        copied: false
      }
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
  <aside class="left-aside">
    <div>
      <div>
        <AsideButton routePath="/dashboard">
          <PhHouse v-if="view == 'Dashboard'" weight="fill" size="17px" />
          <PhHouse v-else weight="bold" size="17px" />

          <div :class="{ 'font-bold': view == 'Dashboard' }">
            {{ $t('button.dashboard') }}
          </div>
        </AsideButton>
      </div>
    </div>
    <div>
      <div>
        <ChangeLocale :view />
        <ToggleTheme />
      </div>
      <div class="divider my-8" v-if="username"></div>
      <div v-if="username">
        <AsideInfo>
          <PhUser weight="bold" size="17px" />
          {{ username }}
        </AsideInfo>
        <Logout />
      </div>
    </div>
  </aside>
</template>
