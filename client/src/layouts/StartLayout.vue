<script>
  // Phosphor Icons
  import {
    PhGithubLogo,
    PhCloudCheck,
    PhUser,
    PhHouse,
    PhGraduationCap,
    PhLock
  } from '@phosphor-icons/vue'

  // UI elements
  import AsideButton from '@/components/AsideButton.vue'
  import ChangeLocale from '@/components/ChangeLocale.vue'
  import ToggleTheme from '@/components/ToggleTheme.vue'

  export default {
    components: {
      // Phosphor Icons
      PhGithubLogo,
      PhCloudCheck,
      PhUser,
      PhHouse,
      PhGraduationCap,
      PhLock,

      // UI elements
      AsideButton,
      ChangeLocale,
      ToggleTheme
    },
    props: {
      view: ''
    }
  }
</script>

<template>
  <aside class="left-aside">
    <div>
      <div>
        <AsideButton routePath="/">
          <PhHouse v-if="view == 'Home'" weight="fill" size="17px" />
          <PhHouse v-else weight="bold" size="17px" />

          <div :class="{ 'font-bold': view == 'Home' }">
            {{ $t('button.home') }}
          </div>
        </AsideButton>

        <AsideButton routePath="/login">
          <PhUser v-if="view == 'Login'" weight="fill" size="17px" />
          <PhUser v-else weight="bold" size="17px" />

          <div :class="{ 'font-bold': view == 'Login' }">
            {{ $t('button.login') }}
          </div>
        </AsideButton>
      </div>
      <div class="divider my-8"></div>
      <div>
        <AsideButton routePath="https://github.com/fortheinternet/chalkgrades">
          <PhGithubLogo weight="bold" size="17px" />
          {{ $t('button.github') }}
        </AsideButton>

        <AsideButton
          routePath="https://fortheinternet.notion.site/API-Documentation-WIP-be3e672768d243aa855209b4f6e475bb?pvs=4"
        >
          <PhCloudCheck weight="bold" size="17px" />
          {{ $t('button.api-docs') }}
        </AsideButton>

        <AsideButton
          routePath="https://fortheinternet.notion.site/Credits-19a5c234927c47179cb89e00a8149201?pvs=4"
        >
          <PhGraduationCap weight="bold" size="17px" />
          {{ $t('button.credits') }}
        </AsideButton>
      </div>
    </div>
    <div>
      <div>
        <ChangeLocale :view />
        <ToggleTheme />
      </div>
    </div>
  </aside>
</template>
